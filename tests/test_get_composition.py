import sys,os
import numpy as np
import pytest

curr_dir=os.path.dirname(os.path.abspath(__file__)) #
parent_dir = os.path.dirname(curr_dir) #get parent
sys.path.append(parent_dir)
from app.Unit_cell_composition.read_win import composition_wrapper

files=['wannier90.win','wannier90_V2.win','mnte.win','mnte_V2.win','wannier90_V3.win','wannier90_V4.win']
test_case_dir='test_cases/'
@pytest.mark.parametrize("f_name",
                         list(map(lambda x: test_case_dir+x,files))
)

def test_get_composition( f_name):    
    unit_cell=composition_wrapper(f_name)
    unit_cell.print_composition()
    #unit_cell.plot_unit_cell()
    assert 1