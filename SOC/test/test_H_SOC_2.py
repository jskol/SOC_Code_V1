'''
Testing The fact that  SOC projected in the
'dyz','dxz','dxy' subspace is equivalent to 
-H_SOC in the p-subspace stated in 
https://arxiv.org/pdf/1507.06323

Yes, order is important:
[px,py,pz]-> ['dyz','dxz','dxy']
'''


import numpy as np
import sys

sys.path.append('../../Angular_momentum')
sys.path.append('../../Unit_cell_composition')
sys.path.append('..')

from angular_momentum import AngularMomentum
from create_H_SOC_V2 import generate_H_SOC_V2
from read_win import composition_wrapper


if __name__=="__main__":
    l_vals=[0, 0.5, 1]
    S=AngularMomentum(0.5)
    P=AngularMomentum(1)
    D=AngularMomentum(2)
    P.to_Cartesian(['px','py','pz'])
    D.to_Cartesian(['dyz','dxz','dxy'])


    H_SOC_DS = np.kron(D.x(),S.x()) + np.kron(D.y(),S.y())+ np.kron(D.z(),S.z())
    H_SOC_PS = np.kron(P.x(),S.x()) + np.kron(P.y(),S.y())+ np.kron(P.z(),S.z())     
    H_SOC_DS[np.absolute(H_SOC_DS)< 1e-3]=0
    H_SOC_PS[np.absolute(H_SOC_PS)< 1e-3]=0

    print("H_SOC (D-subspace):\n",H_SOC_DS)
    print("H_SOC (P-subspace):\n",H_SOC_PS)
    sum_mat=H_SOC_DS+H_SOC_PS
    sum_mat[np.absolute(sum_mat)<1e-3]=0
    print("is H_SOC(D) = -H_SOC(P): ", ~np.any(sum_mat), "\n\n")
    


    ## Reference matrices

    S_P=AngularMomentum(0.5)
    S=AngularMomentum(0)
    S.to_Cartesian()
    P=AngularMomentum(1)
    P.to_Cartesian(['px','py','pz'])
    D=AngularMomentum(2)
    D.to_Cartesian()  
    H_SOC_SS = np.kron(S.x(),S_P.x()) + np.kron(S.y(),S_P.y())+ np.kron(S.z(),S_P.z())
    H_SOC_DS = np.kron(D.x(),S_P.x()) + np.kron(D.y(),S_P.y())+ np.kron(D.z(),S_P.z())
    H_SOC_PS = np.kron(P.x(),S_P.x()) + np.kron(P.y(),S_P.y())+ np.kron(P.z(),S_P.z())  
    H_SOC_PS[np.absolute(H_SOC_PS)<1e-6]=0
    H_SOC_DS[np.absolute(H_SOC_DS)<1e-6]=0
    H_SOC_SS[np.absolute(H_SOC_SS)<1e-6]=0


    file_name="../../Unit_cell_composition/test/wannier90_V3.win"
    H_SOC = generate_H_SOC_V2(file_name)
    H_SOC[np.absolute(H_SOC)<1e-6]=0
    comp=composition_wrapper(file_name)
    comp.print_composition()
    
    ref_point=0
    for atom in comp:
        split_orb=atom.split_orbitals_by_L()
        for l_subspace in split_orb:
            print("Subspace of ", l_subspace)
            H_SOC_block = H_SOC[ref_point:ref_point+2*len(l_subspace),ref_point: ref_point+2*len(l_subspace)]
            
            if l_subspace[0][0]=='s':
                l=0
            elif l_subspace[0][0]=='p':
                l=1
            elif l_subspace[0][0]=='d':
                l=2
            else:
                exit("We have a problem")
            L=AngularMomentum(l)
            L.to_Cartesian(l_subspace)
            H_SOC_ref=np.kron(L.x(),S_P.x()) + np.kron(L.y(),S_P.y())+ np.kron(L.z(),S_P.z())
            H_SOC_ref[np.absolute(H_SOC_ref)<1e-6]=0
            if ~np.any(H_SOC_ref-H_SOC_block):
                print("Test : Passed")
            else:
                exit("Test : Failed")

            ref_point += 2*len(l_subspace)
