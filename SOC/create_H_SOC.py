import sys
import re
import numpy as np

#sys.path.append('../')
sys.path.append('../Angular_momentum')
from ladder_operator import angular_momentum_matrices,get_L_degeneracy

sys.path.append('../Unit_cell_composition')
from create_hamiltonian_time import create_hamiltonian, get_parameters
from UnitCell import UnitCell, Atom
from read_win import get_projections, get_composition, composition_wrapper

def generate_H_SOC(filename):
	'''
	if (len(filenames) == 1):	#if we pas 1 file, both are the same
		spin_up_file = filenames[0]
		spin_down_file = filenames[0]
	elif (len(filenames) == 2):
		spin_up_file = filenames[0]
		spin_down_file = filenames[1]
	elif(len(filenames)==0):
		spin_up_file ="wannier90_hr.dat"
		spin_down_file ="wannier90_hr.dat"	
	else:						#in other cases we have error
		print("error")
		exit(1)
	print("s_up = ", spin_up_file)		###
	print("s_down = ", spin_down_file)	###
	'''
	#spin_degeneracy = get_L_degeneracy(0.5)
	# num_wann, nrpts = get_parameters(spin_up_file)
	# print("num_wann, nrpts = ", num_wann, ", ", nrpts)	###

	S = angular_momentum_matrices(0.5)
	spin_degeneracy=S[0].shape[0]
	assert spin_degeneracy == get_L_degeneracy(0.5)
	print("S = \n", S)

	comp = {}
	comp = composition_wrapper("../Unit_cell_composition/test/wannier90.win")
	comp.print_composition()

	f=open(filename,'r')
	
	### Testing calculating number of Wanniers used in the projection

	num_wann=comp.get_num_wann()
	assert num_wann == 16
	num_spin_wann=spin_degeneracy*num_wann

	H_SOC = np.zeros((num_spin_wann,num_spin_wann), dtype=complex)
	print("H_SOC = \n", H_SOC)
	print("np.shape(H_SOC) = ", np.shape(H_SOC))
	
	ref_point=0

	for atom in comp.composition(): # iterate over atoms
		temp_orbitals=atom.orbitals
		#L_op_set=...
		temp_SOC_mat=np.zeros((L_op_set[0].shape[0]*S[0].shape[0],L_op_set[0].shape[0]*S[0].shape[0]),dtype=complex)
		
		## Generate SOC for one atom
		for direction in np.arange(3):
			temp_SOC_mat += np.kron(L_op_set[direction],S[direction])

		## Input SOC of this atom into the full SOC Hamiltonian
		for i in np.arange(temp_SOC_mat.shape[0]):
			for j in np.arange(temp_SOC_mat.shape[1]):
				H_SOC[ref_point+i][ref_point+j] = temp_SOC_mat[i][j]
		
		ref_point += temp_SOC_mat.shape[0]





	#return H_SOC
	

if __name__=="__main__":
	H_SOC = generate_H_SOC("../Unit_cell_composition/test/mnte.win")
	#print("H_SOC = \n", H_SOC)