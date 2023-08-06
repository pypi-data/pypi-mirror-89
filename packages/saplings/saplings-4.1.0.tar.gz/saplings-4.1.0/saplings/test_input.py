import zipfile
import os
from itertools import product
from collections import defaultdict
import glob
from tqdm import tqdm
from re import match
import shutil
from time import time
import pickle
from functools import partial

import numpy as np
from pandas import read_csv

from nilearn import image
from nilearn.connectome import ConnectivityMeasure

from src.last_hope.create_adhd_dataset import fetch_atlas_masker_and_coords, prepare_fc_matrix_for_dataset
from src.last_hope.utilities import strip_adj_matrix_of_weight_label, Load_Timer, concurrent_exec

def get_block_times(run_path, tr=301/405, bonus_duration=0):
    EV_path = os.path.join(run_path, 'EVs')
    StimTypes = ['_body', '_faces', '_places', '_tools']
    bks = ['0bk', '2bk']
    products = list(product(bks, StimTypes))
    fns = [''.join(product_) + '.txt' for product_ in products]
    block_times = {}
    for i, fn in enumerate(fns):
        f = open(os.path.join(EV_path, fn), 'r')
        line = f.read()
        onset_t = line.split('\t')[0]
        duration = float(line.split('\t')[1])
        duration += bonus_duration
        onset_tr = int(float(onset_t) / tr)
        final_tr = int((float(onset_t) + float(duration)) / tr)
        block_times[products[i]] = (onset_tr, final_tr+1) # note: TR + 1
    return block_times

def get_faces_vs_places(nii, run_path):
    block_times = get_block_times(run_path) # this function must be inside the get_ functions for this to work with SOC
    StimTypes_A = ['_faces']
    bks_A = ['0bk', '2bk']
    products_A = list(product(bks_A, StimTypes_A))
    TRs_A = get_TRs(products_A, block_times)

    StimTypes_B = ['_places']
    bks_B = ['0bk', '2bk']
    products_B = list(product(bks_B, StimTypes_B))
    TRs_B = get_TRs(products_B, block_times)
    return image.index_img(nii, TRs_A), image.index_img(nii, TRs_B)

def get_tools_vs_body(nii, run_path):
    block_times = get_block_times(run_path)
    StimTypes_A = ['_tools']
    bks_A = ['0bk', '2bk']
    products_A = list(product(bks_A, StimTypes_A))
    TRs_A = get_TRs(products_A, block_times)

    StimTypes_B = ['_body']
    bks_B = ['0bk', '2bk']
    products_B = list(product(bks_B, StimTypes_B))
    TRs_B = get_TRs(products_B, block_times)
    return image.index_img(nii, TRs_A), image.index_img(nii, TRs_B)

# test for link between social and gambling tasks?

def get_TRs(products, block_times):
    TRs = []
    for prd in products:
        times = block_times[prd]
        TRs.extend(list(range(times[0], times[1])))
    return TRs

def get_high_vs_low_load(nii, run_path):
    block_times = get_block_times(run_path)
    #print('block_times:')
    #print(block_times)
    #quit()
    StimTypes = ['_body', '_faces', '_places', '_tools']
    bks_2 = ['2bk']
    products_2 = list(product(bks_2, StimTypes))
    TRs_2 = get_TRs(products_2, block_times)

    bks_0 = ['0bk']
    products_0 = list(product(bks_0, StimTypes))
    TRs_0 = get_TRs(products_0, block_times)
    return image.index_img(nii, TRs_2), image.index_img(nii, TRs_0)

def get_all_for_aug(sn, nii, run_path, lr, outpath_examples, get_blk_times_specific=get_block_times):
    lt = Load_Timer('\tdo_4D_examples')

    block_times = get_blk_times_specific(run_path, bonus_duration=8)
    name_counter = defaultdict(lambda: 0)
    for name, times in block_times.items():
        if isinstance(name, tuple):
            name = ''.join(name)

        times_list = list(range(times[0], times[1]))
        #if
        #shape = image.get_data().shape[4]
        pruned_img = image.index_img(nii, times_list)
        save_4D_augged(sn, name, name_counter, lr, pruned_img, outpath_examples)

        #if len(times_list) == 27:
        #    #print('times list:', times_list)
        #    pruned_img = image.index_img(nii, times_list)
        #elif len(times_list) < 27:
        #    print('tooo short')
        #    raise('Error times_list is under 27')
        #else:
        #    for i in range(len(times_list)-27):
        #        #print('times list len:', len(times_list), 'i:', i)
        #        pruned_img = image.index_img(nii, list(range(i, i+27)))
        #        save_4D_augged(sn, name, name_counter, lr, pruned_img, outpath_examples)
    num_examples = sum(n for n in name_counter.values())
    print('Total number of examples for LR:', num_examples)
    print()
    lt.print_time()

