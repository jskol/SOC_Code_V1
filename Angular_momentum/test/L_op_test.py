import sys
import numpy as np
sys.path.append('..')
from angular_momentum import AngularMomentum

### TODO: Correct for the new definition of Angular Momentum -its not a dict of dicts

def angular_momentum_operator_test(l: float, angular_momentum_set: list):
    assert len(angular_momentum_set) == 3 or
        print('l=%.1f not found'%l)
    mats=[x for x in angular_momentum.basis[l].items()]
    if l == 0.5:
        mats=mats[:-1] # To avoid s_0 in testing

    #Print Matrices
    for key,value in mats:
        print("L_%s :\n"%key, value)

    #Test Norm
    l_square=np.zeros(mats[0][1].shape)
    for i in np.arange(len(mats)):
        l_square = l_square + mats[i][1]@mats[i][1]
    diff=l_square-np.eye(len(mats[0][1])) * (l*(l+1))
    diff[np.absolute(diff)<1e-6]=0
    print("Testing if L^2 = l(l+1): ", ~np.any(diff))

    
	#Testing commutations
    for i in np.arange(len(mats)):
        s1=mats[i][1]
        s2=mats[(i+1)%len(mats)][1]
        s3=mats[(i+2)%len(mats)][1]

        #Proper order with Levi-Civita=1
        diff= s1@s2 - s2@s1 -1.j*s3
        diff[np.absolute(diff)< 1e-6]=0
        print("Testing if [S_%s,S_%s]=iS_%s"%(mats[i][0],mats[(i+1)%len(mats)][0],mats[(i+2)%len(mats)][0])," : ", ~np.any(diff))

        #Permutated order with Levi-Civita=-1
        diff2= s1@s3 - s3@s1 +1.j*s2
        diff2[np.absolute(diff2)< 1e-6]=0
        print("Testing if [S_%s,S_%s]=-iS_%s"%(mats[i][0],mats[(i+2)%len(mats)][0],mats[(i+1)%len(mats)][0])," : ", ~np.any(diff2))

if __name__=="__main__":
    l_set=[0.5,1,2]
    for l in l_set:
        AngMom=AngularMomentum(l)
        
        print("\n ---> Testing for l=%.1f"%l)
        angular_momentum_operator_test(l,AngMom)