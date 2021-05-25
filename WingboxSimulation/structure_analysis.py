import numpy as np


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

#Wingbox class : gets a list of rectangular structural elements in format [[xCg, yCg, xLength, yLength]] and the loads applied in format [[load1, load2, load3....], [position1, position2,  ....]]

class Wingbox:

    def __init__(self, structuralElements, loadApplied):

        self.structuralElements = structuralElements
        self.loadApplied = loadApplied

    #Shear force diagram in beam

    def shearDiagram(self, position):
        mask = position >= self.loadApplied[1, :]
        mask[0] = False
        shearAtPosition = -sum(self.loadApplied[0, mask])
        return shearAtPosition
    
    #Bending force diagram in beam

    def momentDiagram(self, position, momentType):
        mask = position >= self.loadApplied[1, :]
        mask[0] = False
        if(momentType == 'bending'):
            bendingAtPosition = self.loadApplied[0, 0]  * self.loadApplied[1, 0] - sum(self.loadApplied[0, mask] * self.loadApplied[1, mask])
            return bendingAtPosition
        if(momentType == 'torsion'): 
            torsionAtPosition = self.loadApplied[0, 0] * self.loadApplied[2, 0] - sum(self.loadApplied[0, mask] * self.loadApplied[2, mask])
            return torsionAtPosition

    def cgCalculator(self, structuralElements):
        structuralElements = np.concatenate((structuralElements, np.array([structuralElements[:, 2]*structuralElements[:, 3]]).T), axis=1)
        xCg = (sum(structuralElements[:, 0]*structuralElements[:, 4])/sum(structuralElements[:, 4]))
        yCg = (sum(structuralElements[:, 1]*structuralElements[:, 4])/sum(structuralElements[:, 4]))
        return xCg, yCg

    def secondMomentArea(self, xLength, yLength, xParallelAxis, yParallelAxis, axis):
        if(axis == 'x'):
            return ((yLength**3*xLength)/12 + xLength*yLength*yParallelAxis**2)
        else:
            return ((yLength*xLength**3)/12 + xLength*yLength*xParallelAxis**2) 

    def secondMomentAreaAssembly(self, structuralElements, axisSMA): #structuralElements[xCg, yCg, xLength, yLength, ]
        cg = self.cgCalculator(structuralElements)
        return sum(self.secondMomentArea(structuralElements[:, 2], structuralElements[:, 3], abs(cg[0]-structuralElements[:, 0]), abs(cg[1]-structuralElements[:, 1]), axisSMA))

    def cutElements(self, structuralElements, axis, height):
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
        
    def firstMomentAreaAssembly(self, structuralElements, axis, height):
        cgReference = self.cgCalculator(structuralElements)
        if(axis == 'x'):
            structuralElementsCut = self.cutElements(structuralElements, 'y', height)
            structuralElementsCut = np.concatenate((structuralElementsCut, np.array([structuralElementsCut[:, 2]*structuralElementsCut[:, 3]]).T), axis=1)
            cgPart = self.cgCalculator(structuralElementsCut)[1]
            return abs(cgReference[1]-cgPart)*sum(structuralElementsCut[:, 2]*structuralElementsCut[:, 3])
        else: 
            structuralElementsCut = self.cutElements(structuralElements, 'x', height)
            structuralElementsCut = np.concatenate((structuralElementsCut, np.array([structuralElementsCut[:, 2]*structuralElementsCut[:, 3]]).T), axis=1)
            cgPart = self.cgCalculator(structuralElementsCut)[0]
            return abs(cgReference[0]-cgPart)*sum(structuralElementsCut[:, 2]*structuralElementsCut[:, 3])

    def normalBendingStress(self, positionFromRoot, axis, height=None):
        if(axis == 'x'):
            SMA = self.secondMomentAreaAssembly(self.structuralElements, axis)
            neutralAxisPosition = self.cgCalculator(self.structuralElements)[1]
            if(height != None):
                return self.momentDiagram(positionFromRoot, 'bending')*abs(neutralAxisPosition-height)/SMA
            else:    
                if(neutralAxisPosition > 0.15 - neutralAxisPosition): #Stress is always the biggest the furthest from the neutralaxis
                    return self.momentDiagram(positionFromRoot, 'bending')*neutralAxisPosition/SMA
                else:
                    return self.momentDiagram(positionFromRoot, 'bending')*(0.15-neutralAxisPosition)/SMA
        else:  #this part is not yet finished and will yield incoherent results
            SMA = self.secondMomentAreaAssembly(self.structuralElements, axis)
            neutralAxisPosition = self.cgCalculator(self.structuralElements)[0]
            if(height != None):
                return self.momentDiagram(positionFromRoot, 'bending')*abs(neutralAxisPosition-height)/SMA
            else:
                if(neutralAxisPosition > 0.15 - neutralAxisPosition):
                    return self.momentDiagram(positionFromRoot, 'bending')*neutralAxisPosition/SMA
                else:
                    return self.momentDiagram(positionFromRoot, 'bending')*(0.15-neutralAxisPosition)/SMA
            
    def shearStressDueToShearForce(self, positionFromRoot, height, axis):
        SMA = self.secondMomentAreaAssembly(self.structuralElements, axis)
        FMA = self.firstMomentAreaAssembly(self.structuralElements, axis, height)
        return self.shearDiagram(positionFromRoot)*FMA/(SMA*0.0015)

    def shearStressDueToTorsion(self, positionFromRoot, thickness): #using thin-walled assumption
        meanLength = np.max(self.structuralElements[0])- np.min(self.structuralElements[0])
        meanHeight = np.max(self.structuralElements[1])- np.min(self.structuralElements[1])
        meanArea = meanLength*meanHeight
        torque = self.momentDiagram(positionFromRoot, "torsion")
        return torque/(meanArea*2*thickness)

    def shearStress(self, positionFromRoot, height, axis, thickness):
        return self.shearStressDueToShearForce(positionFromRoot, height, axis) + self.shearStressDueToTorsion(positionFromRoot, thickness)