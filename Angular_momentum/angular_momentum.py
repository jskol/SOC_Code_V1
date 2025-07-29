import numpy as np

#helper functions

from generate_T_mat import generate_T_mat
from ladder_operator import update_angular_momentum

class AngularMomentum:
    '''
    AngularMomentum.basis object stores all L operators 
    in a nested dictionary:
    AngularMomentum.basis -dictorary in a given l subspace
    AngularMomentum.basis[x] - returns L_x matrix
    AngularMomentum.basis[y] - returns L_y matrix
    AngularMomentum.basis[z] - returns L_z matrix
    '''
        
    def __init__(self,l_value):
        '''
        Constructs a dict of L operators (L_x,L_y,L_z)
        '''
        self.basis=update_angular_momentum(l_value)
        self.L=l_value
    
    def __iter__(self):
        return iter(self.basis.items())

    def print(self):
        '''
        Prints all L matrices for a given l-value
        '''
        print("\nIn the L=%.1f subspace angular momentum operators are given by"%l)
        for name,mat in self.basis.items():
            mat_temp=mat
            mat_temp[np.absolute(mat_temp)<1e-3]=0
            print("L_%s:\n"%name, mat_temp)
    

    def to_Cartesian(self,*projector_set):
        '''
        Transforms all L operator
        initially given in the spherical harmonics basis
        to the Cartesian space
        '''
        if self.L != 0.5:
            T_mat=np.matrix(generate_T_mat(self.L,*projector_set))
            for name,mat in self.basis.items():
                self.basis[name]=T_mat@mat@T_mat.H




if __name__=="__main__":
    l_vals=[0, 0.5, 1]
    for l in l_vals:
        AM=AngularMomentum(l)
        AM.print()
        AM.to_Cartesian()
        AM.print()


    AM=AngularMomentum(1)
    AM.print()
    AM.to_Cartesian(['pz','px','py'])
    AM.print()

    AM=AngularMomentum(1)
    AM.print()
    AM.to_Cartesian(['px','py'])
    AM.print()
