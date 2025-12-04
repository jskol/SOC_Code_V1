import sys,os
import numpy as np
import time
from termcolor import colored


curr_dir=os.path.dirname(os.path.abspath(__file__)) #
parent_dir = os.path.dirname(curr_dir)
sys.path.append(parent_dir)
from app.Trash.create_hamiltonian_class_solution import create_hamiltonian as CH_JS
from app.Trash.create_hamiltonian import create_hamiltonian_original
from app.Unit_cell_composition.create_Hamiltonian import create_hamiltonian

test_case_loc=curr_dir+'/test_cases/'
filename=test_case_loc+'wannier90_up_hr.dat'

func_names=[create_hamiltonian_original,create_hamiltonian, CH_JS]

for func_name in func_names[1:]:
    start = time.time()
    data=func_name(filename)
    end = time.time()
    print(colored("%s: "%func_name.__name__, "green"), end - start, "sec")

data_ref=func_names[-2](filename) # create_hamiltonian_2

print("Runnning comparison ...")
for line1,line2 in zip(data,data_ref):
    l1=line1.to_Wannier()
    l2=line2.to_Wannier()
    for i in np.arange(len(l1)):
        if np.abs(l1[i]-l2[i]) > 1e-6:
            print(l1,"\n",l2)
            raise Exception("To approaches generate different results")