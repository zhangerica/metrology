
# coding: utf-8

# In[ ]:


# Plots x, y, z residuals of module markers after stave is glued to spaceframe


# In[16]:


import glob
import pandas as pd
import csv
import os
import numpy as np
import matplotlib.pyplot as plt


# In[17]:


directory = 'C:\ALICE Upgrade\ITSUsoftwareCMM\Stave\Marker Positions'
cp = raw_input('Enter ID of Right Cold Plate: ')
#for f in os.listdir(directory):
    #if cp in f and f.endswith('.csv'):
        #path = os.path.abspath(directory + '\\' + f)
path = os.path.abspath("STAVE_MARKERPOS_2018_1_29_B-ML-Stave-0_B-HS-R-0_ALC-0312-00_026_B-HS-L-0_ALC-0312-00_120.csv")


# In[18]:


data = pd.read_csv(open(path), header = None, usecols = [2, 4, 5, 6])
label = pd.DataFrame.get(data, 2)


# In[19]:


slices = data.index[label == u'MarkerCenter '].tolist()
one, two, three, four = slices[0], slices[1], slices[2], slices[3]
five, six, seven, eight = slices[4], slices[5], slices[6], slices[7]


# In[20]:


mod1, mod2, mod3, mod4 = data[one+1:two-4], data[two+1:three-4], data[three+1:four-4], data[four+1:five-4]
mod5, mod6, mod7, mod8 = data[five+1:six-4], data[six+1:seven-4], data[seven+1:eight-4], data[eight+1:-4]
hs_low = [mod1, mod2, mod3, mod4]
hs_up = [mod5, mod6, mod7, mod8]
low = pd.concat([mod1, mod2, mod3, mod4])[[4, 5, 6]]
up = pd.concat([mod5, mod6, mod7, mod8])[[4, 5, 6]]


# In[21]:


# z residuals
low_dz_pos = (low[low[4] > 0][6] - 13.3) * 1000
low_dz_pos_y = low[low[4] > 0][5]
low_dz_neg = (low[low[4] < 0][6] - 13.3) * 1000
low_dz_neg_y = low[low[4] < 0][5]
up_dz = (up[6] - 9.7) * 1000
up_dz_y = up[5]


# In[22]:


# z plots
dz, axes = plt.subplots(nrows=1, ncols=2, figsize = (15, 5))
zlow, zup = axes.flatten()

zlow.plot(low_dz_pos_y, low_dz_pos, 'r+', label = 'x = 2 mm')
zlow.plot(low_dz_neg_y, low_dz_neg, 'b+', label = 'x = -28 mm')
zlow.set(xlabel="y [mm]")
zlow.set(ylabel = "$\Delta$ z [$\mu$m]")
zlow.set_title('Lower/Left')
zlow.set_ylim([-150, 250])
for i in [-422, -211, 0, 211, 422]:
    zlow.axvline(x = i, ymin = .1, ymax = .7, c = 'k', linewidth = .4)
zlow.legend(loc = 1)

zup.plot(up_dz_y, up_dz, 'g+', label = 'x = 28 mm')
zup.set(xlabel="y [mm]")
zup.set(ylabel = "$\Delta$ z [$\mu$m]")
zup.set_title('Upper/Right')
zup.set_ylim([-150, 250])
for i in [-422, -211, 0, 211, 422]:
    zup.axvline(x = i, ymin = .1, ymax = .7, c = 'k', linewidth = .4)
zup.legend(loc = 1)
    
plt.show()
#plt.savefig(directory + cp + '_z.png')


# In[23]:


# x residuals
low_dx_pos = (low[low[4] > 0][4] - 2.099) * 1000
low_dx_pos_y = low[low[4] > 0][5]
low_dx_neg = (low[low[4] < 0][4] + 27.899) * 1000
low_dx_neg_y = low[low[4] < 0][5]
up_dx = (up[4] - 27.899) * 1000
up_dx_y = (up[5])


# In[24]:


