import sys
import numpy as np
sys.path.append('..')


from read_win import composition_wrapper


if __name__=="__main__":


    #for els in proj:
    #    print(els, proj[els])
    file_names=['wannier90.win','mnte.win','mnte_V2.win']
    for in_file in file_names[:]:    
        unit_cell=composition_wrapper(in_file)
        unit_cell.print_composition()
        unit_cell.plot_unit_cell()