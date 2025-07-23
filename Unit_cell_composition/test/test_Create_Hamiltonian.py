import sys
import numpy as np
sys.path.append('..')
sys.path.append('../../Misc')
from create_hamiltonian_class_solution import create_hamiltonian,get_parameters
from create_hamiltonian import create_hamiltonian_original
from timing import timing

@timing
def timed_create_hamiltonian(*filenames):
    res=create_hamiltonian(*filenames)
    return res
@timing
def timed_create_hamiltonian_original(*filenames):
    res=create_hamiltonian_original(*filenames)
    return res


if __name__=="__main__":
    file_name='wannier90_up_hr.dat'
    num_wann, nrpts = get_parameters(file_name)
    ## basic check of reading one file
    read_class_no_name=timed_create_hamiltonian()
    if(len(read_class_no_name) == nrpts*(2*num_wann)**2):
        print("Reading Hamiltonian from the default name worked !")
    else:
        exit("Issues with reading the defule file")
    read_class=timed_create_hamiltonian(file_name)
    if(len(read_class) == nrpts*(2*num_wann)**2):
        print("Reading from single file for both spin channesl worked !")
    else:
        exit("Issues with reading from a single file")

    ## check purposefully borken file 
    try:
        read_class=create_hamiltonian(file_name,'wannier90_up_hr_broken.dat')
    except:
        print("Test Passed-> Execption about the data missalignment thrown")   
   

    ## Compare with the old way
    read_old=create_hamiltonian_original(file_name)
    for data_class,original in zip(read_class,read_old):
        data_temp=data_class.to_Wannier()
        for it in np.arange(len(original)):
            if( data_temp[it] != original[it]):
                exit("Test failed for %i in:\n"%it,data_temp,"\n",original)
    print("Comprison between the new and old approach ->Passed")