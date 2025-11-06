import numpy as np
from UnitCell import UnitCell,Atom

allowed_orbital_names=[
's','l=0',
'px','py','pz','p','l=1',
'dxy','dyz','dxz','dx2-y2','dz2','d','l=2'
]

def return_orb_set(name :str)->list:
    '''
    Check if the projection name is in the list
    and return either the full set of orbitals for a given 
    angular momentum or just the name passed 
    (allowing for using the subset of L-block)
    '''
    if name in allowed_orbital_names:
        if (name =='s') or (name == 'l=0'):
            return ['s']
        elif ((name == 'p') or (name == 'l=1')):
            return ['px','py','pz']
        elif ((name== 'd') or (name == 'l=2')):
            return ['dxy','dyz','dxz','dx2-y2','dz2']
        else:
            return [name]
    else:
        exit("Undefined orbital name")    

def get_projections(file_name="wannier90.win"):
    '''
    Function extracting projections
    used in Wannierization procedure

    Returns:
    dictionary with the element name and its set of 
    orbitals it is projected onto within the 
    Wannierization
    '''
    f=open(file_name,'r')
    comp={}
    projectors_flag=False
    for line in f.readlines():
        if(line.rstrip() == "end projections"):
            break
        
        if(projectors_flag):
            temp=line.replace(' ','').split(":")
            #temp[0] -name of the element
            #temp[1] - name of the orbital
            #the rest of the line is irrelevant (for now in future we need to reslove projections passed using ";" symbol)
            ang_mtm=temp[1].strip() # remove whitespaces
            element_name=temp[0].strip()
            comp.get(temp[0])
            temp_orb_name_list=return_orb_set(ang_mtm)
            if comp.get(element_name) == None:
                comp.update({element_name : temp_orb_name_list})
            else:
                new_data = comp.get(element_name)
                new_data.extend(temp_orb_name_list)

        if(line.rstrip() == "begin projections"):
                    projectors_flag=True
    f.close()
    return comp

#Update compostion by multiplicity of each atom type
def get_composition(comp: dict ,file_name="wannier90.win")-> UnitCell:
    '''
    function extracting the composition of unit cell
    taking into consideration the projections used in the 
    Wannierization. 
    
    Returns:
    A UnitCell object, which is a list of Atoms (objects with a name, set of projections, and its position)
    '''
    f=open(file_name,'r')
    res=UnitCell()
    
    import re
    comp_flag=False
    #generate vector of multiplicities
    for line in f.readlines():
        # special care as the wannier can have 
        # positions of atoms in "cart" -Cartesian
        # or fractions of primit shifts "frac"
        if( re.search(r'end atoms_',line.rstrip())):
            break

        if(comp_flag):
            current_line=line.split()
            el_name=current_line[0]
            el=comp.get(el_name)
            if(el==None):
                continue # irrelevant atom
            else:
                #Construnting Atom-object (name,position, orbitals)
                position=[]
                for i in np.arange(3):
                    position.append(float(current_line[1+i]))
                orbitals=comp[el_name]
                atom_temp=Atom(name=el_name,orbitals=orbitals,position=position)
                res.add_atom(atom_temp)            
        
        if(re.search(r'begin atoms_', line.rstrip()) ):
            comp_flag=True
    f.close()
    return res

def composition_wrapper(file_name="wannier90.win")-> UnitCell:
    projetions_dict=get_projections(file_name)
    res=get_composition(projetions_dict,file_name)
    return res