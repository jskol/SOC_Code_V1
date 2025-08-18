import numpy as np
import re
from itertools import islice
import time
from termcolor import colored

class Wannier_data:
	def __init__(self,argv):
		self.x=int(argv[0])
		self.y=int(argv[1])
		self.z=int(argv[2])
		self.o1=int(argv[3])
		self.o2=int(argv[4])
		if( len(argv)<6):
			self.hop=0.0+1.j*0.
		else:
			self.hop=argv[5]+1.j*argv[6]

	
	def __str__(self):
		return f"{self.x} {self.y} {self.z} {self.o1} {self.o2} {self.hop}"

	def to_Wannier(self):
		hopping=self.hop
		return [self.x, self.y, self.z, self.o1, self.o2, np.real(hopping),np.imag(hopping)]

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
	Function merging two input hamiltonian parameters into a set 
	of parameters for one-spinful hamiltonian
	It accepts:
	1) No source files-> useses the default name "wannier90_hr.dat"
	2) one source file-> doubles the parameters of one file
	3) two source files-> 1st one for spin-up second for spin-down
	'''
	if (len(filenames) == 1):
		spin_up_file = filenames[0]
		spin_down_file = filenames[0]
	elif (len(filenames) == 2):
		spin_up_file = filenames[0]
		spin_down_file = filenames[1]
	elif(len(filenames)==0):
		spin_up_file ="wannier90_hr.dat"
		spin_down_file ="wannier90_hr.dat"	
	else:
		print("error")
		exit(1)

	spin_degeneracy = 2
	num_wann, nrpts = get_parameters(spin_up_file)
	skiplines = int(3 + np.ceil(nrpts/15.))

	M_up = np.loadtxt(spin_up_file, skiprows=skiplines)
	M_down = np.loadtxt(spin_down_file, skiprows=skiplines)

	for data_up,data_down in zip(M_up,M_down):

		# Check spin-up and spin-down data complince
		start = time.time()	##
		for ind in np.arange(5):
			if data_up[ind] != data_down[ind]:
				raise Exception("The two data files do not align\n Error occured for:\n", data_up, "\n", data_down)

	col, res = [], []
	iterator = 0
	for data_up,data_down in zip(M_up,M_down): #O(nrpts*nw^2)
		up_ind_1=int(spin_degeneracy*(data_up[3]-1)+1) # "-1" to change from Fortran (wannier90) to python, "+1" change from python to Fortran
		up_ind_2=int(spin_degeneracy*(data_up[4]-1)+1) # "-1" to change from Fortran (wannier90) to python, "+1" change from python to Fortran
		# down_ind_1 = up_ind_1 + 1 #?
		# down_ind_2 = up_ind_2 + 1 #?
		# from 		X = 1, 2, 3, 4, ...
		# we make 	X = 1, 3, 5, 7, ...
		# from 		X = 1, 2, 3, 4, ...
		# we make 	X = 2, 4, 6, 8, ...

		r_vec=[data_up[0],data_up[1],data_up[2]] #store \vec{R} components
		# appending spin_up
		hop=[data_up[-2],data_up[-1]]
		inds = [up_ind_1, up_ind_2]
		col.append(Wannier_data(r_vec + inds + hop))
		
		
		# Adding zeros:
		inds = [up_ind_1, up_ind_2 + 1]
		col.append(Wannier_data(r_vec + inds + [0.,0.]))

		inds = [up_ind_1 + 1, up_ind_2]
		col.append(Wannier_data(r_vec + inds + [0.,0.]))
		
		# appending spin_down
		hop=[data_down[-2],data_down[-1]]
		inds = [up_ind_1 + 1, up_ind_2 + 1]
		col.append(Wannier_data(r_vec + inds + hop))
		

		iterator += 1
		if iterator % num_wann==0:
			col.sort(key=lambda w: (w.o2, w.o1))
			for elem in col:
				res.append(elem)
			col = []
	
		
	return res

if (__name__=="__main__"):

	file_name='test/wannier90_up_hr.dat'
	file_name2='test/wannier90_down_hr.dat'
	merged=create_hamiltonian(file_name, file_name2)

	num_wann, nrpts = get_parameters(file_name)
	
	for sets in merged:
		print(sets.to_Wannier())