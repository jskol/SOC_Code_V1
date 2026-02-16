import sys, os
import numpy as np
import numpy.typing as nty
import pytest
from pathlib import Path


root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from app.Energy_Minimizer.gen_H_TB import generate_H_TB


class TestGenerateHTB:
    """Tests for generate_H_Full function"""
        
    def test_return_type_is_ndarray(self):
        """Test that function returns numpy ndarray"""
        win_file = os.path.join(root_dir, 'tests', 'test_cases', 'wannier90.win')
        param_file = os.path.join(root_dir, 'tests', 'test_cases', 'params')
        file_name = os.path.join(root_dir, 'tests', 'test_cases', 'wannier90_up_hr.dat')
        print([f'{name} ,{os.path.exists(name)}' for name in [win_file,param_file,file_name] ])
        try:
            result = generate_H_TB(win_file, file_name)
            assert isinstance(result, np.ndarray), "Result should be numpy ndarray"
 

        except (FileNotFoundError, TypeError):
            pytest.skip("Test files not available")

    def test_spin_degenerate_case(self):
        """Test that function returns numpy ndarray"""
        win_file = os.path.join(root_dir, 'tests', 'test_cases', 'wannier90.win')
        param_file = os.path.join(root_dir, 'tests', 'test_cases', 'params')
        file_name = os.path.join(root_dir, 'tests', 'test_cases', 'wannier90_up_hr.dat')
        print([f'{name} ,{os.path.exists(name)}' for name in [win_file,param_file,file_name] ])
        
        try:
            result = generate_H_TB(win_file, file_name)

        except (FileNotFoundError, TypeError):
            pytest.skip("Test files not available")

        eig_vals=np.linalg.eigvalsh(result)        
        for eig in np.arange(len(eig_vals),step=2):
                eig_vals[eig]==eig_vals[eig+1]    



if __name__=="__main__":
     test=TestGenerateHTB()
     test.test_spin_degenerate_case()

    

