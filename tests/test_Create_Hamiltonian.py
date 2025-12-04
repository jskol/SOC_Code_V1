import sys, os
import numpy as np
import pytest

sys.path.append('../app/Misc')
from timing import timing

sys.path.append( '../app/Trash')
from create_hamiltonian_class_solution import create_hamiltonian as CH_JS
from create_hamiltonian import create_hamiltonian_original

sys.path.append('../app/Unit_cell_composition')
from create_Hamiltonian import create_hamiltonian,get_parameters

@timing
def timed_create_hamiltonian(*filenames):
    res=create_hamiltonian(*filenames)
    return res
@timing
def timed_create_hamiltonian_original(*filenames):
    res=create_hamiltonian_original(*filenames)
    return res

@timing
def timed_CH_JS(*filenames):
    res=CH_JS(*filenames)
    return res

test_case_loc='test_cases/'
#file_name=test_case_loc+'wannier90_up_hr.dat'
## basic check of reading one file
#target_num_lines=nrpts*(2*num_wann)**2
@pytest.mark.parametrize("func, file_name", [
    (timed_create_hamiltonian,'wannier90_up_hr.dat'),
        (timed_CH_JS,'wannier90_up_hr.dat'),
        pytest.param(timed_create_hamiltonian,'wannier90_up_hr.dat_non_existing',marks=pytest.mark.xfail),
        pytest.param(timed_create_hamiltonian,'wannier90_up_hr_broken.dat',marks=pytest.mark.xfail)
        
    ])
def test_read_file(func,file_name):
    file_path=test_case_loc+file_name
    num_wann, nrpts = get_parameters(file_path)
    target_num_lines=nrpts*(2*num_wann)**2
    read_class=func(file_path)
    assert len(read_class) == target_num_lines

@pytest.mark.parametrize("file_name", ['wannier90_up_hr.dat'])
def test_new_vs_old(file_name):
    file_path=test_case_loc+file_name
    ## Compare with the old way
    read_new=create_hamiltonian(file_path)
    read_old=create_hamiltonian_original(file_path)
    for data_class,original in zip(read_new,read_old):
        data_temp=data_class.to_Wannier()
        for it in np.arange(len(original)):
            assert data_temp[it] == original[it]