def save_4D_augged(sn, name, name_counter, lr, pruned_img, outpath_examples):
    if name[-2:] in ['_0', '_1', '_2', '_3', '_4', '_5', '_6']:
        #print('name pre:', name)
        name = name[:-2]
        #print('name post:', name)
    label_dir = os.path.join(outpath_examples, name + '_4D')
    os.makedirs(label_dir, exist_ok=True)

    name_counter[name] += 1
    nii_4D_example = {
        "subject_id": sn,
        'label': name,
        'bootstrap_id': 0 if lr == 'LR' else 1,
        'nii': pruned_img,
        "global_feats": {},
        'subj_chars': SUBJ_CHAR_MANAGER.get_subj_data(sn),
    }
    fp = os.path.join(outpath_examples, name + '_4D', '{sn}_{lr}_{cnt}.pkl'.format(sn=sn, cnt=name_counter[name], lr=lr))
    with open(fp, 'wb') as file:
        pickle.dump(nii_4D_example, file)

def save_FC_example(nii, sn, label, lr, outpath_examples):
    lt = Load_Timer('\tsave_FC_example')
    confounds = image.high_variance_confounds(nii)
    time_series_list = []
    for i, masker in enumerate(MASKERS):
        time_series_list.append(masker.fit_transform(nii, confounds=confounds))
        print(i, 'time series shape:', time_series_list[-1].shape)
    time_series = np.concatenate(time_series_list, axis=1)
    fc_matrix = CONNECTIVITY_MEASURE.fit_transform([time_series])[0]
    np.fill_diagonal(fc_matrix, 0)
    #fc_matrix = prepare_fc_matrix_for_dataset(fc_matrix, connectivity_measure='correlation')
    FC_example = {
        "subject_id": sn,
        'label': label,
        'bootstrap_id': 0 if lr == 'LR' else 1,
        "adj_matrix": fc_matrix,
        "node_feats": [{} for _ in range(len(fc_matrix))],
        "global_feats": {},
        'subj_chars': SUBJ_CHAR_MANAGER.get_subj_data(sn),
        "node_time_series": time_series.T
    }

    label_dir = os.path.join(outpath_examples, FC_example['label'])
    os.makedirs(label_dir, exist_ok=True)
    fp = os.path.join(label_dir, sn + '_' + lr + '.pkl')
    with open(fp, 'wb') as file:
        pickle.dump(FC_example, file)
    lt.print_time()

def save_flat_3D_vol(nii, sn, label, lr, outpath_examples):
    lt = Load_Timer('\tsave_flat_3d_vol')
    nii_mean = image.mean_img(nii)
    nii_mean_example = {
        "subject_id": sn,
        'label': label,
        'bootstrap_id': 0 if lr == 'LR' else 1,
        'nii': nii_mean,
        "global_feats": {},
        'subj_chars': SUBJ_CHAR_MANAGER.get_subj_data(sn),
    }
    label_dir = os.path.join(outpath_examples, label + '_3D')
    os.makedirs(label_dir, exist_ok=True)
    fp = os.path.join(label_dir, sn + '_' + lr + '.pkl')
    with open(fp, 'wb') as file:
        pickle.dump(nii_mean_example, file)
    lt.print_time()

