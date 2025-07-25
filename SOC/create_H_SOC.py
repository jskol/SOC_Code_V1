import sys
#sys.path.append('../')
sys.path.insert(0, '../Angular_momentum')
from ladder_operator import angular_momentum_matrices
sys.path.insert(0, '../Unit_cell_composition')
from create_hamiltonian_time import create_hamiltonian, get_parameters
from UnitCell import UnitCell, Atom
from read_win import get_projections, get_composition, composition_wrapper
import re

import numpy as np

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
	spin_degeneracy = 2
	# num_wann, nrpts = get_parameters(spin_up_file)
	# print("num_wann, nrpts = ", num_wann, ", ", nrpts)	###

	S = angular_momentum_matrices(0.5)
	print("S = \n", S)

	comp = {}
	comp = composition_wrapper("../Unit_cell_composition/test/wannier90.win")
	comp.print_composition()

	f=open(filename,'r')
	for line in f.readlines():
	# special care as the wannier can have 
	# positions of atoms in "cart" -Cartesian
	# or fractions of primit shifts "frac"

		# to chyba niepotrzebne:
		if(re.search(r'num_wann',line.rstrip())):
			#print("replace line")
			num_wann = int(line.replace('num_wann', '').replace(' ', '').replace('=', ''))
			# there was an easier way
			print("num_wann = ", num_wann)
			break

		

	
	#num_wann = 16
	H_SOC = np.zeros((spin_degeneracy*num_wann, spin_degeneracy*num_wann), dtype=complex)
	print("H_SOC = \n", H_SOC)
	print("np.shape(H_SOC) = ", np.shape(H_SOC))


















	#return H_SOC
	

if __name__=="__main__":
	H_SOC = generate_H_SOC("../Unit_cell_composition/test/mnte.win")
	#print("H_SOC = \n", H_SOC)