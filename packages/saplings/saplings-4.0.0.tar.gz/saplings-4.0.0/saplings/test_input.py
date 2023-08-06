# import torch.nn as nn
# from torch import tensor
#
# class Perceptron(nn.Module):
#   loss = None
#
#   def __init__(self, in_channels, out_channels):
#     super(Perceptron, self).__init__()
#     self.layer = nn.Linear(in_channels, out_channels)
#     self.output = Perceptron.create_output_layer()
#
#   @staticmethod
#   def create_output_layer():
#     def layer(x):
#       return x.mean()
#
#     return layer
#
#   @classmethod
#   def calculate_loss(cls, output, target):
#     cls.loss = output - target
#     return cls.loss
#
#   def __call__(self, x):
#     x = self.layer(x)
#     return self.output(x)
#
# model = Perceptron(1, 8)
# output = model(tensor([10]))
# loss = Perceptron.calculate_loss(output, 8)

# Standard Library
import os
import time
import pickle
import bisect
import random
import warnings
from statistics import mean, stdev
from collections import Counter

# Third Party
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.signal import savgol_filter, find_peaks
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from youtube_transcript_api import YouTubeTranscriptApi as yt_transcript_api
from wikipedia import search as wikisearch
from pprint import pprint
from deepsegment import DeepSegment
from sentence_transformers import SentenceTransformer

VIDEO_ID = "ycPr5-27vSI"
DS_WINDOW = 20 # Window size (in words) for iterative segmentation
K = 100 # Average number of sentences in a JRE clip
# ALPHA = 0.5
FILTER_WINDOW = 25 # Length of the Savitzky-Golay filter window (i.e. # of
                   # coefficients); must be an odd integer
STOP_WORDS = set(stopwords.words("english"))
PROP_NOUNS = ("NNP", "NNPS")
NOUNS = ("NN", "NNS") + PROP_NOUNS
VERBS = ("VB", "VBD", "VBG", "VBN", "VBP", "VBZ")
# TODO: Only include nouns and intransitive verbs if possible
VALID_POS = NOUNS + PROP_NOUNS #+ VERBS

warnings.filterwarnings("ignore")


##########################
# TOPIC BOUNDARY DETECTION
##########################


def fetch_transcript():
    data = yt_transcript_api.get_transcript(VIDEO_ID)
    return pd.DataFrame(data)


def flatten_transcript(transcript_df):
    curr_index = 0
    transcript_text, index_to_timestamp = "", {}
    for _, row in transcript_df.iterrows():
        row_text = row["text"] + " "
        transcript_text += row_text
        index_to_timestamp[curr_index] = {
            "start": row["start"],
            "duration": row["duration"]
        }
        curr_index += len(row_text)

    return transcript_text, index_to_timestamp


def estimate_start_time(bisect_index, word_index, timestamp_indices, index_to_timestamp):
    nearest_ts_index = timestamp_indices[bisect_index]
    ts_data = index_to_timestamp[nearest_ts_index]
    words_covered = word_index - nearest_ts_index
    total_words_in_duration = timestamp_indices[bisect_index + 1] - nearest_ts_index

    start_ts, duration = ts_data["start"], ts_data["duration"]
    t_passed = duration * words_covered / total_words_in_duration

    estimated_ts = start_ts + t_passed
    return estimated_ts


def extract_sentences(transcript_df):
    # TODO: Rename index_to_timestamp as index_to_metadata
    segmenter = DeepSegment("en")
    transcript_text, index_to_timestamp = flatten_transcript(transcript_df)
    sentences = segmenter.segment_long(transcript_text, n_window=DS_WINDOW)

    sentences_with_metadata = []
    word_index, timestamp_indices = 0, list(index_to_timestamp.keys())
    for sent_index, sentence in enumerate(sentences):
        bisect_index = bisect.bisect_left(timestamp_indices, word_index)
        if timestamp_indices[bisect_index] > word_index:
            bisect_index -= 1

        estimated_ts = estimate_start_time(
            bisect_index,
            word_index,
            timestamp_indices,
            index_to_timestamp
        )
        word_index += len(sentence + " ")

        sentences_with_metadata.append({
            "sentence": sentence,
            "timestamp": estimated_ts
        })

    return sentences_with_metadata


