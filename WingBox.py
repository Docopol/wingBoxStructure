import numpy as np
import sys
#import scipy as sp #not yet used
import structure_analysis as sa

#Second moment of area calculation

#Format for elements xCg, yCg, xLength, yLength

#Bottom part stringer and then vertical part stringer
stringerGeneral = np.array([[0.01075, 0.00075, 0.0185, 0.0015], [0.00075, 0.01, 0.0015, 0.02]], dtype=np.float32)
stringerBot = np.array([[0.01075, 0.00075+0.0008, 0.0185, 0.0015], [0.00075, 0.01+0.0008, 0.0015, 0.02]], dtype=np.float32)
stringerTop = np.array([[0.01075, 0.15-0.00075-0.0008, 0.0185, 0.0015], [0.00075, 0.15-0.01-0.0008, 0.0015, 0.02]], dtype=np.float32)

#Sheet order bottom C, left A, top C, right A
sheet = np.array([[0.2, 0.0004, 0.4, 0.0008], [0.0004, 0.075, 0.0008, 0.1484], [0.2, 0.1496, 0.4, 0.0008], [0.3996, 0.075, 0.0008, 0.1484]], dtype=np.float32)

#You can modify the number of stringers

nbStringersTop = 2
nbStringersBot = 5

#Do not modify these

stringerAssemblyTop = np.repeat(stringerTop, [nbStringersTop, nbStringersTop], axis=0)
stringerAssemblyBot = np.repeat(stringerBot, [nbStringersBot, nbStringersBot], axis=0)
wingAssembly = np.concatenate((sheet, stringerAssemblyBot, stringerAssemblyTop), axis=0)


#Output: you can modify freely

#print(secondMomentAreaAssembly(stringerGeneral, 'x'))
#print(secondMomentAreaAssembly(sheet, 'x'))
print(f'The second moment of area of the cross-section is {sa.secondMomentAreaAssembly(wingAssembly, "x")} m^4')

print(f'Normal stress: {sa.normalBendingStress(0.001, wingAssembly, "x")/1e6} MPa') #Parameters (0.001 = distance from clamping side)

print(f'Shear stress: {sa.shearStress(0.001, wingAssembly, 0.075, "x")/1e6} MPa') #Parameters (0.001 = distance from clamping side, 0.075 = height from the bottom)