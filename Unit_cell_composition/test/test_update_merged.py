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
from Update_win_Ham import update_merged,merged_with_SOC_wrapper


if __name__=="__main__":
    test_case_loc='../../test_cases/'
    H_init=create_hamiltonian(test_case_loc+'wannier90_hr.dat')
    n_wann=32 # by-hand

    ### Simple test with uniform huge Magnetic field ###
    
    M_f=1e6
    print("\n Testing spin H_loc update with large (%f) chemical potnetial "%M_f)
    H=M_f*np.eye(n_wann,dtype=np.complex128)
    H_prev=np.zeros((n_wann,n_wann),dtype=np.complex128)
    H_after=np.zeros((n_wann,n_wann),dtype=np.complex128)
    for sets in H_init:
        if [sets.x,sets.y,sets.z] == [0,0,0]:
            H_prev[sets.o1-1][sets.o2-1] = sets.hop

    update_merged(H_init,H)

    for sets in H_init:
        if [sets.x,sets.y,sets.z] == [0,0,0]: 
            H_after[sets.o1-1][sets.o2-1]= sets.hop
    M_f_diff= H_prev.diagonal()-H_after.diagonal() + M_f
    M_f_diff[np.absolute(M_f_diff)<1e-6]=0
    print("Testing local potential (chemical potential ): ", 'Passed' if ~np.any(M_f_diff) else 'Failed ')

    


    ### Testing with atom and orbital-selective magnetic field
    print("\nTesting with orbial and atom -selective magnetic field\n")
    
    update_merged(H_init,-H) # undo the magnetic-field H
    win_file= test_case_loc+'wannier90.win'
    params_file= test_case_loc+'params_merge_test'
    params= read_params_wrapper(param_file=params_file,wannier_in_file= test_case_loc+'wannier90.win')
    print("Parameters read from param file")
    params_names=['magnetic-field','SOC']
    for prop in params_names:
        for mag in params[prop]:
            print(mag)
    H_SOC = generate_H_SOC([ test_case_loc+'wannier90.win'], params=params)
    print("The diagonal of H_SOC in atom-wise basis: ", H_SOC.diagonal())
    T_mat=Trasfer_Matrix_spinful([ test_case_loc+'wannier90.win']) # generate transfer matrix
    # transfer H_SOC to proper basis
    H_SOC_2=T_mat@H_SOC@T_mat.T
    print("The diagonal of H_SOC in orbital-wise basis: ", H_SOC_2.diagonal()) 
    update_merged(H_init,H_SOC_2)
    for sets in H_init:
        if [sets.x,sets.y,sets.z] == [0,0,0]: 
            H_after[sets.o1-1][sets.o2-1]= sets.hop
    

    # Testing wrapper 
    print("\n Testing the wrapper \n")
    update_merged(H_init,-H_SOC_2) # undo the magnetic-field H
    H_init_wrap = merged_with_SOC_wrapper(win_file=[win_file],param_file= test_case_loc+'params_merge_test',files_to_merge=[ test_case_loc+'wannier90_hr.dat'])
    H_wrap=np.zeros((n_wann,n_wann),dtype=np.complex128)
    for sets in H_init_wrap:
        if [sets.x,sets.y,sets.z] == [0,0,0]: 
            H_wrap[sets.o1-1][sets.o2-1]= sets.hop

    diff=H_after.diagonal()-H_wrap.diagonal()
    diff[np.absolute(diff)<1e-6] =0
    print("Wrapper gives the same results as the step-by-step procedure: ", ~np.any(diff))