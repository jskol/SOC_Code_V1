
import argparse

def read_params()-> tuple[str,int,float]:
    parser = argparse.ArgumentParser(
        prog='dos_shift.py',
        description='Reads a DOS text file with columns:\n \
                    E(eV)  DOS_col1  DOS_col2  ... DOS_colN \n\
                    Integrates the chosen DOS column using the trapezoidal rule and \
                    finds the energy E where the cumulative integral reaches FRAC \
                    of the total DOS.\n',
        epilog=' The DOS-file name is REQUIRED \n'
    )
    parser.add_argument(
        "--dosfile",
        required=True, 
        type= str, 
        help="DOS-file name to process"
        )
    parser.add_argument(
        "--col",
        required=False,
        type=int,
        default=2,
        help="DOS column index (default 2)-> 2nd DOS column after E)."
    )
    parser.add_argument(
        "--frac",
        required=False,
        type= float,
        default=0.6667,
        help='The target fraction of all electrons'
        )
    args = parser.parse_args()

    return args.dosfile, args.col, args.frac



#print("I'm using read_params")

if __name__=="__main__":
    #Here you do the testing 
    fname, col, frac =read_params()
    print ( fname, col, frac)