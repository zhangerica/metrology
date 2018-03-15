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
			fnames1[i], fnames1[fnames1.size-1] = fnames1[fnames1.size-1], fnames1[i]
    
for f in os.listdir(dir2):
	if f.startswith(CPnum) and f.endswith('.csv'):
		fnames2.append(f)

fnames2 = np.array(fnames2)

fnames2.sort()

x1, y1, z1 = [], [], []
x2, y2, z2 = [], [], []
dx, dy, dz = [], [], []

x2_all, y2_all, z2_all = [], [], []

for i in range(fnames1.size):
	d1 = pd.read_csv(open(dir1+'\\'+fnames1[i]), header = None, usecols=[4,5,6])
	d2 = pd.read_csv(open(dir2+'\\'+fnames2[i]), header = None, usecols=[4,5,6])

	x3, y3, z3 = pd.DataFrame.get(d1,4).as_matrix(), pd.DataFrame.get(d1,5).as_matrix(), pd.DataFrame.get(d1,6).as_matrix()
	x_temp, y_temp, z_temp = pd.DataFrame.get(d2,4).as_matrix(), pd.DataFrame.get(d2,5).as_matrix(), pd.DataFrame.get(d2,6).as_matrix()
	x4, y4, z4 = np.zeros(4), np.zeros(4), np.zeros(4)
	
	x4[0], y4[0], z4[0] = x_temp[0], y_temp[0], z_temp[0]

	j = 1
	while abs(x_temp[j] - x_temp[j+1]) <= 0.02:
		j += 1
	x4[1], y4[1], z4[1] = x_temp[j], y_temp[j], z_temp[j]

	while abs(y_temp[j] - y_temp[j+1]) <= 0.02:
		j += 1
	x4[2], y4[2], z4[2] = x_temp[j], y_temp[j], z_temp[j]
	
	x4[3], y4[3], z4[3] = x_temp[x_temp.size-5], y_temp[x_temp.size-5], z_temp[x_temp.size-5]

	deltax, deltay, deltaz = x3-x4, y3-y4, z3-z4
	for k in range(deltax.size):
		dx.append(deltax[k])
		dy.append(deltay[k])
		dz.append(deltaz[k])
		
		x1.append(x3[k])
		y1.append(y3[k])
		z1.append(z3[k])

		x2.append(x4[k])
		y2.append(y4[k])
		z2.append(z4[k])

	for k in range(x_temp.size-4):
		x2_all.append(x_temp[k])
		y2_all.append(y_temp[k])
		z2_all.append(z_temp[k])


x1_nom, x2_nom = [], []

y_pos_bef, z_pos_bef = [], []
y_neg_bef, z_neg_bef = [], []

for i in range(len(x1)):
	if x1[i]>0:
		x1_nom.append(x1[i] - 14.999)
		y_pos_bef.append(y1[i])
		z_pos_bef.append(z1[i])
	else:
		x1_nom.append(x1[i] + 14.999)
		y_neg_bef.append(y1[i])
		z_neg_bef.append(z1[i])

plt.hist(x1_nom*(1000*np.ones(len(x1))))
plt.title('Distance from nominal before gluing')
plt.xlabel('$\Delta x (\mu m)$')
plt.ylabel('counts')
plt.xlim([-50,50])
plt.show()



y_pos_aft, z_pos_aft = [], []
y_neg_aft, z_neg_aft = [], []

for i in range(len(x2)):
	if x2[i]>0:
		y_pos_aft.append(y2[i])
		z_pos_aft.append(z2[i])
	else:
		y_neg_aft.append(y2[i])
		z_neg_aft.append(z2[i])

plt.figure(figsize=(10,7))
plt.plot(y_pos_bef, z_pos_bef-0.4*np.ones(len(z_pos_bef)), 'b+',label = 'x>0')
plt.plot(y_neg_bef, z_neg_bef-0.4*np.ones(len(z_neg_bef)), 'r+', label = 'x<0')
plt.title('Before Glue Dried')
plt.xlabel('y (mm)')
plt.ylabel('z (mm)')
plt.ylim([-0.2, 0.2])
plt.legend()
plt.show()

plt.figure(figsize=(10,7))
plt.plot(y_pos_aft, z_pos_aft-0.4*np.ones(len(z_pos_aft)), 'b+', label = 'x>0')
plt.plot(y_neg_aft, z_neg_aft-0.4*np.ones(len(z_neg_aft)), 'r+', label = 'x<0')
plt.title('After Glue Dried')
plt.xlabel('y (mm)')
plt.ylabel('z (mm)')
plt.ylim([-0.2, 0.2])
plt.legend()
plt.show()



x2_all_nom = []
x2_all_pos, x2_all_neg = [], []
y2_all_pos, y2_all_neg = [], []

for i in range(len(x2_all)):
	if x2_all[i] > 0:
		x2_all_nom.append(x2_all[i] - 14.999)
		x2_all_pos.append(x2_all[i] - 14.999)
		y2_all_pos.append(y2_all[i])
	else:
		x2_all_nom.append(x2_all[i] + 14.999)
		x2_all_neg.append(x2_all[i] + 14.999)
		y2_all_neg.append(y2_all[i])

plt.hist(x2_all_nom*(1000*np.ones(len(x2_all))))
plt.title('Distance from nominal after gluing')
plt.xlabel('$\Delta x (\mu m)$')
plt.ylabel('counts')
plt.xlim([-50,50])
plt.show()

plt.figure(figsize=(10,7))
plt.plot(y2_all_pos, x2_all_pos, 'b+', label = 'x>0')
plt.plot(y2_all_neg, x2_all_neg, 'r+', label = 'x<0')
plt.title('Distance from nominal')
plt.xlabel('y (mm)')
plt.ylabel('$\Delta x (mm)$')
plt.ylim([-.05,.05])
plt.legend()
plt.show()


hBAdata = [dx, dy, dz]
hBAlabel = ['$\Delta x (\mu m)$', '$\Delta y (\mu m)$', '$\Delta z (\mu m)$']
figBA, axBA = plt.subplots(1,3)
axBA = axBA.ravel()
for idx, ax in enumerate(axBA):
	ax.hist(hBAdata[idx]*(1000*np.ones(len(hBAdata[idx]))))
	ax.set_xlabel(hBAlabel[idx])
	ax.set_ylabel('counts')
	if idx<2:
		ax.set_xlim([-50,50])
plt.suptitle('Difference in position before/after gluing')
plt.show()
















