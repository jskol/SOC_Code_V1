import sys
import numpy as np
import time
from termcolor import colored
sys.path.append('..')
from create_hamiltonian_class_solution import create_hamiltonian as CH_JS
from create_hamiltonian_time import create_hamiltonian_original,create_hamiltonian, create_hamiltonian_2

filename='wannier90_up_hr.dat'

start = time.time()
create_hamiltonian_original(filename)
end = time.time()
print(colored("original: ", "green"), end - start, "sec")

start = time.time()
create_hamiltonian(filename)
end = time.time()
print(colored("KJ: ", "green"), end - start, "sec")

start = time.time()
CH_JS(filename)
end = time.time()
print(colored("JS: ", "green"), end - start, "sec")