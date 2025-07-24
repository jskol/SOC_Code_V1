import numpy as np
import re
from itertools import islice
import time	###
from termcolor import colored	###

class Wannier_data:
	def __init__(self,argv):
		self.x=int(argv[0])
		self.y=int(argv[1])
		self.z=int(argv[2])
		self.o1=int(argv[3])
		self.o2=int(argv[4])
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
	Function calculating hamiltonian for given files.
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

	spin_degeneracy = 2

	num_wann, nrpts = get_parameters(spin_up_file)
	print("num_wann, nrpts = ", num_wann, ", ", nrpts)	###
	
	skiplines = int(3 + np.ceil(nrpts/15.))
	print("skiplines = ", skiplines)	###

	M_up = np.loadtxt(spin_up_file, skiprows=skiplines)#[:,3:]
	M_down = np.loadtxt(spin_down_file, skiprows=skiplines)#[:,3:]

	# startt = time.time()	##
	for data_up,data_down in zip(M_up,M_down):

		### Check spin-up and spin-down data complince ########
		start = time.time()	##
		for ind in np.arange(5):
			if data_up[ind] != data_down[ind]:
				raise Exception("The two data files do not align\n Error occured for:\n", data_up, "\n", data_down)
				# print("The two data files do not align\n Error occured for:\n", data_up, "\n", data_down)
	# endd = time.time()
	# print(colored("checking data compliancy = ", "green"), endd - startt, "sec")

	#start = time.time()	##
	col, res = [], []
	iterator = 0
	for data_up,data_down in zip(M_up,M_down): #O(nrpts*nw^2)
		up_ind_1=int(spin_degeneracy*(data_up[3]-1)+1)
		up_ind_2=int(spin_degeneracy*(data_up[4]-1)+1)
		# down_ind_1 = up_ind_1 + 1 #?
		# down_ind_2 = up_ind_2 + 1 #?
		# from 		X = 1, 2, 3, 4, ...
		# we make 	X = 1, 3, 5, 7, ...
		# from 		X = 1, 2, 3, 4, ...
		# we make 	X = 2, 4, 6, 8, ...

		r_vec=[data_up[0],data_up[1],data_up[2]] #store \vec{R} components

		hop=[data_up[-2],data_up[-1]]
		inds = [up_ind_1, up_ind_2]
		col.append(Wannier_data(r_vec + inds + hop))
		# appending spin_up

		inds = [up_ind_1, up_ind_2 + 1]
		col.append(Wannier_data(r_vec + inds + [0.,0.]))

		inds = [up_ind_1 + 1, up_ind_2]
		col.append(Wannier_data(r_vec + inds + [0.,0.]))

		hop=[data_down[-2],data_down[-1]]
		inds = [up_ind_1 + 1, up_ind_2 + 1]
		col.append(Wannier_data(r_vec + inds + hop))
		# appending spin_down

		# col.sort(key=lambda w: (w.o2, w.o1)) # O(n*log(n))

		iterator += 1
		if iterator % num_wann==0:
			###
			col.sort(key=lambda w: (w.o2, w.o1)) # O(n*log(n))
			# print("col:")
			# for w in col:
			# 	print(w)
			### printing output column for [1-32][1-2] 
			for elem in col:
				res.append(elem)
			col = []
			#break

	#end = time.time()
	#print(colored("for r_pnt_in in np.arange(nrpts): ", "green"), end - start, "sec")
	###################################
	return res

