import sys
import re
import numpy as np
from termcolor import colored


sys.path.append('../Angular_momentum')
from angular_momentum import AngularMomentum

sys.path.append('../Unit_cell_composition')
from read_win import composition_wrapper
from UnitCell import get_L_from_orbitals_set_name

def generate_H_SOC_V2(*filenames):
	
    if(len(filenames) ==0):
        win_file='wanner90.win'
    elif (len(filenames) == 1):	#if we pas 1 file, both are the same
        win_file = filenames[0]
    else:						#in other cases we have error
        print("error")
        exit(1)
    print("Projections read from: ", win_file)	###

    S_Pauli = AngularMomentum(0.5)
    spin_degeneracy=S_Pauli.x().shape[0]


    comp = composition_wrapper(win_file)
    num_wann=comp.get_num_wann()
    num_spin_wann=spin_degeneracy*num_wann

    H_SOC = np.zeros((num_spin_wann,num_spin_wann), dtype=complex)

    ref_point=0
    for atom in comp: #Iterating over each Atom in the Unit cell
        
        split_orb=atom.split_orbitals_by_L()
        for l_subspace in split_orb:
            
            l=get_L_from_orbitals_set_name(l_subspace) #Please use this function to get "l"
            L_op_set = AngularMomentum(l)
            L_op_set.to_Cartesian(l_subspace)

            H_SOC_in_L_subspace=np.kron(L_op_set.x(),S_Pauli.x())+np.kron(L_op_set.y(),S_Pauli.y())+np.kron(L_op_set.z(),S_Pauli.z())
            for i in np.arange(H_SOC_in_L_subspace.shape[0]):            
                for j in np.arange(H_SOC_in_L_subspace.shape[1]):
                    H_SOC[ref_point+i,ref_point+j]= H_SOC_in_L_subspace[i,j]
            ref_point += spin_degeneracy*len(l_subspace)
    
    return H_SOC