'''
1) Sprawdzić czy warunek na r=0,0,0 działa
2) Dla jakiejś małej macierzy i zmyślonego H_SOC sprawidzić czy update działa
    -) wydrukuj H dla r=0,0,0
    -) H_SOC=1e6*np.eye((2*n_wann,2*n_wann))
    -) zrob update H_SOC'iem
    -) print macierz H dla r=0,0,0 (w szczególności diagonala czy jest rzędu 1e6 )
'''
import sys,os
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..','SOC'))
from create_H_SOC import generate_H_SOC

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..','Basis_reordering'))
from Transfer_Matrix import Trasfer_Matrix_spinful

sys.path.append(os.path.join(os.path.dirname(__file__), '..','..', 'Unit_cell_composition'))
from create_Hamiltonian import create_hamiltonian
from read_params import read_params_wrapper
from Update_win_Ham import update_merged

if __name__=="__main__":
    H_init=create_hamiltonian('wannier90_hr.dat')
    n_wann=32
    H=1e6*np.eye(n_wann,dtype=np.complex128)

    H_prev=np.zeros((n_wann,n_wann),dtype=np.complex128)
    H_after=np.zeros((n_wann,n_wann),dtype=np.complex128)
    for sets in H_init:
        if [sets.x,sets.y,sets.z] == [0,0,0]: # TODO: Test if this condition works
            H_prev[sets.o1-1][sets.o2-1] = sets.hop

    update_merged(H_init,H)

    for sets in H_init:
        if [sets.x,sets.y,sets.z] == [0,0,0]: # TODO: Test if this condition works
            H_after[sets.o1-1][sets.o2-1]= sets.hop

    for diag in np.arange(n_wann):
        print("Before= ", H_prev[diag][diag], " and After= ", H_after[diag][diag])