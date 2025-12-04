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

sys.path.append('../app/Angular_momentum')
from angular_momentum import AngularMomentum

sys.path.append('../app/Unit_cell_composition')
from read_win import composition_wrapper
from UnitCell import get_L_from_orbitals_set_name

sys.path.append('../app/SOC')
from create_H_SOC import generate_H_SOC

### Carmine test #############
S=AngularMomentum(0.5)

def gen_SOC_Mat(l:int, orb_list:list[str])->np.ndarray:
    L=AngularMomentum(l)
    L.to_Cartesian(orb_list)
    H_SOC_temp=np.kron(L.x(),S.x()) + np.kron(L.y(),S.y())+ np.kron(L.z(),S.z())
    H_SOC_temp[np.absolute(H_SOC_temp)<1e-3]=0
    return H_SOC_temp

import pytest
@pytest.mark.parametrize('M1, M2',[
    pytest.param(gen_SOC_Mat(2,['dyz','dxz','dxy']), gen_SOC_Mat(1,['px','py','pz']),id="Right order"),
    pytest.param(gen_SOC_Mat(2,['dxy','dyz','dxz']), gen_SOC_Mat(1,['px','py','pz']),id="Wrong order",marks=pytest.mark.xfail)
    ])
def test_subspace_equivalency(M1,M2):
    sum_mat=M1+M2
    sum_mat[np.absolute(sum_mat)<1e-3]=0 #Remove near-zeros
    print(sum_mat)
    assert ~np.any(sum_mat)

