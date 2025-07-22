import numpy as np
import re
from itertools import islice

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
	#print("len(filenames) = ", len(filenames))
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
				res.append(Wannier_data([
					int(M_up[ref_point][0]),
					int(M_up[ref_point][1]),
					int(M_up[ref_point][2]),					
					int(j+1),
					int(i+1),
					np.real(H_merge[j][i]),
					np.imag(H_merge[j][i])
				]))
				
	return res


def create_hamiltonian_original(*filenames):
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
	merged=create_hamiltonian(file_name)
	num_wann, nrpts = get_parameters(file_name)
	
	for r in np.arange(nrpts):
		range_l=int(r*(2*num_wann)**2)
		range_h=int((r+1)*(2*num_wann)**2)
		mat=(merged[range_l:range_h][:,-2]+1.j*merged[range_l:range_h][:,-1]).reshape((int(2*num_wann),int(2*num_wann)))
		
		print("Testing r #: %i"%r)
		for i  in np.arange(2*num_wann,step=2):
			if (mat[i][i] != mat[i+1][i+1] or mat[i][i+1]!=mat[i][i+1]):
				print(mat[i][i], " : " ,mat[i+1][i+1])
				print(mat[i][i+1], " : ", mat[i][i+1])

	'''
	for r in np.arange(nrpts):
		range_l=int(r*(2*num_wann)**2)
		range_h=int((r+1)*(2*num_wann)**2)
		mat=(merged[range_l:range_h][:,-2]+1.j*merged[range_l:range_h][:,-1]).reshape((2*num_wann,2*num_wann))
		print("Testing r #: %i"%r)
		for i  in np.arange(2*num_wann,step=2):
			if (mat[i][i] != mat[i+1][i+1] or mat[i][i+1]!=mat[i][i+1]):
				print(mat[i][i], " : " ,mat[i+1][i+1])
				print(mat[i][i+1], " : ", mat[i][i+1])
	'''


	for line in merged:
		print ("%i %i %i %i %i %.6f %.6f"%(line[0],line[1],line[2],line[3],line[4],line[5],line[6]))