import sys
import numpy as np
import time
from termcolor import colored
sys.path.append('..')
from create_hamiltonian_class_solution import create_hamiltonian as CH_JS
from create_hamiltonian_time import create_hamiltonian_original,create_hamiltonian, create_hamiltonian_2

filename='wannier90_up_hr.dat'

func_names=[create_hamiltonian_original,create_hamiltonian, create_hamiltonian_2, CH_JS]

for func_name in func_names[1:]:
    start = time.time()
    data=func_name(filename)
    end = time.time()
    print(colored("%s: "%func_name.__name__, "green"), end - start, "sec")

data_ref=func_names[-2](filename) # create_hamiltonian_2


for line1,line2 in zip(data,data_ref):
    l1=line1.to_Wannier()
    l2=line2.to_Wannier()
    for i in np.arange(len(l1)):
        if np.abs(l1[i]-l2[i]) > 1e-6:
            print(l1,"\n",l2)
            raise Exception("To approaches generate different results")


