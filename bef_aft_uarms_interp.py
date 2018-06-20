import numpy as np
import os
import csv
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from mpl_toolkits.mplot3d import Axes3D

def get_xyz(data1, data2=[]):
    x, y, z = [], [], []
    for j in range(4):
        k=0
        for i in range(len(data1[j])):
            if data2!=[] and l_or_r=='right' and ( i==15 or i==19 or i==21 ):
                x.append(data2[j][k][0])
                x.append(data2[j][k+1][0])
                y.append(data2[j][k][1])
                y.append(data2[j][k+1][1])
                z.append(data2[j][k][2])
                z.append(data2[j][k+1][2])
                k+=2
            elif data2!=[] and l_or_r=='left' and ( i==1 or i==3 or i==7 ):
                x.append(data2[j][k][0])
                x.append(data2[j][k+1][0])
                y.append(data2[j][k][1])
                y.append(data2[j][k+1][1])
                z.append(data2[j][k][2])
                z.append(data2[j][k+1][2])
                k+=2
            x.append(data1[j][i][0])
            y.append(data1[j][i][1])
            z.append(data1[j][i][2])

        # if data2 != []:
        #     for i in range(len(data2[j])):
        #         x.append(data2[j][i][0])
        #         y.append(data2[j][i][1])
        #         z.append(data2[j][i][2])
    return x, y, z

def plot_halfstave(befU1, befU2, aftU1, aftU2):
# plots plane of module before and after u-arms including the fit data points (after)
    x1, y1, z1 = get_xyz(befU1, befU2)
    x2, y2, z2 = get_xyz(aftU1)
    x3, y3, z3 = get_xyz(aftU2)

    x1 = abs(np.array(x1))
    x2 = abs(np.array(x2))
    x3 = abs(np.array(x3))

    plt3d = plt.figure()#.gca(projection='3d')
    # ax = plt.gca()
    plt.scatter(y1, x1, marker='+')#, z1, label='before u-arms')
    plt.title('CP: '+CPnum+', HS '+l_or_r+', before u-arms')
    plt.ylabel('x (mm)')
    plt.xlabel('y (mm)')
    # ax.set_xlabel('x (mm)')
    # ax.set_ylabel('y (mm)')
    # ax.set_zlabel('z (mm)')
    # ax.set_xlim(-15.5, 15.5)
    # ax.set_ylim(-422, 422)
    # ax.set_zlim(.3, .7)
    plt.show()

    # plt3d = plt.figure().gca(projection='3d')
    # ax = plt.gca()
    plt.figure()
    plt.title('CP: '+CPnum+', HS '+l_or_r+', after u-arms')
    plt.scatter(y2, x2, label = 'measured', marker='+')#, z2, label = 'after u-arms, measured')
    plt.scatter(y3, x3, label = 'fit', marker='+')#, z3, label = 'after u-arms, fit')
    plt.ylabel('x (mm)')
    plt.xlabel('y (mm)')
    # plt.title('CP: '+CPnum+', After U-Arms')
    # ax.set_xlabel('x (mm)')
    # ax.set_ylabel('y (mm)')
    # ax.set_zlabel('z (mm)')
    plt.legend()
    plt.show()

CPnum = raw_input('Enter Cold Plate ID: ')
l_or_r = raw_input('Are the cross cables on the right or the left? (enter \'right\' or \'left\'): ')

while l_or_r != 'right' and l_or_r != 'left':
    print'invalid input'
    l_or_r = raw_input('Are the cross cables on the right or the left? (enter \'right\' or \'left\'): ')

dir1 = 'C:\ALICE Upgrade\ITSUsoftwareCMM\ModulePlanarity'

fnames1 = []
fnames2 = []

for f in os.listdir(dir1):
    if f.startswith(CPnum) and f.find('ALLMODULES')>0 and f.find('beforeUarms')>0 and f.endswith('.dat'):
        fnames1.append(f)
    if f.startswith(CPnum) and f.find('ALLMODULES')>0 and f.find('afterUarms')>0 and f.endswith('.dat') and f.find('_interp')<0:
        fnames2.append(f)

if fnames1 == [] and fnames2 == []:
    print('Invalid CP ID, try again.')
    quit()

fnames1 = fnames1[len(fnames1)-1]
fnames2 = fnames2[len(fnames2)-1]

befU_fit = [[], [], [], []]
befU_use = [[], [], [], []]
befU_all = [[],[],[],[]]
i, j = 0, 0

f = open(dir1+'\\'+fnames1,'r')
lines = f.readlines()
f.close()
f = open(dir1+'\\'+fnames1,'w')
for line in lines:
    if line.find('Marker Center') < 0:
        f.write(line)
f.close()

