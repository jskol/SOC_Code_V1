import sys, os
import numpy as np

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

if __name__=="__main__":
    test_case_loc='test_cases/'
    file_name=test_case_loc+'wannier90_up_hr.dat'
    num_wann, nrpts = get_parameters(file_name)
    ## basic check of reading one file
    
    ''' All test cases moved to test_cases dir so this test is skipped
    for func in [timed_create_hamiltonian,timed_CH_JS]:
        read_class_no_name=func()
        if(len(read_class_no_name) == nrpts*(2*num_wann)**2):
            print("Reading Hamiltonian from the default name  using %s :Worked !"%func.__name__)
        else:
            exit("Issues with reading the default file using %s"%str(func))
    '''
    for func in [timed_create_hamiltonian,timed_CH_JS]:

        read_class=func(file_name)
        if(len(read_class) == nrpts*(2*num_wann)**2):
            print("Reading from single file for both spin channesl worked !")
        else:
            exit("Issues with reading from a single file using %s"%func.__name__)

    ## check purposefully broken file 
    for func in [timed_create_hamiltonian,timed_CH_JS]:
        try:
            read_class=func(file_name,test_case_loc+'wannier90_up_hr_broken.dat')
        except:
            print("Test Passed for %s-> Execption about the data missalignment thrown"%func.__name__)   
        else:
            exit("Data misaligment test Failed")

    ## Compare with the old way
    read_old=create_hamiltonian_original(file_name)
    for data_class,original in zip(read_class,read_old):
        data_temp=data_class.to_Wannier()
        for it in np.arange(len(original)):
            if( data_temp[it] != original[it]):
                exit("Test failed for %i in:\n"%it,data_temp,"\n",original)
    print("Comprison between the new and old approach ->Passed")