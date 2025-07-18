import numpy as np

#helper functions

from generate_T_mat import generate_T_mat
from ladder_operator import update_angular_momentum

class AngularMomentum:
    '''
    AngularMomentum.basis object stores all L operators 
    in a nested dictionary:
    AngularMomentum.basis[l:float] -dictorary in a given l subspace
    AngularMomentum.basis[l:float][x] - returns L_x matrix
    AngularMomentum.basis[l:float][y] - returns L_y matrix
    AngularMomentum.basis[l:float][z] - returns L_z matrix
    '''
    
    basis={}
    
    def __init__(self,l_values):
        '''
        Constructs set of L operators (L_x,L_y,L_z) for all
        l-values given in l_values list 
        '''
        for l in l_values:
            AngularMomentum.basis[l]=update_angular_momentum(l)
    
    def print(self,l:float):
        '''
        Prints all L matrices for a given l-value
        '''
        print("\nIn the L=%.1f subspace angular momentum operators are given by"%l)
        for name,mat in AngularMomentum.basis[l].items():
            print("L_%s:\n"%name, mat)
    

    def to_Cartesian(self):
        '''
        Transforms all L operator
        initially given in the spherical harmonics basis
        to the Cartesian space
        '''

        for l,subspace in AngularMomentum.basis.items():
            T_mat=np.matrix(generate_T_mat(l))
            for name,mat in subspace.items():
                subspace[name]=T_mat@mat@T_mat.H




if __name__=="__main__":
    l_vals=[0.5,1]
    AM=AngularMomentum(l_vals)
    AM.print(l_vals[1])
    