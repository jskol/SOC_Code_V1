import numpy as np
import sys
from termcolor import colored

sys.path.append('../../Angular_momentum')
sys.path.append('../../Unit_cell_composition')
sys.path.append('..')
from angular_momentum import AngularMomentum
from create_H_SOC import generate_H_SOC
from read_win import get_projections, get_composition, composition_wrapper
from UnitCell import get_L_from_orbitals_set_name

def check_difference(mat, mat2, size, ref):
    mat[np.absolute(mat)<1e-6]=0
    mat2[np.absolute(mat2)<1e-6]=0
    if ~np.any(mat - mat2[ref:ref+size,ref:ref+size]):
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
    S=AngularMomentum(0)
    P=AngularMomentum(1)
    D=AngularMomentum(2)
    P.to_Cartesian(['px','py','pz'])
    D.to_Cartesian(['dxy', 'dyz', 'dxz', 'dx2-y2', 'dz2'])

    spin_degeneracy = 2

    filename = "../../Unit_cell_composition/test/wannier90_V3.win"
    H_SOC = generate_H_SOC(filename)
    ## TODO:
    # 1) Introduce compostion and atomatize testing
    # 2) each type of orbital printed in differentcolor
    # 3) test on two different *.win files

    H_SOC_DS = np.kron(D.x(),S_pauli.x()) + np.kron(D.y(),S_pauli.y())+ np.kron(D.z(),S_pauli.z())
    H_SOC_PS = np.kron(P.x(),S_pauli.x()) + np.kron(P.y(),S_pauli.y())+ np.kron(P.z(),S_pauli.z())
    H_SOC_SS = np.kron(S.x(),S_pauli.x()) + np.kron(S.y(),S_pauli.y())+ np.kron(S.z(),S_pauli.z())

    H_SOC_SS = np.array(H_SOC_SS)
    H_SOC_PS = np.array(H_SOC_PS)
    H_SOC_DS = np.array(H_SOC_DS)
    H_SOC = np.array(H_SOC)

    comp = composition_wrapper(filename)

    ref_p = 0
    for atom in comp:
        split_orb = atom.split_orbitals_by_L()
        for subspace in split_orb:
            print_orbital(subspace)
            size = spin_degeneracy*len(subspace)

            #for elem in len(subspace):
            H_SOC_ref = calculate_H_SOC_ref(subspace, S_pauli)
            check_difference(H_SOC_ref, H_SOC, size, ref_p)
        ref_p += size
