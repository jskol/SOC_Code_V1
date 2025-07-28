import sys
import re
import numpy as np

#sys.path.append('../')
sys.path.append('../Angular_momentum')
from ladder_operator import angular_momentum_matrices,get_L_degeneracy, update_angular_momentum

sys.path.append('../Unit_cell_composition')
from create_hamiltonian_time import create_hamiltonian, get_parameters
from UnitCell import UnitCell, Atom
from read_win import get_projections, get_composition, composition_wrapper

def generate_H_SOC(*filenames):
	
    if (len(filenames) == 1):	#if we pas 1 file, both are the same
        spin_up_file = filenames[0]
        spin_down_file = filenames[0]
    elif (len(filenames) == 2):
        spin_up_file = filenames[0]
        spin_down_file = filenames[1]
    elif(len(filenames)==0):
        spin_up_file ="wannier90.win"
        spin_down_file ="wannier90.win"	
    else:						#in other cases we have error
        print("error")
        exit(1)
    print("s_up = ", spin_up_file)		###
    print("s_down = ", spin_down_file)	###

    #spin_degeneracy = get_L_degeneracy(0.5)
    # num_wann, nrpts = get_parameters(spin_up_file)
    # print("num_wann, nrpts = ", num_wann, ", ", nrpts)	###

    S = angular_momentum_matrices(0.5)
    spin_degeneracy=S[0].shape[0]
    assert spin_degeneracy == get_L_degeneracy(0.5)
    print("S = \n", S)

    comp = {}
    comp = composition_wrapper(spin_up_file)
    comp.print_composition()

    #f=open(filename,'r')

    ### Testing calculating number of Wanniers used in the projection

    num_wann=comp.get_num_wann()
    #assert num_wann == 16
    num_spin_wann=spin_degeneracy*num_wann

    H_SOC = np.zeros((num_spin_wann,num_spin_wann), dtype=complex)
    print("H_SOC = \n", H_SOC)
    print("np.shape(H_SOC) = ", np.shape(H_SOC))

    ref_point=0
	#list_of_orbitals = []
    ''''
    We are looking for a matrix with a strucutre
    block diagonal
    each block is for each atom
    inside each block
    another block diagonal matrix
    for each L-subspace
    '''

    for atom in comp.composition: # iterate over atoms
        print(atom.print_details())
        #print("atom = \n", atom)

        #temp_orbitals=atom.orbitals
        
        temp_list_of_orbitals = []
        prev_letter=atom.orbitals[0][0]
        temp_list=[]
        for orb in atom.orbitals:
            curr_letter=orb[0]
            if curr_letter == prev_letter:
                temp_list.append(orb)
            else:
                temp_list_of_orbitals.append(temp_list)
                temp_list=[]
            prev_letter=curr_letter 
        
        temp_list_of_orbitals.append(temp_list) # Always ends with a non-empty temp_list

        print("divided into subpaces")
        for it,subspace in enumerate(temp_list_of_orbitals):
            print("#%i:"%it ,subspace)

        # for each L-type
        # 1) Generate L operator set (x,y,z)
        # 2) Transform this oper set to Cartesian (using user defined subset and order of orbitals/projectors)
        #    Hint: Use   AngularMomentum.to_Cartesian(subspace)
        # 3) Generate H_SOC 
        
        
        #	temp_list_of_orbitals.append(orb)
        '''
            if (orb == 's'):
                list_of_orbitals.append(orb)
            elif (orb[0] == 'p'):
                
            elif (orb[0] == 'd'):
                l = 2
                print("l == 2")
            else:
                raise Exception("Orbital unavailable!")
            
            
            #L_op_set = angular_momentum_matrices(l)
            print("L_op_set =\n", L_op_set)

            temp_SOC_mat=np.zeros((L_op_set[0].shape[0]*S[0].shape[0],L_op_set[0].shape[0]*S[0].shape[0]),dtype=complex)

            ## Generate SOC for one atom
            for direction in np.arange(3):
                temp_SOC_mat += np.kron(L_op_set[direction],S[direction])
            
            ## Input SOC of this atom into the full SOC Hamiltonian
            for i in np.arange(temp_SOC_mat.shape[0]):
                for j in np.arange(temp_SOC_mat.shape[1]):
                    H_SOC[ref_point+i][ref_point+j] = temp_SOC_mat[i][j]
            '''
        #list_of_orbitals.append(temp_list_of_orbitals)
        #ref_point += temp_SOC_mat.shape[0]
            
    #print("temp_list_of_orbitals = \n", list_of_orbitals)
        

    #return H_SOC


if __name__=="__main__":
        
        #files_to_test_on=['mnte.win','wannier90_V2.win','wannier90_V3.win']
        #H_SOC = generate_H_SOC("../Unit_cell_composition/test/"+file_name)
        H_SOC = generate_H_SOC("../Unit_cell_composition/test/wannier90_V3.win")
        print("np.shape(H_SOC) = \n", np.shape(H_SOC))
    # with np.printoptions(threshold=sys.maxsize):
    # 	print("H_SOC = \n", H_SOC)