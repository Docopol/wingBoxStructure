import numpy as np

maxForce = 3.3e3
bucklingForce = 3e3

#Whiffle tree

attachmentPositions = np.array([[-3e3, 1.0375e3, 1.0375e3, 0.6166e3, 0.30833e3], [0, 0.45, 1.05, 1.75, 2.35]], dtype=np.float32)

#Shear force diagram in beam

def shearDiagram(position):
    shearAtPosition = -sum(attachmentPositions[0][position >= attachmentPositions[1][:]])
    return shearAtPosition
    
#Bending force diagram in beam

def bendingDiagram(position):
    bendingAtPosition = 3e3 * 1.12 - sum(attachmentPositions[0][position >= attachmentPositions[1][:]] * attachmentPositions[1][position >= attachmentPositions[1][:]])
    return bendingAtPosition

def cgCalculator(structuralElements):
    structuralElements = np.concatenate((structuralElements, np.array([structuralElements[:, 2]*structuralElements[:, 3]]).T), axis=1)
    xCg = (sum(structuralElements[:, 0]*structuralElements[:, 4])/sum(structuralElements[:, 4]))
    yCg = (sum(structuralElements[:, 1]*structuralElements[:, 4])/sum(structuralElements[:, 4]))
    return xCg, yCg

def secondMomentArea(xLength, yLength, xParallelAxis, yParallelAxis, axis):
    if(axis == 'x'):
        return ((yLength**3*xLength)/12 + xLength*yLength*yParallelAxis**2)
    else:
        return ((yLength*xLength**3)/12 + xLength*yLength*xParallelAxis**2) 

def secondMomentAreaAssembly(structuralElements, axisSMA): #structuralElements[xCg, yCg, xLength, yLength, ]
    cg = cgCalculator(structuralElements)

    return sum(secondMomentArea(structuralElements[:, 2], structuralElements[:, 3], abs(cg[0]-structuralElements[:, 0]), abs(cg[1]-structuralElements[:, 1]), axisSMA))

def cutElements(structuralElements, axis, height):
    if(axis == 'x'):
        lowerCorner = structuralElements[:, 0] -  structuralElements[:, 2]/2
        heightMask = (lowerCorner) < height
        truncatedStructuralElements = structuralElements[heightMask].copy()
        truncatedStructuralElements[:, 2] = np.minimum(truncatedStructuralElements[:, 2], (height - lowerCorner[heightMask]))
        truncatedStructuralElements[:, 0] = (lowerCorner[heightMask] + truncatedStructuralElements[:, 2]/2)
        return truncatedStructuralElements
    else:
        lowerCorner = structuralElements[:, 1] -  structuralElements[:, 3]/2
        heightMask = (lowerCorner) < height
        truncatedStructuralElements = structuralElements[heightMask].copy()
        truncatedStructuralElements[:, 3] = np.minimum(truncatedStructuralElements[:, 3], (height - lowerCorner[heightMask]))
        truncatedStructuralElements[:, 1] = (lowerCorner[heightMask] + truncatedStructuralElements[:, 3]/2)
        return truncatedStructuralElements
    
def firstMomentAreaAssembly(structuralElements, axis, height):
    cgReference = cgCalculator(structuralElements)
    if(axis == 'x'):
        structuralElementsCut = cutElements(structuralElements, 'y', height)
        structuralElementsCut = np.concatenate((structuralElementsCut, np.array([structuralElementsCut[:, 2]*structuralElementsCut[:, 3]]).T), axis=1)
        cgPart = cgCalculator(structuralElementsCut)[1]
        return abs(cgReference[1]-cgPart)*sum(structuralElementsCut[:, 2]*structuralElementsCut[:, 3])
    else: 
        structuralElementsCut = cutElements(structuralElements, 'x', height)
        structuralElementsCut = np.concatenate((structuralElementsCut, np.array([structuralElementsCut[:, 2]*structuralElementsCut[:, 3]]).T), axis=1)
        cgPart = cgCalculator(structuralElementsCut)[0]
        return abs(cgReference[0]-cgPart)*sum(structuralElementsCut[:, 2]*structuralElementsCut[:, 3])

def normalBendingStress(positionFromRoot, structuralElements, axis):
    if(axis == 'x'):
        SMA = secondMomentAreaAssembly(structuralElements, axis)
        neutralAxisPosition = cgCalculator(structuralElements)[1]
        if(neutralAxisPosition > 0.15 - neutralAxisPosition):
            return bendingDiagram(positionFromRoot)*neutralAxisPosition/SMA
        else:
            return bendingDiagram(positionFromRoot)*(0.15-neutralAxisPosition)/SMA
    else:  #this part is not yet finished
        SMA = secondMomentAreaAssembly(structuralElements, axis)
        neutralAxisPosition = cgCalculator(structuralElements)[0]
        print(neutralAxisPosition)
        if(neutralAxisPosition > 0.15 - neutralAxisPosition):
            return bendingDiagram(positionFromRoot)*neutralAxisPosition/SMA
        else:
            return bendingDiagram(positionFromRoot)*(0.15-neutralAxisPosition)/SMA
        
def shearStress(positionFromRoot, structuralElements, height, axis):
    SMA = secondMomentAreaAssembly(structuralElements, axis)
    FMA = firstMomentAreaAssembly(structuralElements, axis, height)
    maxShear = shearDiagram(positionFromRoot)*FMA/(SMA*0.0015)
    
    return maxShear