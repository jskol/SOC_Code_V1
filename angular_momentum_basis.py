'''
nested_dict = { 'dictA': {'key_1': 'value_1'},
                'dictB': {'key_2': 'value_2'}}
print("hello")
print(nested_dict)
print(nested_dict['dictA']['key_1'])
'''
'''
1) Zainicjować słownik angular_momentum (słownik-słowników) z momentem pędu z macierzami
    Jak używać
    angular_momentum[wartość L][nazwa m_L]
    np.
    angular_momentum[0.5]["z"]= np.array((1,0),(0,-1))
    angular_momentum[2]["xz"] =....
'''
################################################################################
import numpy as np

angular_momentum = { "1/2": {
							'x': np.array([[0,1],[1,0]], dtype=complex),
							'y': 1j * np.array([[0,-1],[1,0]], dtype=complex),
							'z': np.array([[1,0],[0,-1]], dtype=complex)
							}

}

# print("--------------")
#print(angular_momentum['1/2']['x'])
#print(angular_momentum['1/2']['y'])
#print(angular_momentum['1/2']['z'])
# for key,value in angular_momentum['1/2'].items():
# 	print('s=',key, " : \n ",value)


'''
2) Zrobić testy (if __name__=="__main__":) -> w ramach jednego skrptu
    -) czy zwraca dobrą macierz ?
    -) czy relacje komutacyjne są ok, kwadrat macierzy =1 ?

3) stworzyć oddzielnie skrypt testujący s=1/2 ( zaczyać od import angular_momentum i robić test komutacji itd.)   
'''



#Function calculating angular momentum matrices for given l value
def angular_momentum_matrices(l, hbar=1):
	dim = int(2 * l + 1)
	m_vals = np.array([l - i for i in range(dim)])
	# print("m_vals =\n", m_vals) #

    # Lz is diagonal
	Lz = hbar * np.diag(m_vals)

    # Ladder operators
	L_plus = np.zeros((dim, dim), dtype=complex)
	L_minus = np.zeros((dim, dim), dtype=complex)

	for i in range(dim - 1):
		m = m_vals[i + 1]  # current m (for L+ from |m> to |m+1>)
		c = hbar * np.sqrt(l * (l + 1) - m * (m + 1))
		L_plus[i, i + 1] = c
		L_minus[i + 1, i] = c
	# print("L_p=\n", L_plus)		#
	# print("m=\n", L_minus)		#

    # Lx and Ly from L+ and L-
	Lx = 0.5 * (L_plus + L_minus)
	Ly = -0.5j * (L_plus - L_minus)

	return Lx, Ly, Lz

angular_momentum_matrices(0.5)
Lx, Ly, Lz = angular_momentum_matrices(0.5)

# print("Lx =\n", Lx)
# print("Ly =\n", Ly)
# print("Lz =\n", Lz)

#print("end of file") #for tests

if __name__=="__main__":
	for key,value in angular_momentum['1/2'].items():
		print('s=',key, " : \n ",value)