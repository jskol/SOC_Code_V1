import sys,os
import numpy as np

sys.path.append('..')
from Transfer_Matrix import Trasfer_Matrix

sys.path.append(os.path.join(os.path.dirname(__file__), '..','..', 'Unit_cell_composition'))
from read_win import composition_wrapper

if __name__=="__main__":
    test_case_loc='../../test_cases/'
    win_names=['mnte.win','wannier90.win', 'wannier90_V3.win']
    for win in win_names:
        
        print("\nReading from :", win)
        l=Trasfer_Matrix([test_case_loc+win],print_details=False)
        sq= l.T@l
        print("Square is giving unity: ", ~np.any(sq-np.eye(l.shape[0])))
        
        # Read the order from win
        comp = composition_wrapper(test_case_loc+win)
        orb_list=[]    
        for atom in comp:
            orb_list=orb_list+ atom.orbitals
        orb_list=np.array(orb_list)
        print("from file", orb_list)
        
        #create a new reordered list
        new_orb_list=[]
        reordered= l@np.arange(len(orb_list)) #vector after trasnformation
        for new_pos in reordered:
            new_orb_list.append(orb_list[int(new_pos)]) #change positions to str-values
        print("after reordering" , np.array(new_orb_list))


        
