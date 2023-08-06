# So you can execute the file with python to test the file
if __name__ == "__main__":
    import subprocess
    # use -k <string> to only run tests which contain the provided string
    subprocess.run('pytest')
    exit()

# the repo path has to be added to sys.path, or else this package won't be found
import sys, os
parent_dir = os.path.join(os.path.dirname(__file__), '..\\..')

# imports for the tests
import pytest
import copy
from utility.misc import *

def test_rotate_list():
    l = [1, 2, 3]
    assert rotate_list(l, 1) == [3, 1, 2]
    assert l == [1, 2, 3]

    assert rotate_list(l, -1) == [2, 3, 1]
    assert rotate_list(l, 2) == [2, 3, 1]

    assert rotate_list(l, 3) == [1, 2, 3]

    assert rotate_list(l, 4) == [3, 1, 2]
    assert rotate_list(l, 7) == [3, 1, 2]

def test_pad_1d_list():
    # test expected behavior
    l = [1, 2, 3]
    o = [0, 1, 2, 3, 0]
    assert pad_1d_list(l, 0) == o
    assert l == o

    # test thickness argument
    assert pad_1d_list([1, 2], 0, -1) == [1, 2]
    assert pad_1d_list([1, 2], 0)     == [0, 1, 2, 0]
    assert pad_1d_list([1, 2], 0, 1)  == [0, 1, 2, 0]
    assert pad_1d_list([1, 2], 0, 2)  == [0, 0, 1, 2, 0, 0]

    # test differne objects as elements
    assert pad_1d_list([1, 2], '#-#') == ['#-#', 1, 2, '#-#']
    assert pad_1d_list([1, 2], [1,2]) == [[1,2], 1, 2, [1,2]]

def test_pad_2d_list():
    # test expected behavior
    l = [[1, 2],
         [3, 4]]
    o = [[0, 0, 0, 0],
         [0, 1, 2, 0],
         [0, 3, 4, 0],
         [0, 0, 0, 0]]
    assert pad_2d_list(l, 0) == o
    assert l == o

    # test thickness argument
    l  = [[1]]
    o1 = [[0, 0, 0],
          [0, 1, 0],
          [0, 0, 0]]
    o2 = [[0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0],
          [0, 0, 1, 0, 0],
          [0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0]]

    assert pad_2d_list(copy.deepcopy(l), 0,-1) == l
    assert pad_2d_list(copy.deepcopy(l), 0, 0) == l
    assert pad_2d_list(copy.deepcopy(l), 0, 1) == o1
    assert pad_2d_list(copy.deepcopy(l), 0, 2) == o2