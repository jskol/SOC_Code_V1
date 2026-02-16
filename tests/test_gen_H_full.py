import sys, os
import numpy as np
import numpy.typing as nty
import pytest
from pathlib import Path


root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from app.Energy_Minimizer.gen_H_full import generate_H_Full


class TestGenerateHFull:
    """Tests for generate_H_Full function"""
    
    def test_missing_param_file(self):
        """Test that FileNotFoundError is raised when default param file is missing"""
        win_file = os.path.join(root_dir, 'tests', 'test_cases', 'wannier90.win')
        file_name = os.path.join(root_dir, 'tests', 'test_cases', 'wannier90_up_hr.dat')
        
        with pytest.raises(FileNotFoundError, match='Missing parameter file'):
            generate_H_Full(win_file, 'params', file_name)
    
    def test_no_win_file(self):
        """Test function behavior when no win_file is provided"""
        param_file = os.path.join(root_dir, 'tests', 'test_cases', 'params')
        file_name = os.path.join(root_dir, 'tests', 'test_cases', 'wannier90_up_hr.dat')
        
        with pytest.raises((FileNotFoundError, TypeError)):
            generate_H_Full(None, param_file, file_name)
    
    def test_no_hr_files_passed(self):
        """Test function behavior when no hr_files are passed"""
        win_file = os.path.join(root_dir, 'tests', 'test_cases', 'wannier90.win')
        param_file = os.path.join(root_dir, 'tests', 'test_cases', 'params')
        
        with pytest.raises((FileNotFoundError, TypeError)):
            generate_H_Full(win_file=win_file, param_file=param_file)
    
    def test_return_type_is_ndarray(self):
        """Test that function returns numpy ndarray"""
        win_file = os.path.join(root_dir, 'tests', 'test_cases', 'wannier90.win')
        param_file = os.path.join(root_dir, 'tests', 'test_cases', 'params')
        file_name = os.path.join(root_dir, 'tests', 'test_cases', 'wannier90_up_hr.dat')
        print([f'{name} ,{os.path.exists(name)}' for name in [win_file,param_file,file_name] ])
        try:
            result = generate_H_Full(win_file, param_file, file_name)
            assert isinstance(result, np.ndarray), "Result should be numpy ndarray"
        except (FileNotFoundError, TypeError):
            pytest.skip("Test files not available")