f = open(dir1+'\\'+fnames2,'r')
lines = f.readlines()
f.close()
f = open(dir1+'\\'+fnames2,'w')
for line in lines:
    if line.find('Marker Center') < 0:
        f.write(line)
f.close()

with open(dir1+'\\'+fnames1) as fname:
    lines = csv.reader(fname, delimiter = ';')
    for k, line in enumerate(lines):
        if line[0] == '' or line[0] == '100':
            j += 1
            if j%4==0:
                i += 1
            continue
        elif l_or_r=='right' and k!=15+32*i and k!=16+32*i and k!=21+32*i and k!=22+32*i and k!=25+32*i and k!=26+32*i:
            befU_fit[i].append((float(line[4]), float(line[5]), float(line[6])))
        elif l_or_r=='left' and k!=1+32*i and k!=2+32*i and k!=5+32*i and k!=6+32*i and k!=11+32*i and k!=12+32*i:
            befU_fit[i].append((float(line[4]), float(line[5]), float(line[6])))
        else:
            befU_use[i].append((float(line[4]), float(line[5]), float(line[6])))
        befU_all[i].append((float(line[4]), float(line[5]), float(line[6])))

befU_fit = np.array(befU_fit)
befU_use = np.array(befU_use)

aftU = [[], [], [], []]
i, j = 0, 0
junklines = []
with open(dir1+'\\'+fnames2) as fname:
    lines = csv.reader(fname, delimiter = ';')
    for line in lines:
        if line[0] == '' or line[0] == '100':
            j += 1
            if j%4==0:
                i += 1
            junklines.append(line[0]+';'+line[1]+';'+line[2]+';'+line[3]+';'+line[4]+';'+line[5]+';'+line[6]+';'+line[7]+';'+line[8]+'\n')
            continue
        else:
            aftU[i].append((float(line[4]), float(line[5]), float(line[6])))

for i in range(4):
    if len(aftU[i]) < 22:
        print 'Metrology done incorrectly, too few points for module',i+1,'please redo metrology for this HS'
        quit()
    elif len(aftU[i]) > 22:
        for j in range(1, len(aftU[i])-2):
            if abs(aftU[i][j-1][1] - aftU[i][j][1])>29 and abs(aftU[i][j+1][1] - aftU[i][j][1])>29:
                del aftU[i][j]

aftU = np.array(aftU)

for i in range(4):
    befU_fit[i] = np.array(befU_fit[i])
    befU_use[i] = np.array(befU_use[i])
    aftU[i] = np.array(aftU[i])

aftU_fit = [[], [], [], []]

for i in range(4):
    linreg = LinearRegression()
    linreg.fit(befU_fit[i], aftU[i])
    aftU_fit[i] = linreg.predict(befU_use[i])

plot_halfstave(befU_fit, befU_use, aftU, aftU_fit)

x, y, z = get_xyz(aftU, aftU_fit)

col2r = np.array([15,50,50,50,50,50,50,50,50,50,50,50,50,70,85,120,120,120,120,120,120,120,120,120,120,120,120,139])
col2l = np.array([15,52,52,52,52,52,52,52,52,52,52,52,52,72,87,122,122,122,122,122,122,122,122,122,122,122,122,141])

f = open(dir1+'\\'+fnames2[0:len(fnames2)-4]+'_interp.dat', 'w+')

for i in range(4):
    for j in range(28):
        if l_or_r == 'right':
            l = str(j+1)+';'+str(col2r[j])+';point ;1;'+str('{0:.4f}'.format(x[j+28*i]))+';'+str('{0:.4f}'.format(y[j+28*i]))+';'+str('{0:.4f}'.format(z[j+28*i]))+';;0.0000\n'
        else:
            l = str(j+1)+';'+str(col2l[j])+';point ;1;'+str('{0:.4f}'.format(x[j+28*i]))+';'+str('{0:.4f}'.format(y[j+28*i]))+';'+str('{0:.4f}'.format(z[j+28*i]))+';;0.0000\n'
        f.write(l)
        if j==27:
            for k in range(4):
                f.write(junklines[k+4*i])



# sx, sy, sz = 0.,0.,0.
# count = 0.
# for i in range(len(befU_use[0])):
#     sx += befU_use[0][i][0]
#     sy += befU_use[0][i][1]
#     sz += befU_use[0][i][2]
#     count+=1
# for i in range(len(befU_fit[0])):
#     sx += befU_fit[0][i][0]
#     sy += befU_fit[0][i][1]
#     sz += befU_fit[0][i][2]
#     count+=1

# print(sx/count, sy/count, sz/count)
# print(np.mean(x[:28]), np.mean(y[:28]), np.mean(z[:28]))
# print(np.max(z[:28]) - np.min(z[:28]))