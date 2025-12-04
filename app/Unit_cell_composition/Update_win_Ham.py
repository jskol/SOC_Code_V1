import sys,os
import numpy as np


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from SOC.create_H_SOC import generate_H_SOC

from Basis_reordering.Transfer_Matrix import Trasfer_Matrix_spinful

from Unit_cell_composition.create_Hamiltonian import create_hamiltonian
from Unit_cell_composition.read_params import read_params_wrapper

def update_merged(win_Hamiltonian_params_merged: list, H_SOC: np.array)-> None:
    '''
    takes win_Hamiltonian_params_merged- List of hamiltonian 
    parameters from merged win files and updates with H_SOC,
    REMEMBER TO HAVE THE SAME BASIS OF H_SOC AS WIN HAS !!!
    '''
    for sets in win_Hamiltonian_params_merged:
        if [sets.x,sets.y,sets.z] == [0,0,0]: 
            ind_1=sets.o1-1 # to python convention
            ind_2=sets.o2-1 # to python convension
            sets.hop += H_SOC[ind_1][ind_2]


def merged_with_SOC_wrapper(win_file=[], param_file='params',files_to_merge=[])->list:
    res=create_hamiltonian(*files_to_merge) # read hamiltonian elements from wannier90
    if len(win_file)==0:
        win=None
    elif len(win_file)==1:
        win=win_file[0]
    else:
        exit('Too many win-files passed')
    params=read_params_wrapper(param_file=param_file, wannier_in_file=win) # get parameters to H_SOC
    H_SOC= generate_H_SOC(win_file,params) # generate H_SOC (with optional local magnetic field)
    
    T_mat=Trasfer_Matrix_spinful(win_file) # generate transfer matrix
    # transfer H_SOC to proper basis
    H_SOC_2=T_mat@H_SOC@T_mat.T 

    update_merged(res,H_SOC_2) # update the r=0,0,0 hamiltonian matrix
    return res