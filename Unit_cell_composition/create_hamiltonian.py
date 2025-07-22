import numpy as np
import re
from itertools import islice

def get_parameters(filename="wannier90_hr.dat"):
	'''
	Function returning num_wann and nrpts from the file.
	'''
	#Reads only 3 first lines of a file.
	with open(filename) as f:
		next(f)  # skip first line
		num_wann = int(next(f).strip())
		nrpts = int(next(f).strip())
	return num_wann, nrpts


def create_hamiltonian(*filenames):
	'''
	Function calculating hamiltonian for given files.
	'''
	#print("len(filenames) = ", len(filenames))
	if (len(filenames) == 1):	#if we pas 1 file, both are the same
		spin_up_file = filenames[0]
		spin_down_file = filenames[0]
	elif (len(filenames) == 2):
		spin_up_file = filenames[0]
		spin_down_file = filenames[1]
	else:						#in other cases we have error
		print("error")
		exit(1)
	print("s_up = ", spin_up_file)		###
	print("s_down = ", spin_down_file)	###

	spin_degeneracy = 2

	num_wann, nrpts = get_parameters(spin_up_file)
	print("num_wann, nrpts = ", num_wann, ", ", nrpts)	###
	
	skiplines = int(3 + np.ceil(nrpts/15.))
	print("skiplines = ", skiplines)	###

	M_up = np.loadtxt(spin_up_file, skiprows=skiplines)[:,3:]
	M_down = np.loadtxt(spin_down_file, skiprows=skiplines)[:,3:]
	print("M_up = \n", M_up) # it prints in scientific notation ###

	M = np.zeros((spin_degeneracy * num_wann * nrpts, spin_degeneracy * num_wann * nrpts))#, dtype=complex)
	print("M_shape = ", M.shape)	###
	print("M = \n", M)	###

	for lines in M_up:
		M[int(spin_degeneracy*lines[0]) - 2][int(spin_degeneracy*lines[1]) - 2] = lines[2] + 1j*lines[3]
		print("[int(spin_degeneracy*lines[0]) - 1][int(spin_degeneracy*lines[1]) - 1]", int(spin_degeneracy*lines[0]), ", ", int(spin_degeneracy*lines[1]))
		break
	for lines in M_down:
		M[int(spin_degeneracy*lines[0]) - 1][int(spin_degeneracy*lines[1]) - 1] = lines[2] + 1j*lines[3]
		print("[int(spin_degeneracy*lines[0]) - 1][int(spin_degeneracy*lines[1]) - 1]", int(spin_degeneracy*lines[0]), ", ", int(spin_degeneracy*lines[1]))
		break
	# We have '-2' for spin up elements, and '-1' for spin down elements
	# because ...

	print("M = \n", M)	###	








if (__name__=="__main__"):
	create_hamiltonian("test/wannier90_up_hr.dat", "test/wannier90_down_hr.dat")