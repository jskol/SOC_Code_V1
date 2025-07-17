import sys
import numpy as np
sys.path.append('..')
from angular_momentum_basis import angular_momentum


for key,value in angular_momentum['1/2'].items():
	print("s_%s:\n"%key,value)

#test Norms
mats=[x for x in angular_momentum['1/2'].items()]

for i in np.arange(len(mats)):
	diff=mats[i][1]@mats[i][1] - np.eye(2)
	diff[np.absolute(diff)<1e-6]=0
	print("Testing if S_%s ^2 = 1"%mats[i][0], " : ", ~np.any(diff))

#Testing commutations
for i in np.arange(len(mats)):
		s1=mats[i][1]
		s2=mats[(i+1)%len(mats)][1]
		s3=mats[(i+2)%len(mats)][1]

		#Proper order with Levi-Civita=1
		diff= s1@s2 - s2@s1 -2.j*s3
		diff[np.absolute(diff)< 1e-6]=0
		print("Testing if [S_%s,S_%s]=2iS_%s"%(mats[i][0],mats[(i+1)%len(mats)][0],mats[(i+2)%len(mats)][0])," : ", ~np.any(diff))
		
		#Permutated order with Levi-Civita=-1
		diff2= s1@s3 - s3@s1 +2.j*s2
		diff2[np.absolute(diff2)< 1e-6]=0
		print("Testing if [S_%s,S_%s]=-2iS_%s"%(mats[i][0],mats[(i+2)%len(mats)][0],mats[(i+1)%len(mats)][0])," : ", ~np.any(diff2))

