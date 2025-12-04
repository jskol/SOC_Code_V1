import sys,os

curr_dir=os.path.dirname(os.path.abspath(__file__)) #
parent_dir = os.path.dirname(curr_dir)
sys.path.append(parent_dir)
from app.Unit_cell_composition.read_params import read_params, immerse_params_in_composition
from app.Unit_cell_composition.read_win import composition_wrapper

if __name__=="__main__":
    test_case_loc='test_cases/'
    res=read_params(test_case_loc+"params_2_atoms")
    comp=composition_wrapper(test_case_loc+"wannier90_2_atoms.win")
    #comp.print_composition()
    print("\nPrint prams\n")
    params_names=['magnetic-field','SOC']
    for prop in params_names:
        for at in comp:
            print(at.name, " with ", at.orbitals)
        print("\nInitial read\n")
        for mag in res[prop]:
            print(mag)

        res2=immerse_params_in_composition(res,comp)
        print("\n%s : After matching .win\n"%prop)
        for mag in res2[prop]:
            print(mag)

    print("\n\n\nExample of read_params usage :\n",res2.keys())
    print(res2.values())