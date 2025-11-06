import sys
import numpy as np

sys.path.append('../app/Unit_cell_composition')
from read_win import composition_wrapper

if __name__=="__main__":
    test_case_dir='test_cases/'
    file_names=['wannier90.win','wannier90_V2.win','mnte.win','mnte_V2.win','wannier90_V3.win','wannier90_V4.win']
    for in_file in file_names[:]:    
        unit_cell=composition_wrapper(test_case_dir+in_file)
        unit_cell.print_composition()
        unit_cell.plot_unit_cell()