def create_FC_examples_general(sn, lr, outpath_examples, outpath_unzip,
                               conditions=(get_faces_vs_places, ('faces', 'places')),
                               task='WM', do_FC=False, do_flat_3D=False, do_4D_aug=True):
    print('test conditions:', conditions
          )
    lt = Load_Timer('\tLoad image')
    run_path = os.path.join(outpath_unzip, sn, 'MNINonLinear', 'Results', 'tfMRI_' + task + '_' + lr)
    img_path = os.path.join(run_path, 'tfMRI_' + task + '_' + lr + '.nii.gz')
    nii_total = image.load_img(img_path)
    if do_FC or do_flat_3D:
        niis = conditions[0](nii_total, run_path)
        lt.print_time()
        for i, nii in enumerate(niis):
            if do_FC:
                save_FC_example(nii, sn, conditions[1][i], lr, outpath_examples)
            if do_flat_3D:
                save_flat_3D_vol(nii, sn, conditions[1][i], lr, outpath_examples)

    if do_4D_aug:
        print('do 4D aug...')
        print(conditions)
        print(conditions[2])
        get_all_for_aug(sn, nii_total, run_path, lr, outpath_examples, get_blk_times_specific=conditions[2])

def is_subject_already_done(sn, conditions, outpath_examples):
    did_FC = True
    did_3D = True
    did_4D = True
    for label in conditions[1]:
        for lr in ['LR', 'RL']:
            fp = os.path.join(outpath_examples, label, sn + '_' + lr + '.pkl')
            if not os.path.isfile(fp):
                did_FC = False
            fp_3d = os.path.join(outpath_examples, label + '_3D', sn + '_' + lr + '.pkl')
            if not os.path.isfile(fp_3d):
                did_3D = False
            fp_4d = os.path.join(outpath_examples, label + '_4D', '{sn}_{lr}_{cnt}.pkl'.format(sn=sn, cnt=0, lr=lr))
            if not os.path.isfile(fp_4d):
                did_4D = False
    return did_FC, did_3D, did_4D

def process_subject_general(zip_fn, inpath, outpath_examples, outpath_unzip,
                            conditions=(get_faces_vs_places, ('faces', 'places')),
                            task='WM', do_FC=True, do_flat_3D=True, do_4D_aug=True):

    print('Processing', zip_fn, 'for conditions:', conditions, '...')
    sn = zip_fn.split('_')[0]
    try:
        start = time()
        extract_zip_specific_files(zip_fn, inpath, outpath_unzip) # extract the zip on my external HDD (F:)
        print('Zip extract time =', round(time()-start,3), 's')
    except Exception as e:
        print('Error! Failed on unzipping!')
        print('e:', e)
        return

    #start = time()
    #for lr in ['LR', 'RL']:
    #    create_FC_examples_general(sn, lr, outpath_examples, outpath_unzip, conditions=conditions, task=task,
    #                               do_FC=do_FC, do_flat_3D=do_flat_3D, do_4D_aug=do_4D_aug)
    #print('FC create time =', round(time()-start,3), 's')

    ##
    try:
        start = time()
        for lr in ['LR', 'RL']:
            create_FC_examples_general(sn, lr, outpath_examples, outpath_unzip, conditions=conditions, task=task,
                                       do_FC=do_FC, do_flat_3D=do_flat_3D, do_4D_aug=do_4D_aug)
        print('FC create time =', round(time()-start,3), 's')
    except Exception as e:
        print('Error! Failed on creating the FC matrix')
        print('e:', e)

    ##
    try:
        start = time()
        delete_extracted_dir(sn, outpath_unzip) # delete the files extracted from the .zip to save space
        print('Delete time =', round(time()-start, 3), 's')
    except Exception as e:
        print('Error! Failed on deleting!?!?')
        print('e:', e)
    return

def delete_extracted_dir(sn, outpath_unzip):
    if int(sn) == 100206: # this first subject is the example used in extract_zip_specific_files
        return
    dir_path = os.path.join(outpath_unzip, sn)
    shutil.rmtree(dir_path)

