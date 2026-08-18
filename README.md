# SOC_CODE 

## General info
This project aims to help in understanding the role of various spin structures (Magnetic LRO + SOC) on the measurable quantities of a given system.
The spin structures can be added to a model tight-binding Hamiltonian(TBH) by hand or by provided scripts (in-progress). 
The code fits between the wannierization step, which maps the DFT problem onto a tight-binding Hamiltonian, and the wanniertools step, which extracts the measurable
quantities from the TBH.

## Usage
To run the code, just execute main.py with flags. For more information, run 
`python3 app/main.py -h`

## Requirements
To run the code, one needs just Python (3.+) with NumPy and some basic modules (see requirements.txt).


## Contributors
This project was developed by MagTop members: Jan Skolimowski, Carmine Autieri, Kamil Jamroszczyk and Mathews Benny

## Citation

Please cite both the GitHub repository and the accompanying publication in any work that makes use of this code. Proper citation helps acknowledge the software implementation as well as the scientific methodology underlying it.

### Software

Jan Skolimowski, Carmine Autieri, Kamil Jamroszczyk, and Mathews Benny, *SOC_Code_V1*. GitHub Repository.

**Repository:** https://github.com/jskol/SOC_Code_V1

### Publication

Mathews Benny, Xujia Gong, Kamil Jamroszczyk, Amar Fakhredine, Giuseppe Cuono, Rajibul Islam, Jan Skolimowski, and Carmine Autieri.  
*Phys. Rev. B* **114**, 014429 (2026).  
**DOI:** 10.1103/rjg7-n1tc
