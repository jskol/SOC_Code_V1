import argparse

import sys
sys.path.append('Unit_cell_composition')

from Update_win_Ham import merged_with_SOC_wrapper

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Description of a program."
    )
    parser.add_argument("--win", required=True, type=str)
    parser.add_argument("--hr", required=True, type=str)
    parser.add_argument("--param", required=True, type=str)
    parser.add_argument("--out", required=True, type=str)
    args = parser.parse_args()

    win_file = args.win
    param_file = args.param
    files_to_merge = [args.hr]   # put hr file(s) in a list

    result = merged_with_SOC_wrapper(win_file, param_file,files_to_merge)
