import numpy as np
import re
from itertools import islice

def get_matrix_size(filename):
	f=open(filename,'r')
	element_index = 0
	for line in f.readlines():
		elements = re.sub(r'[\t ]+', ' ', line.strip()).split(' ')
		if (len(elements) != 7):
			continue
		if (len(elements) == 7):
			if (int(elements[3]) > int(element_index)): # i had to add int() to both, because it didn't work
				element_index = elements[3]
			else:
				return element_index

def save_to_file_with_zeros_end(elements, matrix_size, output_file):
	# we change the values to 0.0
	elements[5] = 0.0
	elements[6] = 0.0
	for i in range(1, matrix_size+1): # we iterate through remaining columns
		elements[3] = matrix_size + i # increase the index value
		#print("i, elem[3] = ", i, ", ", elements[3])
		result_line = ' '.join(str(x) for x in elements)
		output_file.write(result_line + '\n') #save line to file

def save_to_file_with_zeros_beg(elements, matrix_size, output_file):
	# we change the values to 0.0
	elements[5] = 0.0
	elements[6] = 0.0
	elements[4] = int(elements[4]) + 1 # increase the index value
	for i in range(1, matrix_size+1): # we iterate through first 'matrix_size' columns
		elements[3] = i # increase the index value
		result_line = ' '.join(str(x) for x in elements)
		output_file.write(result_line + '\n') #save line to file

def create_hamiltonian(spin_up_file):#, spin_down_file):
	f=open(spin_up_file,'r')
	#matrix_size = int(get_matrix_size(spin_up_file))
	#print("matrix size = ", matrix_size)
	#big_matrix = np.zeros((matrix_size**2, matrix_size**2), dtype=complex)
	end_of_matrix_flag = False

	with open(spin_up_file, 'r') as f:
		lines = f.readlines()
		num_wann = int(lines[1].strip())
		nrpts = int(lines[2].strip())
	matrix_size = 2*num_wann #one spin matrix
	M = np.zeros((matrix_size, matrix_size), dtype=complex) #matrix for 'up' & 'down'
	M_up = np.zeros((num_wann, num_wann), dtype=complex)
	M_down = np.zeros((num_wann, num_wann), dtype=complex)

	print("num_wann = ", num_wann)
	print("nrpts = ", nrpts)



'''
	for line in f.readlines():
		elements = re.sub(r'[\t ]+', ' ', line.strip()).split(' ')
		if (len(elements) != 7):
			continue
		if (len(elements) == 7):
			with open('output_file.dat', 'a') as output_file:
				output_file.write(re.sub(r'[\t ]+', ' ', line.strip()) + '\n') #save to file
				if (int(elements[3]) == matrix_size):
					save_to_file_with_zeros_end(elements, matrix_size, output_file)
					if	(int(elements[3]) == 2*matrix_size and int(elements[4]) == matrix_size):
						end_of_matrix_flag = True
				if (int(elements[4]) == matrix_size and end_of_matrix_flag == True):
					save_to_file_with_zeros_beg(elements, matrix_size, output_file)
					output_file.write('hello \n') #save line to file
					end_of_matrix_flag = False
'''

'''
import numpy as np

# Initialize 256x256 complex zero matrix
N = 16
big_matrix = np.zeros((N**2, N**2), dtype=complex)

for i in range(N):
    for j in range(N):
        # Compute 16x16 block (replace this with your real computation)
        block = np.zeros((N, N), dtype=complex)  # dummy block

        # Insert block into the big matrix
        row_start = i * N
        col_start = j * N
        big_matrix[row_start:row_start+N, col_start:col_start+N] = block

'''



if (__name__=="__main__"):
	create_hamiltonian("test/wannier90_down_hr.dat")