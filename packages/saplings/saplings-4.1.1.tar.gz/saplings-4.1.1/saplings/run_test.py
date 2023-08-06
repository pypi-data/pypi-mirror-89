import ast
from saplings import Saplings
from rendering import render_tree


my_program = open("test_input.py", "r").read()
program_ast = ast.parse(my_program)
my_saplings = Saplings(program_ast)

trees = my_saplings.get_trees()
for root_node in trees:
    for branches, node in render_tree(root_node):
        print(f"{branches}{node}")

    print()
