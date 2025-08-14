import sys,os
import re
import numpy as np
from termcolor import colored

#sys.path.append('../Angular_momentum')
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Angular_momentum'))
from ladder_operator import angular_momentum_matrices, get_L_degeneracy, update_angular_momentum
from angular_momentum import AngularMomentum


#sys.path.append('../Unit_cell_composition')
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Unit_cell_composition'))
from create_Hamiltonian import create_hamiltonian, get_parameters
from UnitCell import UnitCell, Atom, get_L_from_orbitals_set_name
from read_win import get_projections, get_composition, composition_wrapper
from read_params import read_params, immerse_params_in_composition

def check_input(atom_comp, atom_param, check_type):
    if (atom_comp.name != atom_param[0]
        or any(atom_comp.position[p] != atom_param[p+1] for p in np.arange(3))): # atoms mismatch 
        exit("Atoms mismatch while constructing H_SOC")
    if (check_type == 'SOC' and (len(atom_comp.split_orbitals_by_L()) != (len(atom_param) - 4))):
        exit("Atoms mismatch while constructing H_SOC")

def add_SOC(H_SOC, params, comp)->None:
    '''
    Extends H_SOC matrix by local and orbital-selective 
    spin-orbit Hamiltonian defined in params
    '''
    ref_point = 0 # ref point for H_SOC matrix
    S_Pauli = AngularMomentum(0.5)
    spin_degeneracy = S_Pauli.x().shape[0]
    if ('SOC' in params):
        for atom_comp, atom_param in zip(comp.composition, params['SOC']):
            check_input(atom_comp, atom_param, 'SOC')

            split_orb=atom_comp.split_orbitals_by_L()

            for iterator ,l_subspace in enumerate(split_orb):
                H_SOC_strength=atom_param[4+iterator]
                l=get_L_from_orbitals_set_name(l_subspace)
                L_op_set = AngularMomentum(l)
                L_op_set.to_Cartesian(l_subspace)

                H_SOC_in_L_subspace=H_SOC_strength*(np.kron(L_op_set.x(),S_Pauli.x())+np.kron(L_op_set.y(),S_Pauli.y())+np.kron(L_op_set.z(),S_Pauli.z()))
                for i in np.arange(H_SOC_in_L_subspace.shape[0]):            
                    for j in np.arange(H_SOC_in_L_subspace.shape[1]):
                        H_SOC[ref_point+i,ref_point+j] += H_SOC_in_L_subspace[i,j]
                ref_point += spin_degeneracy*len(l_subspace)

def add_magnetic_field(H_SOC, params, comp)-> None:
    '''
    Extends H_SOC matrix by local and orbital-selective 
    magnetic-field defined in params
    '''
    ref_point = 0 # ref point for H_SOC matrix
    S_Pauli = AngularMomentum(0.5)
    spin_degeneracy = S_Pauli.x().shape[0]
    if ('magnetic-field' in params):
        for atom_comp, atom_param in zip(comp.composition, params['magnetic-field']):
            check_input(atom_comp, atom_param, 'magnetic-field')

            split_orb=atom_comp.split_orbitals_by_L()
            
            
            for iterator, l_subspace in enumerate(split_orb):
                r       = atom_param[4+3*iterator] # "3" because each magnetic field is determined by 3 coeff's
                theta   = atom_param[5+3*iterator]
                phi     = atom_param[6+3*iterator]
                mag_field_x = r * np.sin(theta) * np.cos(phi)
                mag_field_y = r * np.sin(theta) * np.sin(phi)
                mag_field_z = r * np.cos(theta)
                l=get_L_from_orbitals_set_name(l_subspace)
                L_op_set = AngularMomentum(l)
                L_op_set.to_Cartesian(l_subspace)
                id_mat = np.eye(L_op_set.x().shape[0])

                H_MAG_in_L_subspace=np.kron(id_mat,S_Pauli.x()*mag_field_x)+np.kron(id_mat,S_Pauli.y()*mag_field_y)+np.kron(id_mat,S_Pauli.z()*mag_field_z)
                for i in np.arange(H_MAG_in_L_subspace.shape[0]):            
                    for j in np.arange(H_MAG_in_L_subspace.shape[1]):
                        H_SOC[ref_point+i,ref_point+j] += H_MAG_in_L_subspace[i,j]
                ref_point += spin_degeneracy*len(l_subspace)


def generate_H_SOC(*filenames, params={}, print_details=False)-> np.ndarray:
    '''
    TODO
    '''
    print("len(filenames) = ", len(filenames))
    if(len(filenames) == 0):
        win_file='wanner90.win'
    elif (len(filenames) == 1):	#if we pas 1 file, both are the same
        win_file = filenames[0]
    else:						#in other cases we have error
        print("error - file")
        exit(1)

    S_Pauli = AngularMomentum(0.5)
    spin_degeneracy = S_Pauli.x().shape[0]
    comp = {}
    comp = composition_wrapper(win_file)
    if print_details:
        comp.print_composition()

    num_wann=comp.get_num_wann()
    num_spin_wann=spin_degeneracy*num_wann

    H_SOC = np.zeros((num_spin_wann,num_spin_wann), dtype=complex) # Inititate proprely sized zero-matrix

    add_SOC(H_SOC, params, comp) # add SOC
    add_magnetic_field(H_SOC, params, comp) # add mag-field
        
    return H_SOC

def generate_H_SOC_old(*filenames, print_details=False):
	
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
    if print_details:
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
        file = "../Unit_cell_composition/test/wannier90_2_atomswin"
        param_file = "../Unit_cell_composition/test/params_2_atoms"
        res=read_params(param_file)
        comp=composition_wrapper(file)
        #comp.print_composition()
        # print("\nPrint prams\n")
        params_names=['magnetic-field','SOC']
        for prop in params_names:
            for at in comp:
                print(at.name, " with ", at.orbitals)
            print("\nInitial read\n")
            for mag in res[prop]:
                print(mag)

        res2=immerse_params_in_composition(res,comp)
            # print("\n%s : After matching .win\n"%prop)
            # for mag in res2[prop]:
            #     print(mag)

        #H_SOC = generate_H_SOC(file, params=res2)
        # print("np.shape(H_SOC) = \n", np.shape(H_SOC))
        # with np.printoptions(threshold=sys.maxsize):
        #     print("H_SOC = \n", H_SOC)