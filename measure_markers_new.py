
# coding: utf-8

# In[19]:


import glob
import pandas
import os
import xlrd
import numpy as np
import matplotlib.pyplot as plt


# In[20]:


path = os.path.abspath("STAVE*")
path1 = glob.glob(path)[0]
data = pandas.read_excel(open(path1), header = None, usecols = [i for i in range(2, 9)])
arr = data.values
arr = np.array(arr)
array = np.transpose(arr)


# In[21]:


modules = [] 
ys = [] #y-coordinates
xs = []

i = 0
label = arr[i][0]
for j in range(0, 8):
    if i == len(arr):
        print "Done"
    if str(arr[i][0]) == "MarkerCenter ":
        module = []
        y = []
        x = []
        i += 1
    if str(arr[i][0]) == "point ":
        while str(arr[i][0]) == "point ":
            module.append(arr[i][4])
            y.append(arr[i][3])
            x.append(arr[i][2])
            label = arr[i][0]
            i += 1
        modules.append(module)
        ys.append(y)
        xs.append(x)
        i += 4
    j += 1          
modules_cat = np.concatenate(modules) #z-coordinates


# In[22]:


lower = modules[0:4]
lower_nominal = [np.full((1, len(lower[i])), 13.3)[0] for i in range(0, 4)]
lower = [np.asarray(lower[i]) for i in range(0, len(lower))]
lower_residuals = [lower[i] - lower_nominal[i] for i in range(0, len(lower))]
lower_residuals = np.concatenate(lower_residuals)
lower_ys = [np.asarray(ys[i]) for i in range(0, 4)]
lower_ys_cat = np.concatenate(lower_ys)
lower_xs = [np.asarray(xs[i]) for i in range(0, 4)]
lower_xs_cat = np.concatenate(lower_xs)

upper = modules[4:8]
upper_nominal = [np.full((1, len(upper[i])), 9.7)[0] for i in range(0, 4)]
upper = [np.asarray(upper[i]) for i in range(0, len(upper))]
upper_residuals = [upper[i] - upper_nominal[i] for i in range(0, len(upper))]
upper_residuals = np.concatenate(upper_residuals)
upper_ys = [np.asarray(ys[i]) for i in range(4, 8)]
upper_ys_cat = np.concatenate(upper_ys)
upper_xs = [np.asarray(xs[i]) for i in range(4, 8)]
upper_xs_cat = np.concatenate(upper_xs)

low = np.vstack((lower_xs_cat, lower_ys_cat, lower_residuals))

#ys
low_neg_res = np.array([low[2][i] for i in range(0, len(low[1])) if low[0][i] < 0]) #x = -28 mm
low_neg_y = [low[1][i] for i in range(0, len(low[1])) if low[0][i] < 0] 
low_2_res = np.array([low[2][i] for i in range(0, len(low[1])) if low[0][i] > 0]) #x = 2 mm
low_2_y = [low[1][i] for i in range(0, len(low[1])) if low[0][i] > 0]

#x residuals
low_neg_res_x = np.array([low[0][i] for i in range(0, len(low[1])) if low[0][i] < 0]) #x = -28 mm
low_2_res_x = np.array([low[0][i] for i in range(0, len(low[1])) if low[0][i] > 0]) #x = 2 mm


# In[23]:


plt.plot(low_2_y, low_2_res*1000, "r+", label = "x = 2 mm")
plt.plot(low_neg_y, low_neg_res*1000, "b+", label = "x = -28 mm")
plt.xlabel("y [mm]")
plt.ylabel("$\Delta$ z [$\mu$m]")
plt.title("Lower/Left")
plt.axvline(x=211, c = 'k')
plt.axvline(x=422, c = 'k')
plt.axvline(x=-211, c = 'k')
plt.axvline(x=-422, c = 'k')
plt.axvline(x=0, c = 'k')
plt.legend(loc = 1)
plt.ylim((-150, 250))
plt.show()


# In[24]:


plt.plot(upper_ys_cat, upper_residuals*1000, "g+", label = "x = 28 mm")
plt.xlabel("y [mm]")
plt.ylabel("$\Delta$ z [$\mu$m]")
plt.title("Upper/Right")
plt.axvline(x=211, c = 'k')
plt.axvline(x=422, c = 'k')
plt.axvline(x=-211, c = 'k')
plt.axvline(x=-422, c = 'k')
plt.axvline(x=0, c = 'k')
plt.legend(loc = 1)
plt.ylim((-150, 250))
plt.show()


# In[ ]:


"""
-421.925 mod1
-210.825 mod2
0.275 mod3
211.375 mod4

29.5 step long sensor
0.5 step short to next sensor
"""


# In[17]:


"""
plt.plot(low_2_y, low_2_res_x*1000, "r+", label = "x = 2 mm")
plt.plot(low_neg_y, low_neg_res_x*1000, "b+", label = "x = -28 mm")
plt.xlabel("y [mm]")
plt.ylabel("$\Delta$ z [$\mu$m]")
plt.title("Lower/Left")
plt.axvline(x=211, c = 'k')
plt.axvline(x=422, c = 'k')
plt.axvline(x=-211, c = 'k')
plt.axvline(x=-422, c = 'k')
plt.axvline(x=0, c = 'k')
plt.legend(loc = 1)
plt.show()
"""


# In[18]:


#len(low_neg_res_x)

