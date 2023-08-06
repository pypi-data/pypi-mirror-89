from saplings import Saplings
from rendering import render_tree, dictify_tree
import ast
from pprint import pprint

my_program = open("test_input.py", "r").read()
program_ast = ast.parse(my_program)
my_saplings = Saplings(program_ast)

for root_node in my_saplings.get_trees():
    for branches, node in render_tree(root_node):
        print(f"{branches}{node}")

    print()
