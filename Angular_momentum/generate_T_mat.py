import numpy as np
import sys


def generate_T_mat(l :float):
	'''
	Function returns a transfer matrix from
	the Spherical Harmonic to Cartesian coordinates for 
	a given l
	'''
	
	#For every |number> in definition, we take it's complex conjugate,
	#because elements in our transfer matrix are in the form <number|cartesian>.
	
	if l==0:
		res=np.array([1])
	elif l==1:
		'''
		Wannier90 - order of orbitals is:
		pz, px, py
		'''
		res=np.array((
			(0.,1.,0.), #p_z
			(-1./np.sqrt(2),0.,1./np.sqrt(2) ), #p_x
			(-1.j/np.sqrt(2),0.,-1.j/np.sqrt(2)) #p_y
		),dtype=np.complex128)
	elif l==2:
		'''
		Wannier90 - order of orbitals is:
		dz2, dxz, dyz, dx2-y2, dxy
		'''
		res=np.array((
			(0.,0.,1.,0.,0.), #d_z2
			(0.,-1./np.sqrt(2),0.,1./np.sqrt(2),0.), #_xz
			(0.,-1.j/np.sqrt(2),0.,-1.j/np.sqrt(2),0.), #d_yz
			(1./np.sqrt(2),0.,0.,0.,1./np.sqrt(2)), #d_x2-y2
			(1.j/np.sqrt(2),0.,0.,0.,-1.j/np.sqrt(2)) #d_xy
		),dtype=np.complex128)
	else:
		sys.exit("Undefind l-subspace") ## Handle this issue
	return res


def generate_T_mat(l :float,*list_of_orbitals):
	'''
	Function returns a transfer matrix from
	the Spherical Harmonic to Cartesian coordinates for 
	a given l
	additional argument "list_of_orbitals" 
	takes a certain order/subset of orbitals
	to consider
	'''
	
	#For every |number> in definition, we take it's complex conjugate,
	#because elements in our transfer matrix are in the form <number|cartesian>.
	
	if l==0:
		res=np.array([1])
	elif l==1:
		'''
		Wannier90 - order of orbitals is:
		pz, px, py
		'''
		res=np.array((
			(0.,1.,0.), # p_z
			(-1./np.sqrt(2),0.,1./np.sqrt(2) ), # p_x
			(-1.j/np.sqrt(2),0.,-1.j/np.sqrt(2)) # p_y
		),dtype=np.complex128)

		if (len(list_of_orbitals) >0): #consider user-defined ordering
			res_temp=res.copy()
			res=[]
			for orb in list_of_orbitals[0]:
				if orb=='px':
					res.append(res_temp[1,:])
				elif orb=='py':
					res.append(res_temp[2,:])
				elif orb=='pz':
					res.append(res_temp[0,:])

				else:
					exit('wrong orbital type: %s'%orb)
			res=np.array(res,dtype=np.complex128)
	elif l==2:
		'''
		Wannier90 - order of orbitals is:
		dz2, dxz, dyz, dx2-y2, dxy
		'''
		res=np.array((
			(0.,0.,1.,0.,0.), # d_z2
			(0.,-1./np.sqrt(2),0.,1./np.sqrt(2),0.), # d_xz
			(0.,-1.j/np.sqrt(2),0.,-1.j/np.sqrt(2),0.), # d_yz
			(1./np.sqrt(2),0.,0.,0.,1./np.sqrt(2)), # d_x2-y2
			(1.j/np.sqrt(2),0.,0.,0.,-1.j/np.sqrt(2)) # d_xy
		),dtype=np.complex128)
		if (len(list_of_orbitals) >0): #consider user-defined ordering
			res_temp=res.copy()
			res=[]
			for orb in list_of_orbitals[0]:
		
				if orb=='dz2':
					res.append(res_temp[0,:])
				elif orb=='dxz':
					res.append(res_temp[1,:])
				elif orb=='dyz':
					res.append(res_temp[2,:])
				elif orb=='dx2-y2':
					res.append(res_temp[3,:])
				elif orb=='dxy':
					res.append(res_temp[4,:])
				else:
					exit('wrong orbital type: %s'%orb)
			res=np.array(res,dtype=np.complex128)

	else:
		sys.exit("Undefind l-subspace") ## Handle this issue
	return res




if __name__=="__main__":
	test_cases=[0, 1, 2]
	for l in test_cases[1:]:
		print(generate_T_mat(l))


	print(generate_T_mat(1),"\n\n\n")
	print(generate_T_mat(1),"\n")
	print(generate_T_mat(1,['pz','px','py']),"\n")
	print(generate_T_mat(1,['px','py','pz']),"\n")
	print(generate_T_mat(1,['px','pz']),"\n\n")
	
	print("Should give an error:")
	print( generate_T_mat(1,['px','dz2']))
			

		


