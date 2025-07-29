import numpy as np
import sys
from termcolor import colored

sys.path.append('../../Angular_momentum')
sys.path.append('../../Unit_cell_composition')
sys.path.append('..')
from angular_momentum import AngularMomentum
from create_H_SOC import generate_H_SOC
from read_win import get_projections, get_composition, composition_wrapper

def check_atom_blocks(H_SOC, atoms):
	ref_point = 0
	num_atoms = len(atoms)
	print("num_atoms = ", num_atoms)
	return True

def check_difference(mat, mat2, size, ref):
    for i in np.arange(size):
        for j in np.arange(size):
            if(np.absolute(mat[i][j] - mat2[ref + i][ref + j])) > 1e-6:
                print("i, j = ", i, ", ",j)
                print("H_SOC_PS[i][j] = ",H_SOC_PS[i][j])
                print("H_SOC[ref + i][ref + j] = ",H_SOC[ref + i][ref + j])
                return False
    return True

if __name__=="__main__":
    S_pauli=AngularMomentum(0.5)
    S=AngularMomentum(0)
    P=AngularMomentum(1)
    D=AngularMomentum(2)
    P.to_Cartesian()#['px','py','pz'])
    D.to_Cartesian()#['dyz','dxz','dx2-y2','dz2'])

    H_SOC = generate_H_SOC("../../Unit_cell_composition/test/wannier90_V3.win")

    H_SOC_DS = np.kron(D.x(),S_pauli.x()) + np.kron(D.y(),S_pauli.y())+ np.kron(D.z(),S_pauli.z())
    H_SOC_PS = np.kron(P.x(),S_pauli.x()) + np.kron(P.y(),S_pauli.y())+ np.kron(P.z(),S_pauli.z())
    H_SOC_SS = np.kron(S.x(),S_pauli.x()) + np.kron(S.y(),S_pauli.y())+ np.kron(S.z(),S_pauli.z())

    H_SOC_SS = np.array(H_SOC_SS)
    H_SOC_PS = np.array(H_SOC_PS)
    H_SOC_DS = np.array(H_SOC_DS)
    H_SOC = np.array(H_SOC)

    print(colored("S ORBITALS:", 'red'))
    ref = 0
    size = 2 # S orbitals
    ### 1st S orbital ###
    print(check_difference(H_SOC_SS, H_SOC, size, ref))

    ### 2nd S orbital ###
    ref += size
    print(check_difference(H_SOC_SS, H_SOC, size, ref))

    ### 3rd S orbital ###
    ref += size
    print(check_difference(H_SOC_SS, H_SOC, size, ref))

    ### 4th S orbital ###
    ref += size
    print(check_difference(H_SOC_SS, H_SOC, size, ref))

    for _ in np.arange(4):
        print(colored("-----", 'cyan'))
        '''
        P orbitals
        '''
        size = 6
        print(colored("P ORBITALS:", 'red'))
        ### 1st P orbital ###
        print(check_difference(H_SOC_PS, H_SOC, size, ref))

        ### 2nd P orbital ###
        print(check_difference(H_SOC_PS, H_SOC, size, ref))

        ### 3rd P orbital ###
        print(check_difference(H_SOC_PS, H_SOC, size, ref))

        '''
        D orbitals
        '''
        size = 8
        print(colored("D ORBITALS:", 'red'))
        ### 1st D orbital ###
        ref += size
        print(check_difference(H_SOC_DS, H_SOC, size, ref))

        ### 2nd D orbital ###
        print(check_difference(H_SOC_DS, H_SOC, size, ref))
        
        ### 3rd D orbital ###
        print(check_difference(H_SOC_DS, H_SOC, size, ref))
        
        ### 4th D orbital ###
        print(check_difference(H_SOC_DS, H_SOC, size, ref))

    ### one S orbital ###
    print(colored("S ORBITALS:", 'red'))
    size = 2
    ref += size
    print(check_difference(H_SOC_PS, H_SOC, size, ref))

'''
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

	if check_atom_blocks(H_SOC, comp.composition):
		print("All atom blocks are equal for each atom.")
	else:
		print("Found unequal blocks.")


# ../Unit_cell_composition/test/wannier90.win
'''