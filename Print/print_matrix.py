import numpy as np
from datetime import datetime
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Unit_cell_composition'))
from create_Hamiltonian import create_hamiltonian

def save_to_file(merged_hamiltonian, input_filename, output_filename="output.dat"):
    '''
    Function saving merged hamiltonian to file and adding parameters 
    on the beginning of file from input_filename
    '''
    header_lines = []
    now = datetime.now()
    header_lines.append(f"Created on {now.strftime('%d%b%Y')} at {now.strftime('%H:%M:%S')}")

    spin_degeneracy = 2
    num_wann_og = np.loadtxt(input_filename, skiprows=1, max_rows=1)
    num_wann_new = num_wann_og * spin_degeneracy
    header_lines.append(int(num_wann_new))

    nrpts = np.loadtxt(input_filename, skiprows=2, max_rows=1)
    header_lines.append(int(nrpts))

    with open(output_filename, "w") as f:
        f.write(header_lines[0] + "\n")             #date
        f.write(str(int(header_lines[1])) + "\n")   #num_wann
        f.write(str(int(header_lines[2])) + "\n")   #nrpts

        nrpt_header_lines = np.loadtxt(input_filename, skiprows=3, max_rows=int(np.ceil(nrpts/15))-1)
        for n_h_line in nrpt_header_lines:
            line = " ".join(str(int(x)) for x in n_h_line)
            f.write(line + "\n")
        nrpts_last_line = np.loadtxt(input_filename, skiprows=3+int(np.ceil(nrpts/15))-1, max_rows=1)
        f.write(" ".join(str(int(x)) for x in nrpts_last_line) + "\n")

        for sets in merged_hamiltonian:
            line = " ".join(map(str, sets.to_Wannier()))
            f.write(line + "\n")
