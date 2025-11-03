import numpy as np

def read_DOS(fname: str, col_num: int)-> tuple[np.ndarray,np.ndarray]:
        '''
        Function reads the DOS data from the
        fname file picking energy column (0-th) and
        a chosen broadened DOS column (col_num enumarted from "1")
        '''
        data=np.loadtxt(fname,comments='#')
        if len(data[:,0])<2:
            raise RuntimeError("Not enough points to integrate")
        else:
            if col_num > len(data[1,1:]):
                raise RuntimeError("Chosen column is not in the data file")
            elif col_num < 1:
                raise RuntimeError("DOS-column starts from 1")
            
            else:
                return data[:,0],data[:,col_num]

