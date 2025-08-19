'''
Testing The fact that  SOC projected in the
'dyz','dxz','dxy' subspace is equivalent to 
-H_SOC in the p-subspace stated in 
https://arxiv.org/pdf/1507.06323

Yes, order is important:
[px,py,pz]-> ['dyz','dxz','dxy']
'''

import numpy as np
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'Angular_momentum'))
from angular_momentum import AngularMomentum

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'Unit_cell_composition'))
from read_win import composition_wrapper
from UnitCell import get_L_from_orbitals_set_name

sys.path.append('..')
from create_H_SOC import generate_H_SOC

if __name__=="__main__":
   

    ### Carmine test #############
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
    if ~np.any(sum_mat):
        print("is H_SOC(D) = -H_SOC(P): ", ~np.any(sum_mat), "\n\n") # <- Test From Carmine
    else:
        exit("Carmine test has FAILED!")
    ###################################

