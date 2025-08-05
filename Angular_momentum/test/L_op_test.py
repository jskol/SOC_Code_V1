import sys
import numpy as np
sys.path.append('..')
from angular_momentum import AngularMomentum

def angular_momentum_operator_test(angular_momentum: AngularMomentum):
    l=angular_momentum.L
    assert len(angular_momentum.basis.items()) == 3 and l != 0.5 or len(angular_momentum.basis.items()) == 4 and l==0.5, "Wrong number of L-matrices"

    

    #Print Matrices
    mats=[]
    for key,value in angular_momentum:
        print("L_%s :\n"%key, value)
        mats.append(value)
    ## Unpack dict just for testing convenince 
    
    if l == 0.5:
        mats=mats[:-1] # To avoid s_0 in testing
    
    #Test Norm
    l_square=np.zeros(mats[0].shape)
    for i in np.arange(len(mats)):
        l_square = l_square + mats[i]@mats[i]
    diff=l_square-np.eye(len(mats[0])) * (l*(l+1))
    diff[np.absolute(diff)<1e-6]=0
    print("Testing if L^2 = l(l+1): ", ~np.any(diff))

    dir_names=['x','y','z']
	#Testing commutations
    for i in np.arange(len(mats)):
        s1=mats[i]
        s2=mats[(i+1)%len(mats)]
        s3=mats[(i+2)%len(mats)]

        #Proper order with Levi-Civita=1
        diff= s1@s2 - s2@s1 -1.j*s3
        diff[np.absolute(diff)< 1e-6]=0

        print("Testing if [S_%s,S_%s]=iS_%s"%(dir_names[i],dir_names[(i+1)%len(mats)],dir_names[(i+2)%len(mats)])," : ", ~np.any(diff))

        #Permutated order with Levi-Civita=-1
        diff2= s1@s3 - s3@s1 +1.j*s2
        diff2[np.absolute(diff2)< 1e-6]=0
        print("Testing if [S_%s,S_%s]=-iS_%s"%(dir_names[i],dir_names[(i+2)%len(mats)],dir_names[(i+1)%len(mats)])," : ", ~np.any(diff2))
    
if __name__=="__main__":
    l_set=[0.5,1,2]
    for l in l_set:
        AngMom=AngularMomentum(l)
        
        print("\n ---> Testing for l=%.1f"%l)
        angular_momentum_operator_test(AngMom)


    AngMom=AngularMomentum(1.)
    AngMom.to_Cartesian()
    for key,value in AngMom:
        value[np.absolute(value)<1e-6]=0
        print("L_%s :\n"%key, value)
        