# x plots
plt.plot(low_dx_pos_y, low_dx_pos, 'r+', label = 'x = 2.099 mm')
plt.plot(low_dx_neg_y, low_dx_neg, 'b+', label = 'x = -27.899 mm')
plt.plot(up_dx_y, up_dx, 'g+', label = 'x = 27.899 mm')
plt.xlabel("y [mm]")
plt.ylabel("$\Delta$ x [$\mu$m]")
plt.ylim([-400, 250])
for i in [-422, -211, 0, 211, 422]:
    plt.axvline(x = i, ymin = .1, ymax = .7, c = 'k', linewidth = .4)
plt.legend(loc = 1)
plt.title("$\Delta$ x")   
#plt.show()
#plt.savefig(directory + cp + '_x.png')


# # y residuals
# m1 = [-421.925, -211.375] # markers [a, b] for module 1
# m2 = [-210.825, -0.275]
# m3 = [0.275, 210.825]
# m4 = [211.375, 421.925]
# 
# markers = np.concatenate([m1, m2, m3, m4])
# Markers = np.array([m1, m2, m3, m4])

# In[25]:


# y residuals
m1 = [-421.925, -211.375] # markers [a, b] for module 1 
m2 = [-210.825, -0.275] 
m3 = [0.275, 210.825] 
m4 = [211.375, 421.925]

markers = np.concatenate([m1, m2, m3, m4]) 
Markers = np.array([m1, m2, m3, m4])


# In[26]:


X, Y, Z = 4, 5, 6

def is_missing(element):
    return len(element) == 0

# replaces empty arrays resulting from points way out of tolerance with points outside the plot range
def replace(element):
    return pd.Series([10000])

def prepare(markers):
    for n, i in enumerate(markers):
        if is_missing(i):
            markers[n] = replace(i)
    return markers

# low_or_up is either hs_low or hs_up
def marker_pos(low_or_up, module, tolerance):
    number = module - 1
    mod_num = low_or_up[number]
    ad = mod_num[abs(mod_num[Y] - Markers[number][0]) < tolerance]
    bc = mod_num[abs(mod_num[Y] - Markers[number][1]) < tolerance]
    if np.array_equal(np.concatenate(low_or_up), np.concatenate(hs_low)):
        a = ad[ad[X] > 0][Y]
        d = ad[ad[X] < 0][Y]
        b = bc[bc[X] > 0][Y]
        c = bc[bc[X] < 0][Y]
        markers = [a, d, b, c]
    else:
        a = ad[Y]
        b = bc[Y]
        markers = [a, b]
    return prepare(markers)

low_ADBC = [marker_pos(hs_low, i, 0.4) for i in range(1, 5)]
up_AB = [marker_pos(hs_up, i, 0.8) for i in range(1, 5)]


# In[27]:


def np_array(low_markers):
    return np.array([n[i].item() for n in low_markers for i in [0, 1]])

a_i, b_i, c_i, d_i = 0, 2, 3, 1

low_ab = [[low_ADBC[i][a_i], low_ADBC[i][b_i]] for i in range(0, 4)]
low_dc = [(low_ADBC[i][d_i], low_ADBC[i][c_i]) for i in range(0, 4)]

low_ab = np_array(low_ab)
low_dc = np_array(low_dc)
up_ab = np_array(up_AB)


# In[28]:


plt.plot(markers, (low_ab - markers)*1000, 'r+', label = "x = 2.099 mm")
plt.plot(markers, (low_dc - markers)*1000, 'b+', label = "x = -27.899 mm")
plt.plot(markers, (up_ab - markers)*1000, 'g+', label = "x = 27.899 mm")
for i in [-422, -211, 0, 211, 422]:
    plt.axvline(x = i, ymin = 0, ymax = 1, c = 'k', linewidth = .4)
plt.title("$\Delta$ y")
plt.xlabel("y [mm]")
plt.ylabel("$\Delta$ y [$\mu$m]")
plt.legend(bbox_to_anchor=(1, 1))
plt.show()
#plt.savefig(directory + cp + '_y.png')

