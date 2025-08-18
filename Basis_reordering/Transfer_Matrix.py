import numpy as np 
import sys,os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Unit_cell_composition'))
 
from read_win import composition_wrapper

def Trasfer_Matrix(*filenames,print_details=False)->np.matrix:
    '''
    Function that takes a file name and returns
    a transfer matrix T from atom-wise basis vector v
    to an oribital-wise basis vector w
            T@v = w
    thus matrix M that takes atom-wise basis vectors
    becomes matrix H in orbital-wise basis
            H = T@M@T^+
    
    '''
    
    if(len(filenames) == 0):
        win_file='wanner90.win'
    elif (len(filenames) == 1):	#if we pas 1 file, both are the same
        win_file = filenames[0]
    else:						#in other cases we have error
        print("error - file")
        exit(1)

    comp = {}
    comp = composition_wrapper(win_file)
    if print_details:
        comp.print_composition()
    
    orb_list=[]    
    for atom in comp:
        orb_list=orb_list+ atom.orbitals
    
    orbs_dict={}
    for orb in orb_list:
        if orb not in orbs_dict.keys():
            name_loc= [pos for pos, names in enumerate(orb_list) if names == orb]
            orbs_dict.update({orb : name_loc})
    list_of_pos=[]
    for pos in orbs_dict.values():
        list_of_pos = list_of_pos+pos
    
    if print_details:
        print("positions pre sorting", orb_list)
        print("positions after sorting ", list_of_pos)
    
    T_mat=np.zeros((len(orb_list),len(orb_list)))
    for old,new in enumerate(list_of_pos):
        T_mat[old,new]=1

    if print_details:
        print(T_mat)
    
    return T_mat
    
    
