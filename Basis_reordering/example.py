import numpy as np
import string



N=4
Mat1=np.zeros((N,N),dtype=object)

for i in np.arange(Mat1.shape[0]):
    for j in np.arange(Mat1.shape[1]):
        Mat1[i][j]='<%s | H | %s >'%(str(i+1),str(j+1))

print("\nInitial ordering of elements\n",Mat1)

#Exchange 1-3
x,y=1,2

T_mat=np.eye(N,dtype=int)
T_mat[x-1][x-1]=0
T_mat[y-1][y-1]=0
T_mat[x-1][y-1]=1
T_mat[y-1][x-1]=1

print("\nTransfer Matrix\n",T_mat)

Mat1_T=np.matrix(T_mat).T@Mat1@T_mat 
print("\nAfter exchanging(%i with %i):\n"%(x,y),Mat1_T)



