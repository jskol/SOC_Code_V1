import numpy as np
from UnitCell import UnitCell,Atom

def get_projections(file_name="wannier90.win"):
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

            el=comp.get(temp[0])
            if el == None:
                comp.update({temp[0] : [temp[1]]}) # Add new atom
            else:
                new_data = comp.get(temp[0])
                new_data.append(temp[1])

        if(line.rstrip() == "begin projections"):
            projectors_flag=True
    
    f.close()

    return comp


#Update compostion by multiplicity of each atom type
def get_compostion(comp: dict ,file_name="wannier90.win")-> UnitCell:
    f=open(file_name,'r')
    res=UnitCell()
    comp_flag=False
    #generate vector of multiplicities
    for line in f.readlines():
        if(line.rstrip() == "end atoms_cart"):
            break
        if(comp_flag):
            current_line=line.split()
            el_name=current_line[0]
            el=comp.get(el_name)
            if(el==None):
                continue # irrelevant atom
            else:
                position=[]
                for i in np.arange(3):
                    position.append(current_line[1+i])
                orbitals=comp[el_name]
                atom_temp=Atom(name=el_name,orbitals=orbitals,position=position)
                res.add_atom(atom_temp)            
        if(line.rstrip() == "begin atoms_cart"):
            comp_flag=True   
    f.close()
    return res