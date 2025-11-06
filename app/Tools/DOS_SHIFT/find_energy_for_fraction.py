import numpy as np


# This is a helper function fog main= find_energy_for_fraction
def cumulative_integral(E: np.ndarray, dos: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Computes the cumulative integral of the DOS using the trapezoidal rule.

    Parameters
    E : Energy values (in eV).
    dos : Density of states at corresponding energies from E.
    """
    sort_idx = np.argsort(E)
    E_sorted = E[sort_idx]
    dos_sorted = dos[sort_idx]

    cum_at_E = np.zeros_like(E_sorted)
    cum_at_E[1:] = np.cumsum(
        0.5 * (dos_sorted[1:] + dos_sorted[:-1]) * (E_sorted[1:] - E_sorted[:-1])
    )

    return E_sorted, cum_at_E


def find_energy_for_fraction(E: np.ndarray, DOS: np.ndarray, fraction: float) -> float:
    """
    Finds the energy where the cumulative integral equals a given fraction of the total.

    Parameters
    E : Energy values 
    dos : Density of states at corresponding energies from E.
    fraction : Target fraction of occupation.
    """
    E_sorted,DOS_int=cumulative_integral(E, DOS) # collect DOS data into cummulative intgral bins 
    Ntot = DOS_int[-1]
    target = fraction * Ntot
    if fraction > 1 or fraction <0:
        raise RuntimeError("Fraction has to be in the [0:1] range")

    if fraction == 0:
        return E_sorted[0]
    elif fraction == 1:
        return E_sorted[-1]
    else:
        idx = np.searchsorted(DOS_int, target)
        if idx == 0:
            return E[0]

        E1, E2 = E_sorted[idx - 1], E_sorted[idx]
        N1, N2 = DOS_int[idx - 1], DOS_int[idx]

        t = 0.5 if N1 == N2 else (target - N1) / (N2 - N1) # pick the middle of the gap in case of an insulator or point between the two points (metal) using Newton method
        return E1 + t * (E2 - E1)

