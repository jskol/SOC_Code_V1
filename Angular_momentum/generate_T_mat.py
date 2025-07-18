import numpy as np
import sys


def generate_T_mat(l :float):
	'''
	For every |number> in definition, we take it's complex conjugate,
	because elements in our matrix are in the form <number|cartesian>.
	'''
	if l==0:
		res=np.array([1])
	elif l==1:
		'''
		Wannier90 - order of orbitals is:
		pz, px, py
		'''
		res=np.array((
			(0.,1.,0.),
			(-1./np.sqrt(2),0.,1./np.sqrt(2) ),
			(-1.j/np.sqrt(2),0.,-1.j/np.sqrt(2))
		),dtype=np.complex128)
	elif l==2:
		'''
		Wannier90 - order of orbitals is:
		dz2, dxz, dyz, dx2-y2, dxy
		'''
		res=np.array((
			(0.,0.,1.,0.,0.),
			(0.,-1./np.sqrt(2),0.,1./np.sqrt(2),0.),
			(0.,-1.j/np.sqrt(2),0.,-1.j/np.sqrt(2),0.),
			(1./np.sqrt(2),0.,0.,0.,1./np.sqrt(2)),
			(1.j/np.sqrt(2),0.,0.,0.,-1.j/np.sqrt(2))
		),dtype=np.complex128)
	else:
		sys.exit("Undefind l-subspace") ## Handle this issue
	return res

if __name__=="__main__":
    test_cases=[0, 1, 2]
    for l in test_cases:
        print(generate_T_mat(l))


