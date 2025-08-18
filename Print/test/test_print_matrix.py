import numpy as np
import re
from termcolor import colored
from datetime import datetime
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'Unit_cell_composition'))
from create_Hamiltonian import create_hamiltonian

sys.path.append('..')
from print_matrix import save_to_file

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

        if tokens1 != tokens2:
            print(f"Line {line_num} differs:")
            print("filename:", tokens1)
            print("output_file:", tokens2)
            exit()
    print("data in both files match")

if __name__=="__main__":
    filename = '../../Unit_cell_composition/test/wannier90_up_hr.dat'
    filename2 = '../../Unit_cell_composition/test/wannier90_down_hr.dat'
    output_file = "output.dat"

    merged = create_hamiltonian(filename, filename2)
    save_to_file(merged, filename, output_file)

    compare_files(filename, output_file)
