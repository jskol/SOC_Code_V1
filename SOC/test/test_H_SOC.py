import numpy as np
import sys
from termcolor import colored
import time


sys.path.append('../../Misc')
from timing import timing

sys.path.append('../../Angular_momentum')
from angular_momentum import AngularMomentum

sys.path.append('../../Unit_cell_composition')
from UnitCell import get_L_from_orbitals_set_name
from read_win import get_projections, get_composition, composition_wrapper

sys.path.append('..')
from create_H_SOC import generate_H_SOC_old, generate_H_SOC
@timing
def timed_generate_H_SOC_old(*filenames):
    res=generate_H_SOC_old(*filenames)
    return res

@timing
def timed_generate_H_SOC(*filenames):
    res=generate_H_SOC(*filenames)
    return res

sys.path.append('../../Trash')
from create_H_SOC_V2 import generate_H_SOC_V2
@timing
def timed_generate_H_SOC_V2(*filenames):
    res=generate_H_SOC_V2(*filenames)
    return res


def check_difference(mat, mat2, size, ref):
    mat[np.absolute(mat)<1e-6] = 0
    mat2[np.absolute(mat2)<1e-6] = 0
    diff_mat = mat - mat2[ref:ref+size,ref:ref+size]
    diff_mat[np.absolute(diff_mat)<1e-6] = 0
    if ~np.any(diff_mat):
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
    S_pauli=AngularMomentum(0.5)
    spin_degeneracy = S_pauli.x().shape[0]

    
    files = ["../../Unit_cell_composition/test/wannier90_V2.win"
    ,"../../Unit_cell_composition/test/wannier90_V3.win"
    ,"../../Unit_cell_composition/test/wannier90_V4.win"
    ]
    for filename in files:
        
        funcs=[timed_generate_H_SOC_V2,timed_generate_H_SOC_old,timed_generate_H_SOC]
        for fun in funcs:
            H_SOC = fun(filename)
        exit()
        
        comp = composition_wrapper(filename)

        ref_p = 0
        for atom in comp:
            split_orb = atom.split_orbitals_by_L()
            for subspace in split_orb:
                print_orbital(subspace)
                size = spin_degeneracy*len(subspace)
                H_SOC_ref = calculate_H_SOC_ref(subspace, S_pauli)
                check_difference(H_SOC_ref, H_SOC, size, ref_p)
                ref_p += size
