import sys
import numpy as np
sys.path.append('..')


from read_win import get_projections,get_compostion


if __name__=="__main__":
    proj=get_projections()
    for els in proj:
        print(els, proj[els])

    unit_cell=get_compostion(proj)
    unit_cell.print_composition()