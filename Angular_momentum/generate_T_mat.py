import numpy as np


def generate_T_mat(l :float):

    if l==0:
        res=np.array([1])
    elif l==1:
        '''
        Wannier90, the default order of 
        orbitals for constructing maximally localized 
        Wannier functions (MLWFs) is: pz, px, py
        '''
        res=np.array((
            (0.,1.,0.),
            (-1./np.sqrt(2),0.,1./np.sqrt(2) ),
            (-1.j/np.sqrt(2),0.,-1.j/np.sqrt(2) )
        ),dtype=np.complex128)

    #...
    else:
        exit("Undefind l-subspace") ## Handle this issue
    return res




if __name__=="__main__":
    test_cases=[0,1,2]
    for l in test_cases:
        print(generate_T_mat(l))


