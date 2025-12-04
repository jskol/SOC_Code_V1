import numpy as np
import re
from termcolor import colored
from datetime import datetime
import sys, os

curr_dir=os.path.dirname(os.path.abspath(__file__)) #
parent_dir = os.path.dirname(curr_dir)
sys.path.append(parent_dir)

from app.Unit_cell_composition.create_Hamiltonian import create_hamiltonian
from app.Print.print_matrix import save_to_file

def compare_files(filename, output_file):
    '''
    Function takes filename and filename2 and calculates merged_hamiltonian.
    It is then saved to file and the output_file is compared to filename.
    '''
    nrpts = np.loadtxt(filename, skiprows=2, max_rows=1)

    for line_num in range(3, int(np.ceil(nrpts/15))+4):
    #range from line witn nrpts to the end of integers
        with open(filename) as f1, open(output_file) as f2:
            lines1 = f1.readlines()
            lines2 = f2.readlines()

        # Normalize whitespace and split into tokens
        tokens1 = lines1[line_num - 1].split()
        tokens2 = lines2[line_num - 1].split()
        assert tokens1 == tokens2
        #if tokens1 != tokens2:
        #    print(f"Line {line_num} differs:")
        #    print("filename:", tokens1)
        #    print("output_file:", tokens2)
        #    exit()
    print("data in both files match")

test_case_loc = os.path.join(curr_dir, 'test_cases/')
filename = os.path.join(test_case_loc, 'wannier90_up_hr.dat')
filename2 = os.path.join(test_case_loc, 'wannier90_down_hr.dat')
filename3 = os.path.join(test_case_loc, 'wannier90_down_hr_broken_preambule.dat')
output_file = "output.dat"

import pytest


@pytest.mark.parametrize("f1, f2",[
    pytest.param(filename, filename,id="merging the same two files"),
    pytest.param(filename, filename2,id="marging the opposite spins"),
    pytest.param(filename, filename3,id="broken preambule",marks=pytest.mark.xfail)
    ])
def test_marge(f1,f2):
    assert os.path.isfile(f1)
    assert os.path.isfile(f2)
    merged = create_hamiltonian(f1,f2)
    save_to_file(merged, [f1,f2], output_file)
    compare_files(f1, output_file)
    assert True
    os.remove(output_file)