def create_hamiltonian_2(*filenames):
	'''
	Function calculating hamiltonian for given files.
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

	spin_degeneracy = 2

	num_wann, nrpts = get_parameters(spin_up_file)
	print("num_wann, nrpts = ", num_wann, ", ", nrpts)	###
	
	skiplines = int(3 + np.ceil(nrpts/15.))
	print("skiplines = ", skiplines)	###

	M_up = np.loadtxt(spin_up_file, skiprows=skiplines)#[:,3:]
	M_down = np.loadtxt(spin_down_file, skiprows=skiplines)#[:,3:]

	# startt = time.time()	##
	for data_up,data_down in zip(M_up,M_down):

		### Check spin-up and spin-down data complince ########
		start = time.time()	##
		for ind in np.arange(5):
			if data_up[ind] != data_down[ind]:
				#raise Exception("The two data files do not align\n Error occured for:\n", data_up, "\n", data_down)
				print("The two data files do not align\n Error occured for:\n", data_up, "\n", data_down)
	# endd = time.time()
	# print(colored("checking data compliancy = ", "green"), endd - startt, "sec")

	#start = time.time()	##
	col, res = [], []
	iterator = 0
	for data_up,data_down in zip(M_up,M_down): #O(nrpts*nw^2)
		up_ind_1=int(spin_degeneracy*(data_up[3]-1)+1)
		up_ind_2=int(spin_degeneracy*(data_up[4]-1)+1)
		# down_ind_1 = up_ind_1 + 1 #?
		# down_ind_2 = up_ind_2 + 1 #?
		# from 		X = 1, 2, 3, 4, ...
		# we make 	X = 1, 3, 5, 7, ...
		# from 		X = 1, 2, 3, 4, ...
		# we make 	X = 2, 4, 6, 8, ...

		r_vec=[data_up[0],data_up[1],data_up[2]] #store \vec{R} components

		hop=[data_up[-2],data_up[-1]]
		inds = [up_ind_1, up_ind_2]
		col.append(Wannier_data(r_vec + inds + hop))
		# appending spin_up

		hop=[data_down[-2],data_down[-1]]
		inds = [up_ind_1 + 1, up_ind_2 + 1]
		col.append(Wannier_data(r_vec + inds + hop))
		# appending spin_down

		# col.sort(key=lambda w: (w.o2, w.o1)) # O(n*log(n))
		#####

		#####
		iterator += 1
		if iterator % num_wann==0:
			###
			print("col:")
			for w in col:
				print(w)
			#break
			col.sort(key=lambda w: (w.o2, w.o1)) # O(n*log(n))
			for elem in col:
				res.append(elem)
			col = []
			break ###

	#end = time.time()
	#print(colored("for r_pnt_in in np.arange(nrpts): ", "green"), end - start, "sec")
	###################################
	return res


def create_hamiltonian_original(*filenames):
	'''
	Function calculating hamiltonian for given files.
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

	spin_degeneracy = 2

	num_wann, nrpts = get_parameters(spin_up_file)
	print("num_wann, nrpts = ", num_wann, ", ", nrpts)	###
	
	skiplines = int(3 + np.ceil(nrpts/15.))
	print("skiplines = ", skiplines)	###

	M_up = np.loadtxt(spin_up_file, skiprows=skiplines)#[:,3:]
	M_down = np.loadtxt(spin_down_file, skiprows=skiplines)#[:,3:]

	res=[]	
	for r_pnt_in in np.arange(nrpts):
		H_merge=np.zeros((spin_degeneracy*num_wann,spin_degeneracy*num_wann),dtype='complex')
		ref_point=r_pnt_in*(num_wann**2)
		for sm_ind in np.arange(num_wann**2):
			up_point=M_up[ref_point+sm_ind]
			down_point=M_down[ref_point+sm_ind]
			H_merge[int(2*(up_point[3]-1))][int(2*(up_point[4]-1))]=up_point[5]+1.j*up_point[6]
			H_merge[int(2*(down_point[3]-1)+1)][int(2*(down_point[4]-1)+1)]=down_point[5]+1.j*down_point[6]
		
		for i in np.arange(spin_degeneracy*num_wann):
			for j in np.arange(spin_degeneracy*num_wann):
				temp=np.array([
					int(M_up[ref_point][0]),
					int(M_up[ref_point][1]),
					int(M_up[ref_point][2]),					
					int(j+1),
					int(i+1),
					np.real(H_merge[j][i]),
					np.imag(H_merge[j][i])
				])
				res.append(temp)

	return np.array(res)


if (__name__=="__main__"):

	file_name='test/wannier90_up_hr.dat'
	file_name2='test/wannier90_down_hr.dat'
	merged=create_hamiltonian(file_name, file_name2)
	#merged=create_hamiltonian_original(file_name)

	num_wann, nrpts = get_parameters(file_name)
	
	# for sets in merged:
	# 	print(sets.to_Wannier())