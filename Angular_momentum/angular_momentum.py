import numpy as np

#helper functions

from generate_T_mat import generate_T_mat
from ladder_operator import update_angular_momentum

class AngularMomentum:
    basis={}
    
    def __init__(self,l_values):
        for l in l_values:
            AngularMomentum.basis[l]=update_angular_momentum(l)
    
    def print(self,l):
        print("\nIn the L=%.1f subspace angular momentum operators are given by"%l)
        for name,mat in AngularMomentum.basis[l].items():
            print("L_%s:\n"%name, mat)
    

    def to_Cartesian(self):
        '''
        Transforms L operator
        from the spherical harmonics basis
        to the Cartesian space
        '''

        for l,subspace in AngularMomentum.basis.items():
            T_mat=np.matrix(generate_T_mat(l))
            for name,mat in subspace.items():
                subspace[name]=T_mat@mat@T_mat.H




if __name__=="__main__":
    l_vals=[0.5, 1]
    AM=AngularMomentum(l_vals)
    AM.print(l_vals[1])