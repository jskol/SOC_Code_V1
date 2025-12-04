import numpy as np
import sys, os
from termcolor import colored
import time

curr_dir=os.path.dirname(os.path.abspath(__file__)) #
parent_dir = os.path.dirname(curr_dir)
sys.path.append(parent_dir)


from app.Misc.timing import timing
from app.Angular_momentum.angular_momentum import AngularMomentum
from app.Unit_cell_composition.UnitCell import get_L_from_orbitals_set_name
from app.Unit_cell_composition.read_win import composition_wrapper
from app.Unit_cell_composition.read_params import read_params, immerse_params_in_composition
from app.SOC.create_H_SOC import generate_H_SOC

@timing
def timed_generate_H_SOC(*filenames):
    res=generate_H_SOC(*filenames)
    return res

from app.Trash.create_H_SOC_V2 import generate_H_SOC_V2
@timing
def timed_generate_H_SOC_V2(*filenames):
    res=generate_H_SOC_V2(*filenames)
    return res

def check_difference(mat, mat2, size, ref):
    mat[np.absolute(mat)<1e-6] = 0
    mat2[np.absolute(mat2)<1e-6] = 0
    if ~np.any(mat - mat2):
        print("Test : ", colored("Passed", 'green'))
    else:
        exit("Test : Failed")

def print_orbital(subspace):
    first_letter=subspace[0][0]
    if (first_letter == 's'):
        print(colored("S orbital", 'red'))
    elif (first_letter == 'p'):
        print(colored("P orbital", 'blue'))
    elif (first_letter == 'd'):
        print(colored("D orbital", 'yellow'))
    else:
        raise Exception("Orbital unavailable!")

def calculate_H_SOC_ref(subspace, S_pauli):
    L_set = AngularMomentum(get_L_from_orbitals_set_name(subspace))
    L_set.to_Cartesian(subspace)
    H_SOC_ref = np.kron(L_set.x(),S_pauli.x()) + np.kron(L_set.y(),S_pauli.y()) + np.kron(L_set.z(),S_pauli.z())
    return H_SOC_ref

if __name__=="__main__":

    test_case_loc='test_cases/'
    filename = test_case_loc+"wannier90_2_atoms.win"

    param_file = test_case_loc+"params_2_atoms"
    res=read_params(param_file)
    comp=composition_wrapper(filename)
    res2=immerse_params_in_composition(res,comp)

    H_SOC = generate_H_SOC([filename], params=res2)
    print("shape(H_SOC) = ", np.shape(H_SOC))
    #H_SOC[H_SOC < 1e-3] = 0
    np.set_printoptions(suppress=True)
    print("H_SOC = \n", H_SOC)
    
    print("\nH_SOC(Upper-left) = \n", np.diag(H_SOC[:6,:6]))
    print("\nH_SOC(Lower-right) = \n", np.diag(H_SOC[6:,6:]))
    
    exit()
    print(colored("spin up", 'red'), "=\n", H_SOC[::2, ::2])
    print(colored("spin down", 'red'), "=\n", H_SOC[1::2, 1::2])

    print(colored("SOC up/down", 'red'), "=\n", H_SOC[::2, 1::2])
    print(colored("SOC down/up", 'red'), "=\n", H_SOC[1::2, ::2])
