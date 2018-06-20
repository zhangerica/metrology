import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
import csv

CPnum = raw_input('Enter Cold Plate ID: ')

def histo(n, data, xlabel, xlim, title):
	fig, axs = plt.subplots(1,n)
	axs = axs.ravel()
	for idx, ax in enumerate(axs):
		ax.hist(data[idx])
		ax.set_xlabel(xlabel[idx])
		ax.set_ylabel('counts')
		ax.set_xlim(xlim)
	plt.suptitle(title)
	plt.show()


dir1 = 'C:\ALICE Upgrade\ITSUsoftwareCMM\ModulePosition'
dir2 = 'C:\ALICE Upgrade\ITSUsoftwareCMM\ModulePlanarity'


BefGlueDry = raw_input('Check before glue dried? (yes/no)')
print(BefGlueDry)
while BefGlueDry != 'yes' and BefGlueDry != 'no':
	print('invalid input')
	BefGlueDry = raw_input('Check before glue dried? (yes/no)')

uarms = ''
if BefGlueDry == 'no':
	uarms = raw_input('Have the u-arms been glued?')
	while uarms != 'yes' and uamrs != 'no':
		print('invalid input')
		uarms = raw_input('Have the u-arms been glued?')



fnames1 = []
fnames2 = []
fnames3 = []

for f in os.listdir(dir1):
	if f.startswith(CPnum) and f.endswith('.dat'):
		fnames1.append(f)

if fnames1 == []:
	print('Invalid CP ID, try again.')
	quit()

fnames1 = np.array(fnames1)

for j in range(fnames1.size):
	for i in range(fnames1.size):
		if fnames1[i].find('MODULEPOS'+str(i+1))+1:
			continue
		else:
			fnames1[i], fnames1[fnames1.size-1] = fnames1[fnames1.size-1], fnames1[i]
    
if BefGlueDry == 'no':
	for f in os.listdir(dir2):
		if f.startswith(CPnum) and f.find('ALLMODULES')>0 and f.find('beforeUarms')>0 and f.endswith('.dat'):
			fnames2.append(f)

	fnames2 = fnames2[len(fnames2)-1]

if uarms == 'yes':
	for f in os.listdir(dir2):
		if f.startswith(CPnum) and f.find('ALLMODULES')>0 and f.find('afterUarms')>0 and f.endswith('.dat'):
			fnames3.append(f)

	fnames3 = fnames3[len(fnames3)-1]

x1, y1, z1 = [], [], []
x2, y2, z2 = [], [], []
dx, dy, dz = [], [], []
dx1, dy1, dz1 = [], [], []

x2_all, y2_all, z2_all = [], [], []
x3_all, y3_all, z3_all = [], [], []

for i in range(fnames1.size):
	d1 = pd.read_csv(open(dir1+'\\'+fnames1[i]), header = None, usecols=[4,5,6])

	x3, y3, z3 = pd.DataFrame.get(d1,4).as_matrix(), pd.DataFrame.get(d1,5).as_matrix(), pd.DataFrame.get(d1,6).as_matrix()

	for k in range(1,x3.size):
		x1.append(x3[k])
		y1.append(y3[k])
		z1.append(z3[k])

if BefGlueDry == 'no':
	with open(dir2+'\\'+fnames2) as fname:
		lines = csv.reader(fname, delimiter = ';')
		for line in lines:
			if line[0] == '' or line[0] == '100':
				continue
			else:
				x2_all.append(float(line[4]))
				y2_all.append(float(line[5]))
				z2_all.append(float(line[6]))
	for i in range(4):
		x2.append(x2_all[0 + 28*i])
		x2.append(x2_all[13 + 28*i])
		x2.append(x2_all[14 + 28*i])
		x2.append(x2_all[27 + 28*i])
		y2.append(y2_all[0 + 28*i])
		y2.append(y2_all[13 + 28*i])
		y2.append(y2_all[14 + 28*i])
		y2.append(y2_all[27 + 28*i])
		z2.append(z2_all[0 + 28*i])
		z2.append(z2_all[13 + 28*i])
		z2.append(z2_all[14 + 28*i])
		z2.append(z2_all[27 + 28*i])

	x1, x2, y1, y2, z1, z2 = np.array(x1), np.array(x2), np.array(y1), np.array(y2), np.array(z1), np.array(z2)
	dx, dy, dz = x2-x1, y2-y1, z2-z1


x3, y3, z3 = [], [], []

