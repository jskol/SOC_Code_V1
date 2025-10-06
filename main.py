import argparse
import sys
import os

sys.path.append('Unit_cell_composition')
from Update_win_Ham import merged_with_SOC_wrapper

sys.path.append('Print')
from print_matrix import save_to_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='main.py',
        description="Code adds SOC and local magnetic fields onto a wannierized TB model",
        epilog="If no --hr is/are provided then a template for the param file is generated"
    )
    parser.add_argument("--win", required=True, type=str,help=" provide a path to wannier_in_file for the lattice geometry and its chemical compostion")
    parser.add_argument("--hr", required=False, nargs="+", type=str,help=" provide a path to parameters of the wannierized TB model")
    parser.add_argument("--param", required=False, type=str,default='params',help="provide path to the paramfile for the strengths of the model SOC and Mag-Fields")
    parser.add_argument("--out", required=False, type=str, default='out.dat', help="provde the name of the ouput file, default name out.dat")
    args = parser.parse_args()

    win_file = args.win
    param_file = args.param
    files_to_merge = args.hr   # put hr file(s) in a list
    out_file= args.out

    if(files_to_merge== None and (not os.path.isfile('./param'))):
        from read_params import gen_template
        gen_template(win_file)            
        exit("Generating a template param file")
    
    else:
        # Set of sanity checks
        if(files_to_merge== None):
            exit("Please provide the names of files with the wanniereized TB model paramters.")
        else:
            for hr_name in files_to_merge:
                if not os.path.isfile(hr_name):
                    exit("Could not find ",hr_name )
        if( not os.path.isfile(param_file)):
            exit("Could not find ", param_file)
        
        ## If all is good run the calculations

        result = merged_with_SOC_wrapper([win_file], param_file, files_to_merge)
        save_to_file(result, files_to_merge, out_file)