def vectorize_sentences(sentences):
    model = SentenceTransformer("bert-base-nli-mean-tokens")
    sentence_embeddings = model.encode([s["sentence"] for s in sentences])

    sentences_with_vectors = []
    for sentence, embedding in zip(sentences, sentence_embeddings):
        sentences_with_vectors.append({**sentence, **{"embedding": embedding}})

    return sentences_with_vectors


def compute_similarity_vals(sentences):
    sim_vals = [0.0]
    for i in range(1, len(sentences)):
        left_sents = sentences[:i] if i <= K else sentences[i - K:i]
        right_sents = sentences[i:i + K]

        left_embeddings = [s["embedding"] for s in left_sents]
        right_embeddings = [s["embedding"] for s in right_sents]

        left_mean_emb = np.array(left_embeddings).mean(axis=0)
        right_mean_emb = np.array(right_embeddings).mean(axis=0)

        numer = np.dot(left_mean_emb, right_mean_emb)
        denom = np.linalg.norm(left_mean_emb) * np.linalg.norm(right_mean_emb)
        cosine_sim = numer / denom if denom else 0.0

        sim_vals.append(cosine_sim)

    return sim_vals


def compute_boundary_probs(sim_vals, sentences):
    probs = [1.0]
    for i in range(1, len(sim_vals)):
        left_sim_vals = sim_vals[:i + 1] if i <= K else sim_vals[i - K:i]
        right_sim_vals = sim_vals[i:i + K]

        left_max, right_max = max(left_sim_vals), max(right_sim_vals)
        prob = 0.5 * ((left_max + right_max) - 2 * sim_vals[i])

        probs.append(prob)

    # u = mean(probs[1:-1])
    # sigma = stdev(probs[1:-1])
    # threshold = u - (ALPHA * sigma)

    sentences_with_boundary_probs = []
    for prob, sentence in zip(probs, sentences):
        # prob = prob if prob >= threshold else 0.0
        sentences_with_boundary_probs.append({
            **sentence,
            **{"probability": prob}
        })

    return sentences_with_boundary_probs


def get_sentences_in_segment(sentences, index, next_index):
    return [s["sentence"] for s in sentences[index: next_index]]


def identify_boundaries(sentences):
    candidates = sentences # [s for s in sentences if s["probability"]]

    probs = [c["probability"] for c in candidates]
    smoothed_probs = savgol_filter(probs, FILTER_WINDOW, 3)
    peaks, _ = find_peaks(smoothed_probs)
    sorted_peaks = sorted(peaks, key=lambda p: smoothed_probs[p], reverse=True)

    num_boundaries = int(len(sentences) / K)
    top_peaks = sorted(sorted_peaks[:num_boundaries])

    print("\t\tPlotting boundary probabilities and peaks")
    plt.plot(probs, color="blue")
    plt.plot(top_peaks, smoothed_probs[top_peaks], "x", color="red")
    plt.show()

    boundaries, start_ts = {}, 0
    for index in range(num_boundaries - 1):
        peak_index, next_peak_index = top_peaks[index], top_peaks[index + 1]
        candidate = candidates[peak_index]
        end_ts = candidate["timestamp"]
        start_ts_str = time.strftime("%H:%M:%S", time.gmtime(start_ts))

        boundaries[start_ts_str] = get_sentences_in_segment(
            sentences,
            peak_index,
            next_peak_index
        )
        start_ts = end_ts

    return boundaries


################
# TOPIC LABELING
################


def create_similarity_matrix(vectors):
    num_nodes = len(vectors)
    sim_matrix = [[0.0 for _ in range(num_nodes)] for _ in range(num_nodes)]
    for i, source in enumerate(vectors):
        for j, target in enumerate(vectors):
            if j >= i:
                break

            numer = np.dot(source, target)
            denom = np.linalg.norm(source) * np.linalg.norm(target)
            cosine_sim = numer / denom if denom else 0.0

            sim_matrix[i][j] = cosine_sim
            sim_matrix[j][i] = cosine_sim

    return nx.from_numpy_matrix(np.matrix(sim_matrix))


