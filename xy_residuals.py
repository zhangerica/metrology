import numpy as np
import matplotlib.pyplot as plt
import pandas
# 4 markers per module
# 4 modules per dummy half stave

xNominalAbs = 14.99

def GetData(number):
    file = "YellowDummy" + str(number) + ".xls"
    dummy = pandas.read_excel(open(file), header = None)
    matrix = dummy.as_matrix()
    data = [matrix[i] for i in range(1, 48) if i%3 != 0]
    return data

def xAbs(number):
    data = GetData(number)
    x = [data[i] for i in range(0, 32) if i%2 == 0]
    abs_x = [abs(x[i][-2]) for i in range(0, len(x))]
    return abs_x

def yAbs(number):
    data = GetData(number)
    y = [data[i] for i in range(0, 32) if i%2 != 0]
    abs_y = [abs(y[i][-2]) for i in range(0, len(y))]
    return abs_y

def xPlot(number):
    abs_x = xAbs(number)
    xErr = [abs_x[i] - xNominalAbs for i in range(0, len(abs_x))]
    xErr_mu = [xErr[i] * 1000 for i in range(0, len(xErr))] # delta x in microns
    plt.hist(xErr_mu, bins = np.linspace(-200, 200, 9))
    plt.title("Dummy " + str(number) + " $\Delta x$" )
    plt.xlabel("$\Delta x\ [\mu m]$" )
    plt.ylabel("Number of Markers")
    plt.show()
    return

def yErr(number):
    abs_y = yAbs(number)
    mod1, mod2, mod3, mod4 = abs_y[0:4], abs_y[4:8], abs_y[8:12], abs_y[12:16]
    mod1nom = [421.925, 211.375, 211.375, 421.925]
    mod2nom = [210.825, 0.275, 0.275, 210.825]
    mod3nom = [0.275, 210.825, 210.825, 0.275]
    mod4nom = [211.375, 421.925, 421.925, 211.375]
    modnom = mod1nom + mod2nom + mod3nom + mod4nom
    return [abs_y[i] - modnom[i] for i in range(0, len(abs_y))]

def yPlot(number):
    err_y = yErr(number)
    err_y_mu = [err_y[i] * 1000 for i in range(0, len(err_y))] # delta y in microns
    plt.hist(err_y_mu, bins = np.linspace(-400, 400, num = 17))
    plt.xlabel("$ \Delta y\ [\mu m]$")
    plt.ylabel("Number of Markers")
    plt.title("Dummy " + str(number) + " $\Delta y$")
    plt.show()
    return
"""
err_y_1 = yErr(1)
err_y_2 = yErr(2)
err_y = err_y_1 + err_y_2
err_y_mu =  [err_y[i] * 1000 for i in range(0, len(err_y))] # delta y in microns
plt.hist(err_y_mu, bins = np.linspace(-400, 400, num = 17))
plt.xlabel("$ \Delta y\ [\mu m]$" )
plt.ylabel("Number of Markers")
plt.title("Dummies 1 and 2 $\Delta y$ ")
plt.show()
"""
xPlot(1)
xPlot(2)
yPlot(1)
yPlot(2)
"""
abs_x_1 = xAbs(1)
abs_x_2 = xAbs(2)
abs_x = abs_x_1 + abs_x_2
err_x = [abs_x[i] - xNominalAbs for i in range(0, len(abs_x))]
err_x_mu =  [err_x[i] * 1000 for i in range(0, len(err_x))] # delta x in microns
plt.hist(err_x_mu, bins = np.linspace(-400, 400, num = 17))
plt.xlabel("$ \Delta x\ [\mu m]$" )
plt.ylabel("Number of Markers")
plt.title("Dummies 1 and 2 $\Delta x$ ")
plt.show()
"""
