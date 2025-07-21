import numpy as np
from UnitCell import UnitCell,Atom

allowed_orbital_names=[
's','l=0',
'px','py','pz','p','l=1',
'dxy','dyz','dxz','dx2-y2','dz2','d','l=2'
]

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
            #the rest of the line is irrelevant
            ang_mtm=temp[1].strip() # remove whitespaces
            if ang_mtm in allowed_orbital_names:
                element_name=comp.get(temp[0])
                if element_name == None:
                    if ((ang_mtm == 'p') or (ang_mtm == 'l=1')):
                        comp.update({temp[0]: ['px','py','pz']})
                    elif ((ang_mtm == 'd') or (ang_mtm == 'l=2')):
                        comp.update({temp[0]: ['dxy','dyz','dxz','dx2-y2','dz2']})
                    else:
                        comp.update({temp[0] : [ang_mtm]}) # Add new atom
                else:
                    new_data = comp.get(temp[0])
                    new_data.append(ang_mtm)
            else:
                exit('Unknown orbital name %s'%temp[1])
        
        if(line.rstrip() == "begin projections"):
                    projectors_flag=True
    f.close()
    return comp




#Update compostion by multiplicity of each atom type
def get_compostion(comp: dict ,file_name="wannier90.win")-> UnitCell:
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
    res=get_compostion(projetions_dict,file_name)
    return res