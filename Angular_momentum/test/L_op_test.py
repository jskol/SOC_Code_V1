#TODO: To samo co dla Pauliego ale dla L=całkowitego

import sys
import numpy as np
sys.path.append('..')
#from angular_momentum_basis import angular_momentum_matrices
from pauli_test import angular_momentum_operator_test

# for key,value in angular_momentum['1/2'].items():
# 	print("s_%s:\n"%key,value)

print("testing")
angular_momentum_operator_test(1)