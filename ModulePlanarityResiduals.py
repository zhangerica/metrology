import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
import glob

dir1 = 'C:\ALICE Upgrade\ITSUsoftwareCMM\ModulePosition'
dir2 = 'C:\ALICE Upgrade\ITSUsoftwareCMM\ModulePlanarity'

CPnum = raw_input('Enter Cold Plate ID: ')

fnames1 = []
fnames2 = []

for f in os.listdir(dir1):
	if f.startswith(CPnum) and f.endswith('.csv'):
		fnames1.append(f)

fnames1 = np.array(fnames1)

for j in range(fnames1.size):
	for i in range(fnames1.size):
		if fnames1[i].find('MODULEPOS'+str(i+1))+1:
			continue
		else:
			fnames1[i], fnames1[fnames1.size-1] = fnames1[fnames1.size-1],fnames1[i]
    
for f in os.listdir(dir2):
	if f.startswith(CPnum) and f.endswith('.csv'):
		fnames2.append(f)

fnames2 = np.array(fnames2)

fnames2.sort()

dx, dy, dz = [], [], []

for i in range(fnames1.size):
	d1 = pd.read_csv(open(dir1+'\\'+fnames1[i]), header = None, usecols=[4,5,6])
	d2 = pd.read_csv(open(dir2+'\\'+fnames2[i]), header = None, usecols=[4,5,6])
	print(d2)

	x1, y1, z1 = pd.DataFrame.get(d1,4).as_matrix(), pd.DataFrame.get(d1,5).as_matrix(), pd.DataFrame.get(d1,6).as_matrix()
	x_temp, y_temp, z_temp = pd.DataFrame.get(d2,4), pd.DataFrame.get(d2,5), pd.DataFrame.get(d2,6)
	x2, y2, z2 = np.zeros(4), np.zeros(4), np.zeros(4)
	
	x2[0], y2[0], z2[0] = x_temp[0], y_temp[0], z_temp[0]

	j = 1
	while abs(x_temp[j] - x_temp[j+1]) <= 0.02:
		j += 1
	x2[1], y2[1], z2[1] = x_temp[j], y_temp[j], z_temp[j]

	while abs(y_temp[j] - y_temp[j+1]) <= 0.02:
		j += 1
	x2[2], y2[2], z2[2] = x_temp[j], y_temp[j], z_temp[j]
	
	x2[3], y2[3], z2[3] = x_temp[x_temp.size-5], y_temp[x_temp.size-5], z_temp[x_temp.size-5]
	print(x2)
	print(y2)
	print(z2)
	deltax, deltay, deltaz = x1-x2, y1-y2, z1-z2
	for i in range(deltax.size):
		dx.append(deltax[i])
		dy.append(deltay[i])
		dz.append(deltaz[i])

print(dx)

plt.hist(dx)
plt.show()

plt.hist(dy)
plt.show()

plt.hist(dz)
plt.show()
