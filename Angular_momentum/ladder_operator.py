import numpy as np
#TODO: Komentarz jak to działa


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