def create_word_vectors(words, embeddings):
    for word in words:
        # BUG: This condition would never be hit with a better embeddings
        # dataset
        if word not in embeddings:
            continue

        yield [float(val) for val in embeddings[word]]


def rank_keywords(keywords, embeddings):
    if not keywords:
        return keywords

    # keyword_freqs = sorted(
    #     Counter(keywords).items(),
    #     key=lambda item: item[1],
    #     reverse=True
    # )
    # return [keyword for keyword, freq in keyword_freqs if freq > 1]

    keywords = list(set(keywords))
    keyword_vectors = list(create_word_vectors(keywords, embeddings))
    sim_matrix = create_similarity_matrix(keyword_vectors)
    weighted_degrees = sorted(
        dict(sim_matrix.degree(weight="weight")).items(),
        key=lambda item: item[1],
        reverse=False
    )

    return [keywords[i] for i, degree in weighted_degrees]


def construct_query(keywords, num_keywords=None):
    keywords = keywords if not num_keywords else keywords[:num_keywords]
    query, num_words = "", 0
    for keyword in keywords:
        if len(query + keyword + " ") >= 300:
            break

        query += keyword + " "
        num_words += 1

    # IDEA: This might be useful for creating better queries:
    # https://en.wikipedia.org/wiki/Help:Searching#Search_string_syntax

    return query[:-1]


def extract_keywords(sentences):
    # TODO: Check how word_tokenize handles punctuation
    # TODO: Remove text surrounded by brackets (e.g. [Music])
    # QUESTION: Should I lemmatize words?

    # TODO: Remove punctuation

    keywords = []
    for sentence in sentences:
        words = (word.lower() for word in word_tokenize(sentence))
        words = [word for word in words if word not in STOP_WORDS]
        for word, pos in pos_tag(words):
            if pos not in VALID_POS:
                continue
            if len(word) < 3:
                continue

            keywords.append(word)

    return keywords


def load_word_embeddings(filepath):
    embeddings = {}
    with open(filepath, 'r', encoding="utf-8") as f:
        for line in f:
            values = line.split()
            word = values[0]
            embeddings[word] = values[1:]

    return embeddings


def retrieve_search_results(query, max_num_words=None):
    if not query:
        return []

    search_results = wikisearch(query.split(" "))
    return search_results


def label_topic_segments(boundaries):
    embeddings = load_word_embeddings("./data/glove.6B.50d.txt")
    labeled_segments = {}
    for timestamp, sentences in boundaries.items():
        keywords = extract_keywords(sentences)
        ranked_keywords = rank_keywords(keywords, embeddings)
        query = construct_query(ranked_keywords)
        search_results = retrieve_search_results(query)

        label = search_results[:8] if search_results else "N/A"
        labeled_segments[timestamp] = label

    return labeled_segments


if __name__ == "__main__":
    path_to_cached_data = f"./data/sentence_embeds.{DS_WINDOW}.{VIDEO_ID}.pkl"
    if not os.path.exists(path_to_cached_data):
        print(f"\tFetching transcript (video_id={VIDEO_ID})")
        transcript_df = fetch_transcript()

        print(f"\tExtracting sentences from transcript (ds_window={DS_WINDOW})")
        sentences = extract_sentences(transcript_df)

        print("\tVectorizing sentences")
        sentences = vectorize_sentences(sentences)

        print(f"\t\tSaving sentence embeddings (store={path_to_cached_data})")
        pickle.dump(sentences, open(path_to_cached_data, "wb"))
    else:
        print(f"\tLoading sentence embeddings (store={path_to_cached_data})")
        sentences = pickle.load(open(path_to_cached_data, "rb"))

    print(f"\tComputing similarity values (k={K})")
    sim_vals = compute_similarity_vals(sentences)

    print(f"\tComputing boundary probabilities (k={K})")
    sentences = compute_boundary_probs(sim_vals, sentences)

    print(f"\tIdentifying boundaries (filter_window={FILTER_WINDOW})")
    boundaries = identify_boundaries(sentences)

    print("\tLabeling topic segments")
    labeled_segments = label_topic_segments(boundaries)
    pprint(labeled_segments, indent=16)
