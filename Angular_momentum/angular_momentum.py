import numpy as np


class AngularMomentum:
    basis={{}}
    
    def __init__(self,L_values):
        for L in L_values:
            AngularMomentum.basis[L]=update_angular_momentum(L)
    
    def print(self,L):
        print(" In the L=%.1f subspace angular momentum operators are given by\n"%L)
        for name,mat in AngularMomentum.basis[L].items():
            print("L_%s:\n"%name, mat)
    

    def to_Cartesian(self):
        '''
        Transforms L operator
        from the spherical harmonics basis
        to the Cartesian space
        '''

        for L,subspace in AngularMomentum.basis.items():
            T_mat=np.matrix(get_T_mat(L))
            for name,mat in subspace.items():
                subspace[name]=T_mat@mat@T_mat.H


