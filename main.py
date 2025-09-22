import argparse
import sys

sys.path.append('Unit_cell_composition')
from Update_win_Ham import merged_with_SOC_wrapper

sys.path.append('Print')
from print_matrix import save_to_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Description of a program."
    )
    parser.add_argument("--win", required=True, type=str)
    parser.add_argument("--hr", required=True, nargs="+", type=str)
    parser.add_argument("--param", required=True, type=str)
    parser.add_argument("--out", required=False, type=str)
    args = parser.parse_args()

    win_file = args.win
    param_file = args.param
    files_to_merge = args.hr   # put hr file(s) in a list
    out_file = args.out

    result = merged_with_SOC_wrapper([win_file], param_file, files_to_merge)

    save_to_file(result, files_to_merge[0], out_file)

    # print(files_to_merge)
    # print(win_file)
    # print(param_file)