def process_all_subjects_general(zip_fns, inpath, outpath_examples, outpath_unzip,
                                 conditions=(get_faces_vs_places, ('faces', 'places')),
                                 task='WM', do_FC=False, do_flat_3D=False, atlas='power',
                                 do_4D_aug=True):
    set_masker(atlas)
    for zip_fn in tqdm(zip_fns):
        sn = zip_fn.split('_')[0]
        print('\n', 'subject:', sn)
        if not SUBJ_CHAR_MANAGER.is_subj_valid(sn):
            print('not valid:', sn)
            continue
        did_FC, did_flat_3D, did_4D = is_subject_already_done(sn, conditions, outpath_examples)
        print('Did FC:', did_FC)
        print('Did flat 3D:', did_flat_3D)
        if (did_FC or not do_FC) and (did_flat_3D or not do_flat_3D) and (did_4D or not do_4D_aug):
            print('Skipping...')
            continue
        process_subject_general(zip_fn, inpath, outpath_examples, outpath_unzip,
                                conditions=conditions,
                                task=task,
                                do_FC=do_FC and not did_FC,
                                do_flat_3D=do_flat_3D and not did_flat_3D,
                                do_4D_aug=do_4D_aug)

def extract_zip_specific_files(zip_fn, inpath, outpath_unzip, max_size=1e6,):

    sn = zip_fn.split('_')[0]
    if os.path.isdir(os.path.join(outpath_unzip, sn)):
        print('Zip file already extracted for', sn)
        return

    if 'WM' in inpath:
        example_fp = r'E:\PycharmProjects\ScratchPad\HCP\HCP_WM_data\100206'
        acceptable_override = ('tfMRI_WM_LR.nii.gz', 'tfMRI_WM_RL.nii.gz')
    elif 'SOC' in inpath:
        example_fp = r'E:\PycharmProjects\ScratchPad\HCP\HCP_SOC_data\100206'
        acceptable_override = ('tfMRI_SOCIAL_LR.nii.gz', 'tfMRI_SOCIAL_RL.nii.gz')
    elif 'EMO' in inpath:
        example_fp = r'E:\PycharmProjects\ScratchPad\HCP\HCP_EMO_data\100206'
        acceptable_override = ('tfMRI_EMOTION_LR.nii.gz', 'tfMRI_EMOTION_RL.nii.gz')
    elif 'DEC' in inpath:
        example_fp = r'E:\PycharmProjects\ScratchPad\HCP\HCP_DEC_data\100206'
        acceptable_override = ('tfMRI_GAMBLING_LR.nii.gz', 'tfMRI_GAMBLING_RL.nii.gz')
    elif 'MOTOR' in inpath:
        example_fp = r'E:\PycharmProjects\ScratchPad\HCP\HCP_MOTOR_data\100206'
        acceptable_override = ('tfMRI_MOTOR_LR.nii.gz', 'tfMRI_MOTOR_RL.nii.gz')
    else:
        print('Error, invalid inpath name! Should be WM, SOC, EMO, or DEC')
        raise

    all_archive_fps = glob.glob(os.path.join(example_fp, '**'), recursive=True)

    good_fps = []
    for fp in all_archive_fps:
        fn = os.path.split(fp)[-1]
        if fn in acceptable_override:
            good_fps.append(fp)
        if os.path.getsize(fp) <= max_size:
            good_fps.append(fp)

    good_fps = [fp for fp in good_fps if os.path.isfile(fp) and '.sh' not in fp]
    good_fps = [fp.split(example_fp + '\\')[-1] for fp in good_fps if fp != example_fp + '\\']  # get only the tree within the directory, also exclude items that are just '\\'
    good_fps = [os.path.join(sn, fp) for fp in good_fps]
    good_fps = [fp.replace('\\', '/') for fp in good_fps]

    zip_fp = os.path.join(inpath, zip_fn)
    with zipfile.ZipFile(zip_fp, 'r') as z:
        for fp in good_fps:
            try: z.extract(fp, outpath_unzip)
            except Exception as e: print(e)

    # only takes 7.8 s if writing to E: drive

class Subject_char_manager():
    def __init__(self):
        self.df_char = read_csv('HCP_subj_data.csv')

    def get_subj_data(self, subject_id):
        df_subj = self.df_char[self.df_char['Subject'] == int(subject_id)]
        row_subj = df_subj.iloc[0]
        return row_subj.to_dict()

    def is_subj_valid(self, subject_id):
        df_subj = self.df_char[self.df_char['Subject'] == int(subject_id)]
        if len(df_subj) == 1:
            return True
        else:
            print('Subject:', subject_id, 'cannot be used. They have', len(df_subj), 'entries in HCP_subj_data.csv')
            return False

