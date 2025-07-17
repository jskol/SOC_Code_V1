import sys
import numpy as np
sys.path.append('..')
from ladder_operator import angular_momentum_matrices



if __name__=="__main__":
    Lx,Ly,Lz=angular_momentum_matrices(1)

    p_orb=np.array((
        (-1./np.sqrt(2),0.,1./np.sqrt(2) ),
        (-1.j/np.sqrt(2),0.,-1.j/np.sqrt(2) ),
        (0.,1.,0.)
    ),dtype=np.complex128)
    # Add them into to set of all orbital space spaning "matrices"
     
    #L-operator in the basis of spherical harmonics
    p_orb_L=np.array((
    ((0.,1.,0.),(1.,0.,1.),(0.,1.,0.))/np.sqrt(2),
    ((0.,-1.j,0.),(1.j,0.,-1.j),(0.,1.j,0.))/np.sqrt(2),
    ((1.,0.,0.),(0.,0.,0.),(0.,0.,-1.)),# not divided by sqrt(2)
    ),dtype=np.complex128)

    print(Lx)

    Lx_q=np.matrix(p_orb)@Lx@np.matrix(p_orb).H
    

    spins=angular_momentum_matrices(0.5)
    print(len(spins))
    L_Cartesian=[]
    for L in [Lx,Ly,Lz]:
        L_Cartesian.append(np.matrix(p_orb)@L@np.matrix(p_orb).H)

    H_SO=np.zeros((6,6),dtype=complex)

    for i in np.arange(len(spins)):
        H_SO = H_SO+ np.kron(L_Cartesian[i],spins[i])

    H_SO[np.absolute(H_SO)< 1e-3]=0
    print(H_SO)