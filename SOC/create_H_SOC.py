import sys
import re
import numpy as np
from termcolor import colored

sys.path.append('../Angular_momentum')
from ladder_operator import angular_momentum_matrices,get_L_degeneracy, update_angular_momentum
from angular_momentum import AngularMomentum

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

    S_mat_set = angular_momentum_matrices(0.5)
    spin_degeneracy=S_mat_set[0].shape[0]
    assert spin_degeneracy == get_L_degeneracy(0.5)
    print("S = \n", S_mat_set)

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

	#list_of_orbitals = []
    ''''
    We are looking for a matrix with a strucutre
    block diagonal
    each block is for each atom
    inside each block
    another block diagonal matrix
    for each L-subspace
    '''
    ref_p = 0 # ref point for H_SOC matrix
    for atom in comp.composition: # iterate over atoms
        print(atom.print_details())
        
        temp_list_of_orbitals = atom.split_orbitals_by_L()

        print("divided into subpaces:")
        #we go through subspaces of ONE atom
        sub_ref_p = 0 # ref point for matrix of one atom
        sub_mat_size = 2 * sum(len(sublist) for sublist in temp_list_of_orbitals)
        sub_matrix = np.zeros((sub_mat_size, sub_mat_size), dtype=complex) 
        #creating matrix of zeros for one atom
        print(colored("size(sub_matrix) = ", 'blue'), np.shape(sub_matrix))
        for it, subspace in enumerate(temp_list_of_orbitals):
            print("#:",subspace)
            first_letter=subspace[0][0]
            if (first_letter == 's'):
                l = 0
                #print("orbital S")
            elif (first_letter == 'p'):
                l = 1
                #print("orbital P")
            elif (first_letter == 'd'):
                l = 2
                #print("orbital D")
            else:
                #print("Orbital unavailable - orb = ", subspace[0])
                raise Exception("Orbital unavailable!")

            L_op_set = AngularMomentum(l)
            L_op_set.to_Cartesian(subspace)

            sub_sub_matrix = np.zeros((2*len(subspace), 2*len(subspace)), dtype=complex)
            for it, direction in enumerate(['x', 'y', 'z']):
                sub_sub_matrix += np.kron(L_op_set.basis[direction], S_mat_set[it])
            ## we've created matrix for a particular orbital
            print(colored("size(sub_sub_matrix) = ", 'yellow'), np.shape(sub_sub_matrix))

            for i in np.arange(2*len(subspace)):
                for j in np.arange(2*len(subspace)):
                    sub_matrix[sub_ref_p + i][sub_ref_p + j] = sub_sub_matrix[i][j]
            #saving sub_sub_matrix into sub_matrix
            sub_ref_p += 2*len(subspace) #incrementing reference point of sub_matrix

            print(colored("sub_ref_p = ", 'green'), sub_ref_p)

        for i in np.arange(sub_mat_size):
            for j in np.arange(sub_mat_size):
                H_SOC[ref_p + i][ref_p + i] = sub_matrix[i][j]
        ref_p += sub_mat_size
            

        # for each L-type
        # 1) Generate L operator set (x,y,z)
        # 2) Transform this oper set to Cartesian (using user defined 
		# 	 subset and order of orbitals/projectors)
        #    Hint: Use   AngularMomentum.to_Cartesian(subspace)
        # 3) Generate H_SOC 

    return H_SOC


if __name__=="__main__":
        
        #files_to_test_on=['mnte.win','wannier90_V2.win','wannier90_V3.win']
        #H_SOC = generate_H_SOC("../Unit_cell_composition/test/"+file_name)
        H_SOC = generate_H_SOC("../Unit_cell_composition/test/wannier90_V3.win")
        print("np.shape(H_SOC) = \n", np.shape(H_SOC))
        # with np.printoptions(threshold=sys.maxsize):
        #     print("H_SOC = \n", H_SOC)