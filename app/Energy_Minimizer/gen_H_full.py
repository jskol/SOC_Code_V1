import numpy as np

import os,sys
app_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(app_dir)


from Energy_Minimizer.gen_H_TB import generate_H_TB 
# To get tight-binding hamiltonia

from SOC.create_H_SOC import generate_H_SOC 
# to get SOC + local magnetic field

from Basis_reordering.Transfer_Matrix import Trasfer_Matrix_spinful
 # helper function to transorm natural basis for SOC to wannier (orbital-major) orgering

from Unit_cell_composition.read_params import read_params_wrapper
#helper to read model parameters from a file

def generate_H_Full(win_file:str=None,param_file:str='params',*hr_files)->np.ndarray:
    """
    Docstring for gen_H_Full
    
    :param win_file (str): win-file containing all details of wannierization
    :param param_file: param file containing parameters for model  H_SOC
    :param hr_files(optional): path to hoppings from wannierization for each spin channel (up &down)
        if nothing is passed then code attempts to read default name
        if one passed code assumes a spin-symmetric hopping matrix  
    """
    #Sanity checks
    if param_file=='params' and not os.path.exists('params'):
        raise FileNotFoundError('Missing parameter file')
    elif param_file=='params':
        print('Using default param file')
        param_file='params'

    H=generate_H_TB(win_file,*hr_files)
    
    params=read_params_wrapper(param_file=param_file, wannier_in_file=win_file) # get parameters to H_SOC
    H_SOC= generate_H_SOC([win_file],params)   # generate H_SOC (with optional local magnetic field)
    T_mat=Trasfer_Matrix_spinful([win_file])   # generate transfer matrix
    H_SOC_2=T_mat@H_SOC@T_mat.T              # transfer H_SOC to proper basis (orbital-major)

    return H+H_SOC_2




if __name__=="__main__":
    win_file='tests/test_cases/wannier90.win'
    file_name='tests/test_cases/wannier90_up_hr.dat'
    file_name2='tests/test_cases/wannier90_down_hr.dat' 
    param_name='tests/test_cases/params'
    res=generate_H_Full(win_file,param_name,file_name,file_name)
    print(res.shape)
    print(f'first 5 eigenvalues= {np.linalg.eigvalsh(res)[:5]}')