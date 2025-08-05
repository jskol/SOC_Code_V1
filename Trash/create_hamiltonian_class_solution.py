import numpy as np

class Wannier_data:
	def __init__(self,argv):
		self.x=int(argv[0])
		self.y=int(argv[1])
		self.z=int(argv[2])
		self.o1=int(argv[3])
		self.o2=int(argv[4])
		if( len(argv)<6):
			self.hop=0.0
		else:
			self.hop=argv[5]+1.j*argv[6]

	def __str__(self):
		return f"{self.x} {self.y} {self.z} {self.o1} {self.o2} {self.hop}"

	def to_Wannier(self):
		'''
		change Wannier into a list of vaules stored in
		the same way as they are stored in the original
		wannier90 file
		'''
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
	Function Reading the tight-binding Hamiltonian matrix elements
	
	Input(optional):
	-list of file names (from zero to two)
	-if len(input)==0 both spin channels get parameters from a default file name 'wannier90_hr.dat'
	-if len(input)==1 both spin channels get parameters from a specified file name
	-if len(input)==2 first file gives parameters for the spin-UP channel and the ohter file for the spin DOWN
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

	M_up = np.loadtxt(spin_up_file, skiprows=skiplines)
	M_down = np.loadtxt(spin_down_file, skiprows=skiplines)
	res=[]

	iterator=0
	col_L,col_R=[],[]	# Store here simultanously two consecutive cols
	for data_up,data_down in zip(M_up,M_down):

		### Check spin-up and spin-down data complince ########
		for ind in np.arange(5):
			if data_up[ind] != data_down[ind]:
				raise Exception("The two data files do not align\n Error occured for:\n", data_up, "\n", data_down)
		########################################################
		
		Upper_Left_ind1=int(spin_degeneracy*(data_up[3]-1)+1)
		Upper_Left_ind2=int(spin_degeneracy*(data_up[4]-1)+1)	
		r_vec=[data_up[0],data_up[1],data_up[2]] #store \vec{R} components
		for move_down in np.arange(spin_degeneracy):
			for move_right in np.arange(spin_degeneracy):
				inds=[Upper_Left_ind1+ move_down,Upper_Left_ind2+ move_right] # store the new indices
				hop=[0.,0.] # store real and imaginary part of hopping
				if move_down ==0 and move_right==0:
					hop=[data_up[-2],data_up[-1]]
				elif move_down==1 and move_right==1:
					hop=[data_down[-2],data_down[-1]]
				
				final_set=r_vec+inds+hop
				Wannieraized=Wannier_data(final_set)
				if(move_right==0):
					col_L.append(Wannieraized)
				else:
					col_R.append(Wannieraized)

		iterator += 1

		# ####### once the col_L and col_R are filled 
		# ####### with 2*num_wannier concatinate the two cols
		if iterator % num_wann==0:
			for at in col_L:
				res.append(at)
			col_L=[]

			for at in col_R:
				res.append(at)
			col_R=[]
		#####################################################
	return res


if (__name__=="__main__"):

	file_name='test/wannier90_up_hr.dat'
	merged=create_hamiltonian(file_name)
	num_wann, nrpts = get_parameters(file_name)

	for sets in merged:
		print(sets.to_Wannier())
		
