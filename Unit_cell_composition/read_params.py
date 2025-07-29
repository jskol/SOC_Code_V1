import numpy as np


from read_win import composition_wrapper
from UnitCell import UnitCell

def read_params(param_file='params'):
    ''' 
    Read parameters like SOC and (local) magnetic fields
    '''
    params=['SOC','magnetic-field']
    res={}
    for param in params:
        f=open(param_file,'r')
        param_flag=False
        end_line="end %s"%param
        begin_line="begin %s"%param
        res_temp=[]
        for line in f.readlines():
            if len(line.split())== 0: # Skip empty lines 
                    continue
            
            if(line.rstrip() == end_line) or (line.split()[0]=='end' and line.split()[-1]==param) :
                break
        
            if(param_flag):
                
                #temp[0] -name of the element
                #temp[1:4] - location
                #temp[4:]- parameters
                temp_line=[]
                for it,entry in enumerate(line.split()):
                    if it == 0:
                        temp_line.append(entry)
                    else:
                        temp_line.append(float(entry))

                res_temp.append(temp_line)

            if(line.rstrip() == begin_line):
                param_flag=True
        
        f.close()
        res.update({param : res_temp})
    return res


def immerse_params_in_composition(params: list, unitcell : UnitCell):
    '''
    Function that aligns the atoms in params with atoms in UnitCell
    and adds zeros where the parameters are not given
    '''
    res={}
    for key in params.keys():
        temp_vec=[]        
        for atom in unitcell:
            add_zero=True
            if key == 'SOC':
                zero_temp=[0.]
            else:
                zero_temp=[0.,0.,0.]
            num_of_l=len(atom.split_orbitals_by_L()) #number of differnt L-values
            zero = num_of_l*zero_temp
            for atoms_p in params[key]: # look for the matching atom of the unitcell in the list of atoms with given parameters
                if atoms_p[0] == atom.name:
                    if atoms_p[1:4] == atom.position:
                        atom_output=atoms_p
                        for i in np.arange(np.abs(len(atoms_p[4:])-len(zero))): # append zeros if the number of params does not fit the number orbitals
                            atom_output.append(0.)
                        temp_vec.append(atom_output)
                        add_zero=False
                    else:
                        continue
                else:
                    continue     
            
            if add_zero: # if no parames given for this atom add zero
                temp_vec.append([atom.name]+atom.position+ zero)
        res.update({key : temp_vec})
    return res


