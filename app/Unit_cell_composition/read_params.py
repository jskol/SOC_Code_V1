import numpy as np
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from read_win import composition_wrapper
from UnitCell import UnitCell

def read_params(param_file='params'):
    ''' 
    Read parameters like SOC and (local) magnetic fields
    and return a dictionary of parameters that were in the 
    param_file
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

def immerse_params_in_composition(params: dict, unitcell : UnitCell):
    '''
    Function that aligns the atoms in params with atoms in UnitCell
    and adds zeros where the parameters are not given and returns a dictionary
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

def read_params_wrapper(param_file='params', wannier_in_file=None,unit_cell=None):
    '''
    function wrapper that depending on the supplied compostion
    either from wannier file or by unit cell obejects
    prepares the parameters dictionary for further calculations
    '''
    print(wannier_in_file)
    res_temp=read_params(param_file)
    if ((wannier_in_file==None) and (unit_cell==None)):   
        exit("One has to pass either .win file or the unit-cell composition")
    elif(unit_cell==None):
        unit_cell=composition_wrapper(wannier_in_file)
    elif((wannier_in_file != None) and (unit_cell != None)):
        exit("Pick either .win file or unit_Cell")
    
    return immerse_params_in_composition(res_temp,unit_cell)


def gen_template(wannier_in_file=None, out_dir=os.getcwd()):
    '''
    function generating an empty or filled with zeros
    properly defined params file
    '''

    unit_cell=composition_wrapper(wannier_in_file)
    
    with open(os.path.join(out_dir,'params'),'w') as f:
        f.write('#Name #x #y #z #m_r # m_theta #m_phi\n')
        f.write('begin magnetic-field\n')
        if wannier_in_file != None:
            for atom in unit_cell:
                out_str='%s'%atom.name
                for coord in atom.position:
                    out_str += ' %s'%coord
                out_str += ' 0 0 0\n'
                f.write(out_str)
        f.write('end magnetic-field\n')

        f.write('#Name #x #y #z #lambda_SOC\n')
        f.write('begin SOC\n')
        if wannier_in_file != None:
            for atom in unit_cell:
                out_str='%s'%atom.name
                for coord in atom.position:
                    out_str += ' %s'%coord
                out_str += ' 0\n'
                f.write(out_str)
        f.write('end SOC')


