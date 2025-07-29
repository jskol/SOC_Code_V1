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
#from create_H_SOC import generate_H_SOC
#from read_win import get_projections, get_composition, composition_wrapper


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
    print("is H_SOC(D) = -H_SOC(P): ", ~np.any(sum_mat))
    
