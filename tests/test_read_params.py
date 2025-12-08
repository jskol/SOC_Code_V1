import sys,os
import pytest
curr_dir=os.path.dirname(os.path.abspath(__file__)) #
parent_dir = os.path.dirname(curr_dir)
sys.path.append(parent_dir)
from app.Unit_cell_composition.read_params import read_params, immerse_params_in_composition
from app.Unit_cell_composition.read_win import composition_wrapper


@pytest.mark.parametrize("param_file,composition_file",[
    ("params_2_atoms","wannier90_2_atoms.win"),
    pytest.param("params_3_atoms","wannier90_2_atoms.win",marks=pytest.mark.xfail(raises=FileNotFoundError,reason="Non-existing file passed"))
])
def test_read_params(param_file,composition_file):
    test_case_loc=os.path.join(os.getcwd(),'test_cases/')
    res=read_params(os.path.join(test_case_loc,param_file))
    comp=composition_wrapper(os.path.join(test_case_loc,composition_file))
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

