import numpy as np
import sys
#import scipy as sp #not yet used
import structure_analysis as sa

#Applied load on structure

bucklingForce = 3e3
positionForce = 1.12

#Whiffle tree setup 

root = sa.Node([0.75, 1.95, positionForce, bucklingForce])

root.Insert([0.45, 1.05, 0.75, 0])
root.Insert([1.75, 2.35, 1.95, 0])
root.Insert([0.45, 0.45, 0.45, 0])
root.Insert([1.05, 1.05, 1.05, 0])
root.Insert([1.75, 1.75, 1.75, 0])
root.Insert([2.35, 2.35, 2.35, 0])


attachmentPositions = np.insert(root.PrintEndLoads(), [0], [[-bucklingForce], [positionForce]], axis=1)


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

wingBox = sa.Wingbox(wingAssembly, attachmentPositions)

#Output: you can modify freely

#print(secondMomentAreaAssembly(stringerGeneral, 'x'))
#print(secondMomentAreaAssembly(sheet, 'x'))
# print(f'The second moment of area of the cross-section is {sa.secondMomentAreaAssembly(wingAssembly, "x")} m^4')

# print(f'Normal stress: {sa.normalBendingStress(0.001, wingAssembly, "x")/1e6} MPa') #Parameters (0.001 = distance from clamping side)

# print(f'Shear stress: {sa.shearStress(0.001, wingAssembly, 0.075, "x")/1e6} MPa') #Parameters (0.001 = distance from clamping side, 0.075 = height from the bottom)

print(f'The second moment of area of the cross-section is {wingBox.secondMomentAreaAssembly(wingBox.structuralElements,"x")} m^4')
