#!/usr/bin/env python3
"""
dos_shift.py

Usage:
    python dos_shift.py --dosfile DOS_FILENAME [--col COL=2] [--frac FRAC = 0.6667]

Description:
    Reads a DOS text file with columns:
      E(eV)  DOS_col1  DOS_col2  ... DOS_colN
    Integrates the chosen DOS column using the trapezoidal rule and
    finds the energy E where the cumulative integral reaches FRAC
    of the total integrated DOS.

Example:
    python dos_shift.py dos.dat --col 2
"""

import numpy as np
from typing import Tuple


from read_DOS import read_DOS
from find_energy_for_fraction import find_energy_for_fraction

from read_params import read_params

if __name__ == "__main__":

    fname, col, frac = read_params()
    E, dos = read_DOS(fname, col)
    E23 = find_energy_for_fraction(E, dos, frac)
    print(f"{E23:.8f} eV")
