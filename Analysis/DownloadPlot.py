import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
import seaborn as sns
import math
import numpy as np

lddisp = pd.read_excel('Alfa Data set adjusted.xlsx', usecols="A:C")
inboard = pd.read_excel('Alfa Data set adjusted.xlsx', sheet_name=1, usecols="A:J")
outboard = pd.read_excel('Alfa Data set adjusted.xlsx', sheet_name=2, usecols="A:J")


outboard -= outboard.mean(axis=1)[7]
inboard -= inboard.mean(axis=1)[7]



all = pd.concat([lddisp, inboard.add_prefix("in "), outboard.add_prefix("out ")], axis=1)
all.head()


fig, ax = plt.subplots(121)
for i in range(8):
    ax[0] = all.plot(x="LOADCELL [kN]", y=f'in SG {i+1}')
    ax[1] = all.plot(x="LOADCELL [kN]", y=f'out SG {i+1}')
plt.show()