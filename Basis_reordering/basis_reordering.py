import numpy as np
import string

###
# import re
from termcolor import colored

import sys
sys.path.append('../SOC')
from create_H_SOC import generate_H_SOC

sys.path.append('../Unit_cell_composition')
from read_params import read_params, immerse_params_in_composition
from read_win import get_projections, get_composition, composition_wrapper

# sys.path.append('../Angular_momentum')
# from ladder_operator import angular_momentum_matrices, get_L_degeneracy, update_angular_momentum
# from angular_momentum import AngularMomentum

# sys.path.append('../Unit_cell_composition')
# from create_Hamiltonian import create_hamiltonian, get_parameters
# from UnitCell import UnitCell, Atom, get_L_from_orbitals_set_name

###

if __name__=="__main__":
    file = "../Unit_cell_composition/test/wannier90_V4.win"
    param_file = "../Unit_cell_composition/test/params"
    res=read_params(param_file)
    comp=composition_wrapper(file)
    res2=immerse_params_in_composition(res,comp)

    H_SOC = generate_H_SOC(file, params=res2)

    print("comp = ", comp)



'''
N=4
Mat1=np.zeros((N,N),dtype=object)

for i in np.arange(Mat1.shape[0]):
    for j in np.arange(Mat1.shape[1]):
        Mat1[i][j]='<%s | H | %s >'%(str(i+1),str(j+1))

print("\nInitial ordering of elements\n",Mat1)

#Exchange 2-3
x,y=2,3

T_mat=np.eye(N,dtype=int)
T_mat[x-1][x-1]=0
T_mat[y-1][y-1]=0
T_mat[x-1][y-1]=1
T_mat[y-1][x-1]=1

print("\nTransfer Matrix\n",T_mat)

Mat1_T=np.matrix(T_mat).T@Mat1@T_mat 
print("\nAfter exchanging(%i with %i):\n"%(x,y),Mat1_T)
'''