if uarms == 'yes':
	modnum=0
	count=0
	fac=1
	with open(dir2+'\\'+fnames3) as fname:
		lines = csv.reader(fname, delimiter = ';')
		for i, line in enumerate(lines):
			if line[0] == '' or line[0] == '100':
				if modnum==0:
					modnum +=1
					x3.append(x3_all[0])
					y3.append(y3_all[0])
					z3.append(z3_all[0])
					k=1
					while abs(x3_all[k] - x3_all[k+1]) <= 0.02:
						k += 1
					x3.append(x3_all[k])
					y3.append(y3_all[k])
					z3.append(z3_all[k])
					while abs(y3_all[k] - y3_all[k+1]) <= 0.02:
						k += 1
					x3.append(x3_all[k])
					y3.append(y3_all[k])
					z3.append(z3_all[k])
					x3.append(x3_all[len(x3_all)-1])
					y3.append(y3_all[len(y3_all)-1])
					z3.append(z3_all[len(z3_all)-1])
				else:
					modnum+=1
				if modnum%4 == 0:
					print(modnum%4)
					if count>0:
						x3.append(x3_all[count])
						y3.append(y3_all[count])
						z3.append(z3_all[count])
						count+=1
						while abs(x3_all[count] - x3_all[count+1]) <= 0.02:
							count += 1
						x3.append(x3_all[count])
						y3.append(y3_all[count])
						z3.append(z3_all[count])
						while abs(y3_all[count] - y3_all[count+1]) <= 0.02:
							count += 1
						x3.append(x3_all[count])
						y3.append(y3_all[count])
						z3.append(z3_all[count])
						x3.append(x3_all[len(x3_all)-1])
						y3.append(y3_all[len(y3_all)-1])
						z3.append(z3_all[len(z3_all)-1])
					count=i+1-4*fac
					fac+=1
			else:
				x3_all.append(float(line[4]))
				y3_all.append(float(line[5]))
				z3_all.append(float(line[6]))

	print(len(x3_all))
	print(x3_all)
	print(x3)

	x3, y3, z3 = np.array(x3), np.array(y3), np.array(z3)

	dx1, dy1, dz1 = x3-x2, y3-y2, z3-z2

nominal_y = [-421.925, -211.375, -211.375, -421.925, -210.825, -0.275, -0.275, -210.825, 0.275, 210.825, 210.825, 0.275, 211.375, 421.925, 421.925, 211.375]

y1_nom = np.array(y1) - np.array(nominal_y)

x1_nom, x2_nom= [], []

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



hNomdata = [x1_nom*(1000*np.ones(len(x1))), y1_nom*(1000*np.ones(len(y1)))]
hNomxlabel = ['$\Delta x (\mu m)$', '$\Delta y (\mu m)$']
hNomlim = [-50,50]
hNomtitle = 'Distance from nominal before gluing'
histo(2, hNomdata, hNomxlabel, hNomlim, hNomtitle)


y_pos_aft, z_pos_aft = [], []
y_neg_aft, z_neg_aft = [], []

if BefGlueDry == 'no':
	for i in range(len(x2)):
		if x2[i]>0:
			y_pos_aft.append(y2[i])
			z_pos_aft.append(z2[i])
		else:
			y_neg_aft.append(y2[i])
			z_neg_aft.append(z2[i])



	dataY = [y_pos_bef, y_pos_aft, y_neg_bef, y_neg_aft]
	dataZ = [z_pos_bef-0.4*np.ones(len(z_pos_bef)), z_pos_aft-0.4*np.ones(len(z_pos_aft)), z_neg_bef-0.4*np.ones(len(z_neg_bef)), z_neg_aft-0.4*np.ones(len(z_neg_aft))]
	YZtitle = ['Before Glue Dried', 'After Glue Dried']
	figYZ, axYZ = plt.subplots(1,2)
	axYZ = axYZ.ravel()
	for idx, ax in enumerate(axYZ):
		ax.plot(dataY[idx], dataZ[idx], 'b+', label = 'x>0')
		ax.plot(dataY[idx+2], dataZ[idx+2], 'r+', label = 'x<0')
		ax.set_xlabel('y (mm)')
		ax.set_ylabel('z (mm)')
		ax.set_ylim([-0.2, 0.2])
		ax.set_title(YZtitle[idx])
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
	plt.ylim([-.4,.4])
	plt.legend()
	plt.show()


	hBAdata = [dx*(1000*np.ones(len(dx))), dy*(1000*np.ones(len(dy))), dz*(1000*np.ones(len(dz)))]
	hBAlabel = ['$\Delta x (\mu m)$', '$\Delta y (\mu m)$', '$\Delta z (\mu m)$']
	histo(3, hBAdata, hBAlabel, [-500,500 ], 'Difference in position before/after gluing')

if uarms == 'yes':
	hBAdata = [dx1*(1000*np.ones(len(dx1))), dy1*(1000*np.ones(len(dy1))), dz1*(1000*np.ones(len(dz1)))]
	hBAlabel = ['$\Delta x (\mu m)$', '$\Delta y (\mu m)$', '$\Delta z (\mu m)$']
	histo(3, hBAdata, hBAlabel, [-300,300 ], 'Difference in position before/after u-arms gluing')


























































