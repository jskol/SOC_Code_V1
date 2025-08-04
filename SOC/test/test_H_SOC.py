import numpy as np
import sys
from termcolor import colored

sys.path.append('../../Angular_momentum')
sys.path.append('../../Unit_cell_composition')
sys.path.append('..')
from angular_momentum import AngularMomentum
from create_H_SOC import generate_H_SOC
from read_win import get_projections, get_composition, composition_wrapper

def check_difference(mat, mat2, size, ref):
    mat[np.absolute(mat)<1e-6]=0
    mat2[np.absolute(mat2)<1e-6]=0
    if ~np.any(mat - mat2[ref:ref+size,ref:ref+size]):
        print("Test : ", colored("Passed", 'green'))
    else:
        exit("Test : Failed")

if __name__=="__main__":
    S_pauli=AngularMomentum(0.5)
    S=AngularMomentum(0)
    P=AngularMomentum(1)
    D=AngularMomentum(2)
    P.to_Cartesian(['px','py','pz'])
    D.to_Cartesian(['dxy', 'dyz', 'dxz', 'dx2-y2', 'dz2'])

    H_SOC = generate_H_SOC("../../Unit_cell_composition/test/wannier90_V3.win")

    H_SOC_DS = np.kron(D.x(),S_pauli.x()) + np.kron(D.y(),S_pauli.y())+ np.kron(D.z(),S_pauli.z())
    H_SOC_PS = np.kron(P.x(),S_pauli.x()) + np.kron(P.y(),S_pauli.y())+ np.kron(P.z(),S_pauli.z())
    H_SOC_SS = np.kron(S.x(),S_pauli.x()) + np.kron(S.y(),S_pauli.y())+ np.kron(S.z(),S_pauli.z())

    H_SOC_SS = np.array(H_SOC_SS)
    H_SOC_PS = np.array(H_SOC_PS)
    H_SOC_DS = np.array(H_SOC_DS)
    H_SOC = np.array(H_SOC)

    print(colored("S ORBITALS:", 'cyan'))
    ref = 0
    size = 2 # S orbitals
    ### S orbitals ###
    for _ in np.arange(4):
        check_difference(H_SOC_SS, H_SOC, size, ref)
        ref += size
    for _ in np.arange(4):
        '''
        P orbitals
        '''
        size = 6
        print(colored("P ORBITALS:", 'cyan'))

        ### P orbitals ###
        check_difference(H_SOC_PS, H_SOC, size, ref)
        ref += size
        '''
        D orbitals
        '''
        print(colored("D ORBITALS:", 'cyan'))
        size = 10

        ### D orbitals ###
        check_difference(H_SOC_DS, H_SOC, size, ref)
        ref += size

