import sys
import re
import numpy as np
from termcolor import colored

sys.path.append('../Angular_momentum')
from ladder_operator import angular_momentum_matrices,get_L_degeneracy, update_angular_momentum
from angular_momentum import AngularMomentum

sys.path.append('../Unit_cell_composition')
from create_hamiltonian_time import create_hamiltonian, get_parameters
from UnitCell import UnitCell, Atom, get_L_from_orbitals_set_name
from read_win import get_projections, get_composition, composition_wrapper

def generate_H_SOC(*filenames):
    if(len(filenames) ==0):
        win_file='wanner90.win'
    elif (len(filenames) == 1):	#if we pas 1 file, both are the same
        win_file = filenames[0]
    else:						#in other cases we have error
        print("error")
        exit(1)

    S_Pauli = AngularMomentum(0.5)
    spin_degeneracy = S_Pauli.x().shape[0]

    comp = {}
    comp = composition_wrapper(win_file)
    comp.print_composition()

    num_wann=comp.get_num_wann()
    num_spin_wann=spin_degeneracy*num_wann

    H_SOC = np.zeros((num_spin_wann,num_spin_wann), dtype=complex)

    ref_point = 0 # ref point for H_SOC matrix
    for atom in comp.composition: # Iterating over each Atom in the Unit cell
        split_orb=atom.split_orbitals_by_L()
        for l_subspace in split_orb:

            l=get_L_from_orbitals_set_name(l_subspace)
            L_op_set = AngularMomentum(l)
            L_op_set.to_Cartesian(l_subspace)

            H_SOC_in_L_subspace=np.kron(L_op_set.x(),S_Pauli.x())+np.kron(L_op_set.y(),S_Pauli.y())+np.kron(L_op_set.z(),S_Pauli.z())
            for i in np.arange(H_SOC_in_L_subspace.shape[0]):            
                for j in np.arange(H_SOC_in_L_subspace.shape[1]):
                    H_SOC[ref_point+i,ref_point+j]= H_SOC_in_L_subspace[i,j]
            ref_point += spin_degeneracy*len(l_subspace)

            # sub_sub_matrix = np.zeros((2*len(l_subspace), 2*len(l_subspace)), dtype=complex)
            # for it, direction in enumerate(['x', 'y', 'z']):
            #     sub_sub_matrix += np.kron(L_op_set.basis[direction], S_mat_set[it])
            # ## we've created matrix for a particular orbital
            # print(colored("size(sub_sub_matrix) = ", 'yellow'), np.shape(sub_sub_matrix))

        #     for i in np.arange(2*len(l_subspace)):
        #         for j in np.arange(2*len(l_subspace)):
        #             sub_matrix[sub_ref_p + i][sub_ref_p + j] = sub_sub_matrix[i][j]
        #     #saving sub_sub_matrix into sub_matrix
        #     sub_ref_p += 2*len(l_subspace) #incrementing reference point of sub_matrix

        #     print(colored("sub_ref_p = ", 'green'), sub_ref_p)

        # for i in np.arange(sub_mat_size):
        #     for j in np.arange(sub_mat_size):
        #         H_SOC[ref_p + i][ref_p + i] = sub_matrix[i][j]
        # ref_p += sub_mat_size
    return H_SOC

def generate_H_SOC_old(*filenames):
	
    if(len(filenames) == 0):
        win_file='wanner90.win'
    elif (len(filenames) == 1):
        win_file = filenames[0]
    else:
        print("error")
        exit(1)

    S_mat_set = angular_momentum_matrices(0.5)
    spin_degeneracy = S_mat_set[0].shape[0]

    comp = {}
    comp = composition_wrapper(win_file)
    comp.print_composition()

    num_wann = comp.get_num_wann()
    num_spin_wann = spin_degeneracy*num_wann

    H_SOC = np.zeros((num_spin_wann,num_spin_wann), dtype=complex)

    ''''
    We are looking for a matrix with a strucutre
    block diagonal
    each block is for each atom
    inside each block
    another block diagonal matrix
    for each L-subspace
    '''
    ref_p = 0 # ref point for H_SOC matrix
    iter = 0
    for atom in comp.composition: # iterate over atoms
        temp_list_of_orbitals = atom.split_orbitals_by_L()

        #we go through subspaces of ONE atom
        sub_ref_p = 0 # ref point for matrix of one atom
        sub_mat_size = 2 * sum(len(sublist) for sublist in temp_list_of_orbitals)
        sub_matrix = np.zeros((sub_mat_size, sub_mat_size), dtype=complex) 

        for subspace in temp_list_of_orbitals:
            l = get_L_from_orbitals_set_name(subspace)
            L_op_set = AngularMomentum(l)
            L_op_set.to_Cartesian(subspace)

            sub_sub_matrix = np.zeros((2*len(subspace), 2*len(subspace)), dtype=complex)
            for it, direction in enumerate(['x', 'y', 'z']):
                sub_sub_matrix += np.kron(L_op_set.basis[direction], S_mat_set[it])

            for i in np.arange(2*len(subspace)):
                for j in np.arange(2*len(subspace)):
                    sub_matrix[sub_ref_p + i][sub_ref_p + j] = sub_sub_matrix[i][j]
            #saving sub_sub_matrix into sub_matrix
            sub_ref_p += 2*len(subspace) #incrementing reference point of sub_matrix

        for i in np.arange(sub_mat_size):
            for j in np.arange(sub_mat_size):
                H_SOC[ref_p + i][ref_p + j] = sub_matrix[i][j]
        ref_p += sub_mat_size
    return H_SOC

if __name__=="__main__":
        
        #files_to_test_on=['mnte.win','wannier90_V2.win','wannier90_V3.win']
        #H_SOC = generate_H_SOC("../Unit_cell_composition/test/"+file_name)
        H_SOC = generate_H_SOC_old("../Unit_cell_composition/test/wannier90_V3.win")
        print("np.shape(H_SOC) = \n", np.shape(H_SOC))
        # with np.printoptions(threshold=sys.maxsize):
        #     print("H_SOC = \n", H_SOC)