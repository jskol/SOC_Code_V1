import os
def read_k_space(win_file:str='wannier90.win')->list[list[float]]:
    if not os.path.exists(win_file):
        raise FileNotFoundError(f'{win_file} was not found')
    result=[]
    with open(win_file,'r') as f:
        read_k_points=False
        for line_temp in f:
            line=line_temp.strip()
            
            if line == 'end kpoints':
                continue
            if read_k_points:
                
                result.append(
                    list(map(float,line.split()))
                    )

            if line=='begin kpoints':
                read_k_points=True
    return result


if __name__=="__main__":
    """
    Quick test if this works
    """
    win='tests/test_cases/wannier90.win'
    print(read_k_space(win))