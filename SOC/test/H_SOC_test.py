import numpy as np
import sys

sys.path.append('../../Angular_momentum')
sys.path.append('../../Unit_cell_composition')
sys.path.append('..')
from create_H_SOC import generate_H_SOC
from read_win import get_projections, get_composition, composition_wrapper

def check_atom_blocks(H_SOC, atoms):
	ref_point = 0
	num_atoms = len(atoms)
	print("num_atoms = ", num_atoms)

	for i in np.arange(4-1):
		block_size = 2 * len(atoms[i].orbitals)
		#print("block_size = ", block_size) ###
		ref_block = H_SOC[i*block_size:(i+1)*block_size, i*block_size:(i+1)*block_size]
		block = H_SOC[(i+1)*block_size:(i+2)*block_size, (i+1)*block_size:(i+2)*block_size]
		if not np.array_equal(block, ref_block):
			print("NOT EQUAL")
			return False
	ref_point = 8
	for i in np.arange(4-1):
		j = ref_point + i
		block_size = 2 * len(atoms[i+4].orbitals)
		#print("block_size = ", block_size) ###
		ref_block = H_SOC[ref_point+i*block_size:ref_point+(i+1)*block_size, ref_point+i*block_size:ref_point+(i+1)*block_size]
		block = H_SOC[ref_point+(i+1)*block_size:ref_point+(i+2)*block_size, ref_point+(i+1)*block_size:ref_point+(i+2)*block_size]
		if not np.array_equal(block, ref_block):
			print("NOT EQUAL")
			return False


	# for idx, atom in enumerate(atoms):
	# 	block_size = 2 * len(atom.orbitals)
	# 	block_size_next = 2 * len(atoms[idx+1].orbitals)
	# 	print("block_size = ", block_size) ###
	# 	ref_block = H_SOC[ref_point:ref_point+block_size, ref_point:ref_point+block_size]

	# 	num_blocks = len(atoms)
	# 	print("num_blocks = ", num_blocks) ###



		# for b in range(1, num_blocks):
		# 	i = ref_point + b * block_size
		# 	block = H_SOC[i:i+block_size, i:i+block_size]
		# 	if not np.array_equal(block, ref_block):
		# 		print(f"Atom {idx} ({atom.name}) has unequal blocks at {ref_point} and {i}")
		# 		return False

		# ref_point += block_size  # move to the next atom's block

	return True

if __name__=="__main__":
	#spin_up_file = "../Unit_cell_composition/test/mnte.win"
	spin_up_file = "../../Unit_cell_composition/test/wannier90.win"

	H_SOC = generate_H_SOC(spin_up_file)
	print("np.shape(H_SOC) = \n", np.shape(H_SOC))
	#with np.printoptions(threshold=sys.maxsize):
		#print("H_SOC = \n", H_SOC)
	for i in np.arange(32):
		print("H_SOC[",i,"] = \n", H_SOC[i])

	#assert H_SOC[0] == H_SOC[1]
	#print(np.alltrue(H_SOC[0] == H_SOC[1] == H_SOC[2] == H_SOC[3]))
	all_equal = all(np.array_equal(H_SOC[0], H_SOC[i]) for i in range(1, 8))
	print(all_equal)

	print(np.array_equal(H_SOC[8:14][8:14], H_SOC[14:20][14:20]))

	comp = composition_wrapper(spin_up_file)

	iter = 0
	# for atom in comp.composition:
	# 	print("H_SOC[",iter,":",iter+2*norb,"][",iter,":",iter+2*norb,"], H_SOC[",iter,":",iter+2*norb,"][",iter,":",iter+2*norb,"]")
	# 	print(np.array_equal(H_SOC[iter:iter+2*norb][iter:iter+2*norb], H_SOC[iter:iter+2*norb][iter:iter+2*norb]))
	# 	print(len(atom.orbitals))

	if check_atom_blocks(H_SOC, comp.composition):
		print("All atom blocks are equal for each atom.")
	else:
		print("Found unequal blocks.")


# ../Unit_cell_composition/test/wannier90.win