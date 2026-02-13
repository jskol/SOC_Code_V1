import numpy as np
import os,sys
app_loc=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(app_loc)
from Unit_cell_composition.create_Hamiltonian import create_hamiltonian
from Unit_cell_composition.read_win import composition_wrapper 

def generate_H_TB(win_file:str=None,*hr_files):
    """
    Generate matrix with only the 
    wannnierized TB parametes
    
    Needed parameters:
    win_file: path to the wannier90 parameters
    hf_files: paths to spin_up and spin_down wannierization results

    If no parametrs are given then attemting to use the default names
    """

    merged=create_hamiltonian(*hr_files)
    
    if win_file is None:
        win_default='wanner90.win'
        print(f'Trying default win-file name ({win_default})')
        if not os.path.exists(win_default):
            raise FileNotFoundError(f'{win_default} not found!')
        win_file=win_default
    else:
        if not os.path.exists(win_file):
            raise FileNotFoundError(f'{win_file} was not found, check where you are')
    
    comp=composition_wrapper(win_file)
    num_wann=comp.get_num_wann()
    spin_degeneracy=2
    num_spin_wann=spin_degeneracy*num_wann

    H_TB = np.zeros((num_spin_wann,num_spin_wann), dtype=complex) # Inititate proprely sized zero-matrix
    for sets in merged:
          if [sets.x,sets.y,sets.z] == [0,0,0]: 
            ind_1=sets.o1-1 # to python convention
            ind_2=sets.o2-1 # to python convension
            H_TB[ind_1][ind_2] =sets.hop

    return H_TB




if __name__=="__main__":
    win_file='tests/test_cases/wannier90.win'
    file_name='tests/test_cases/wannier90_up_hr.dat'
    file_name2='tests/test_cases/wannier90_down_hr.dat'
    res=generate_H_TB(win_file,file_name,file_name)
    print(res.shape)
    print(f'first 5 eigenvalues= {np.linalg.eigvalsh(res)[:5]}')
    
