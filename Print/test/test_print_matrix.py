import numpy as np
import re
from termcolor import colored
from datetime import datetime
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'Unit_cell_composition'))
from create_Hamiltonian import create_hamiltonian

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from print_matrix import save_to_file


if __name__=="__main__":
