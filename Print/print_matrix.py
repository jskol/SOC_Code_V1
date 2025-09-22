import numpy as np
from datetime import datetime
import csv

def input_file_preamble_check(n: int, m: int, input_filename=[])->bool:
    print(" len of input: ", len(input_filename))
    print(input_filename)
    if len(input_filename)==1:
        return True
    elif len(input_filename)==2:
        file1, file2 = input_filename
        all_match = True

        with open(file1) as f1, open(file2) as f2:
            for row_num, (line1, line2) in enumerate(zip(f1, f2), start=1):
                row1 = line1.split()
                row2 = line2.split()
                if row1[n:m+1] != row2[n:m+1]:
                    print(f"Row {row_num} mismatch:")
                    print(f"  {file1}: {row1[n:m+1]}")
                    print(f"  {file2}: {row2[n:m+1]}")
                    all_match = False
        print("return = ", all_match)
        return all_match
    else:
        
        return False

def save_to_file(merged_hamiltonian, input_filename=[], output_filename: str ="output.dat"):
    '''
    Function saving merged hamiltonian to file and adding parameters 
    on the beginning of file from input_filename
    '''
    nrpts = np.loadtxt(input_filename, skiprows=2, max_rows=1)
    print( "Preabule check: " ,input_file_preamble_check(3-1, 3+int(np.ceil(nrpts/15))-1, input_filename))
 
    #     raise Exception("Two hr files mismatch")
    # exit(0)

    header_lines = []
    now = datetime.now()
    header_lines.append(f"Created on {now.strftime('%d%b%Y')} at {now.strftime('%H:%M:%S')}")

    spin_degeneracy = 2
    num_wann_og = np.loadtxt(input_filename, skiprows=1, max_rows=1)
    num_wann_new = num_wann_og * spin_degeneracy
    header_lines.append(int(num_wann_new))

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
