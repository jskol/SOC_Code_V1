import sys

sys.path.append('..')

from read_params import read_params,immerse_params_in_composition
from read_win import composition_wrapper

if __name__=="__main__":
    res=read_params()
    comp=composition_wrapper()

    print("\nPrint prams\n")
    params_names=['magnetic-field','SOC']
    for prop in params_names:
        print("\nInitial read\n")
        for mag in res[prop]:
            print(mag)

        res2=immerse_params_in_composition(res,comp)
        print("\n%s : After matching .win\n"%prop)
        for mag in res2[prop]:
            print(mag)
