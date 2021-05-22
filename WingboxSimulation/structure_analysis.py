import numpy as np

bucklingForce = 3e3
positionForce = 1.12

#Whiffle tree, format (starts position, end position, position of the applied force, magnitude of the applied force)

class Node:
    
    numberAttachPoints = 4 #Must be a power of two
    
    def __init__(self, dataInit): #Initilizes tree with root node
        
        self.left = None 
        self.right = None
        self.data = dataInit
        forceTopTree = dataInit[3]
    
    def Insert(self, dataExtraNode): #Adds nodes liked to the tree
        
        if self.data:
            if dataExtraNode[2] < self.data[2]:
                if self.left is None:
                    newForce = round((self.data[3]*abs(self.data[2]-self.data[1]))/abs(self.data[1]-self.data[0]), 2)
                    dataExtraNode[3] = newForce
                    self.left = Node(dataExtraNode)
                else:
                    self.left.Insert(dataExtraNode)
            elif dataExtraNode[2] > self.data[2]:
                if self.right is None:
                    newForce = round((self.data[3]*abs(self.data[2]-self.data[0]))/abs(self.data[1]-self.data[0]), 2)
                    dataExtraNode[3] = newForce
                    self.right = Node(dataExtraNode)
                else:
                    self.right.Insert(dataExtraNode)
        else:
            self.data = data
    
    def __CalculateEndLoads(self, node, endLoad): #Shout out to jcbd0101 for his contribution to make this work
        if((node.left is None) and (node.right is None)):
            endLoad[:, int(endLoad[0, 0]+1)] = np.array([node.data[3], node.data[2]])
            endLoad[0, 0] += 1
        else:
            self.__CalculateEndLoads(node.left, endLoad)
            self.__CalculateEndLoads(node.right, endLoad)
    
    def PrintEndLoads(self): #Prints the attachment points and the respective applied loads
        start = self
        endLoad = np.zeros(shape = (2, self.numberAttachPoints+1))
        self.__CalculateEndLoads(start, endLoad)
        return np.delete(endLoad, 0, axis=1)
    
    def PrintTree(self): #Prints tree from left to right
        if self.left:
            self.left.PrintTree()
        print( self.data),
        if self.right:
            self.right.PrintTree()

root = Node([0.75, 1.95, positionForce, bucklingForce])

root.Insert([0.45, 1.05, 0.75, 0])
root.Insert([1.75, 2.35, 1.95, 0])
root.Insert([0.45, 0.45, 0.45, 0])
root.Insert([1.05, 1.05, 1.05, 0])
root.Insert([1.75, 1.75, 1.75, 0])
root.Insert([2.35, 2.35, 2.35, 0])


attachmentPositions = np.insert(root.PrintEndLoads(), [0], [[-bucklingForce], [0]], axis=1)
#attachmentPositions = np.array([[-maxForce, 1.0375e3, 1.0375e3, 0.6166e3, 0.30833e3], [0, 0.45, 1.05, 1.75, 2.35]], dtype=np.float32)

#Shear force diagram in beam

def shearDiagram(position):
    shearAtPosition = -sum(attachmentPositions[0][position >= attachmentPositions[1][:]])
    return shearAtPosition
    
#Bending force diagram in beam

def bendingDiagram(position):
    bendingAtPosition = bucklingForce  * positionForce - sum(attachmentPositions[0][position >= attachmentPositions[1][:]] * attachmentPositions[1][position >= attachmentPositions[1][:]])
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
