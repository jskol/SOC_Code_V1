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
    D.to_Cartesian(['dxy','dyz','dxz'])


    H_SOC_DS = np.kron(D.x(),S.x()) + np.kron(D.y(),S.y())+ np.kron(D.z(),S.z())
    H_SOC_PS = np.kron(P.x(),S.x()) + np.kron(P.y(),S.y())+ np.kron(P.z(),S.z())     

    print("H_SOC (D-subspace):\n",H_SOC_DS)
    print("H_SOC (P-subspace):\n",H_SOC_PS)