def combine_all_examples(outpath_examples, labels=('high_load', 'low_load'), max_n_per_label=1000,
                         atlas='power_harvOxSubChopped-5'):
    print('Combining all examples. Labels =', labels, 'n =', max_n_per_label)
    set_masker(atlas)
    from datetime import date
    print('len COORDS:', len(COORDS))
    combined_dict = {'node_coords': COORDS}
    for label in labels:
        label_dir = os.path.join(outpath_examples, label)
        label_fns = os.listdir(label_dir)
        print('number of potential examples:', len(label_fns))
        label_fns = label_fns[0:max_n_per_label]
        label_exs = []
        if len(label_fns) < max_n_per_label:
            print('Not enough examples!')
            print('    Ending!')
            return
        for fn in label_fns:
            #ex = pickle.load(open(os.path.join(label_dir, fn), 'rb'))
            #print('adj shape:', ex['adj_matrix'].shape)
            try:
                label_exs.append(pickle.load(open(os.path.join(label_dir, fn), 'rb')))
            except Exception as e:
                print('Error (!):', e)
                print('\tfile:', os.path.join(label_dir, fn))

        #label_exs = [pickle.load(open(os.path.join(label_dir, fn), 'rb')) for fn in label_fns]
        if isinstance(label_exs[0]['adj_matrix'][0][0], dict):
            print('Killing these adj matrices')
            for ex in label_exs:
                if isinstance(ex['adj_matrix'][0][0], dict):
                    ex['adj_matrix'] = strip_adj_matrix_of_weight_label(ex['adj_matrix'])
        combined_dict[label] = label_exs

    date_str = date.today().strftime('_%b%d_%y')
    output_fn = 'ex_n' + str(max_n_per_label) + '_' + '_'.join(labels) + date_str + '.pkl'
    print('Dumping...')
    with open(os.path.join(outpath_examples, output_fn), 'wb') as file:
        pickle.dump(combined_dict, file)
    print('All dumped. Quit now.')


CONNECTIVITY_MEASURE = ConnectivityMeasure(kind='correlation')
SUBJ_CHAR_MANAGER = Subject_char_manager()
MASKERS, COORDS = None, None
def set_masker(atlas_names):
    global MASKERS
    global COORDS
    atlas_names_list = atlas_names.split('_')
    MASKERS, COORDS = [], []
    for atlas_name in atlas_names_list:
        masker, coords = fetch_atlas_masker_and_coords(atlas_name=atlas_name)
        MASKERS.append(masker), COORDS.extend(coords)

def do_combine():
    for n in [100, 400, 800]:
        combine_all_examples(OUTPATH_EXAMPLES, labels=('high_load', 'low_load'), max_n_per_label=n,
                             atlas=ATLAS_NAME)
    quit()

if __name__ == '__main__':
    ATLAS_NAME = 'power_harvOxSubChopped-5'
    ATLAS_NAME = 'harOxCort'
    ATLAS_NAME = 'shaef'
    ATLAS_NAME = 'power'

    OUTPATH_UNZIP = r'HCP\HCP_WM_data'#r'F:\HCP_processed'
    OUTPATH_EXAMPLES = os.path.join('HCP', ATLAS_NAME, 'HCP_WM_examples')
    INPATH  = r'F:\HCP_WM_data'

    fns_all = glob.glob(os.path.join(INPATH, '*_3T_tfMRI_WM_preproc.zip'))
    fns_all = [os.path.split(fp)[-1] for fp in fns_all]
    print('number of files:', len(fns_all))
    starting = 0
    print('Starting:', starting)
    fns_all = fns_all[starting:]
    #do_combine()

    conds = (get_high_vs_low_load, ('high_load', 'low_load'), get_block_times)
    #conds = (get_high_vs_low_load, ('places', 'tools'))

    process_all_subjects_general(fns_all, INPATH, OUTPATH_EXAMPLES, OUTPATH_UNZIP, conditions=conds, do_flat_3D=False,
                                 atlas=ATLAS_NAME)

    #process_all_subjects_high_low(fns_all, OUTPATH_UNZIP)
    # TODO: compare emotion process faces vs. 0bk faces?
