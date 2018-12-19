#Mohamed Ameen Omar
#u16055323 
#EAI 320 - Practical 1
#2018
import googlemaps
import queue
from anytree import Node, RenderTree
gmaps = googlemaps.Client(key='AIzaSyD5Jjcpu_zl38yBDijOSELow5eZhGq6aic')
tuks = "University of Pretoria , Pretoria"
csir = "CSIR , Meiring Naude Road , Pretoria"
airforce = "Air Force Base Waterkloof, Centurion" #West Gate, Hans Strydom Drive, Lyttelton, Centurion, 0157
denel = "Denel Dynamics, Nellmapius Drive, Centurion"
armscor = "Armscor, Delmas Road, Pretoria"
nameOfCities = [csir,armscor,denel,airforce] #list of the locations besides the starting point
######################################### NODE CLASS #########################################
class node:
    def __init__(self, name, distance = 0, totalDistance = 0, parent = None, progeny = []):
        self.distance = distance #distance from parent to node
        self.name = name
        self.progeny = [] #list with all node's children
        self.totalDistance = totalDistance #totalDistance of the "Family" upto and inlcuding current node
        self.parent = parent
        self.visited = False    
        self.anyTreeNode = None        
    #adds the location passed in as a child for the current node
    def addChild(self, name):
        if(self.progeny != []):
            for x in range(0,len(self.progeny)):
                if(name == self.progeny[x].name):
                    return
        dist = gmaps.distance_matrix(self.name,name)['rows'][0]['elements'][0]['distance']['value']
        totalDist = self.totalDistance + dist
        tempNode = node(name,dist,totalDist,self)
        #tempNode.parent = self
        self.progeny.append(tempNode)    
    def isLeaf(self):
        if(self.progeny == []):
            return True
        return False
    #returns a list of the names of the current node's siblings
    def getSiblings(self):
        if(self.parent == None or self.parent.childHasSiblings() == False):
            return [""]
        siblings = []
        for x in range(0, len(self.parent.progeny)):
            if(self.parent.progeny[x].name != self.name):
                siblings.append(self.parent.progeny[x].name)
        return siblings    
    #checks if child has siblings
    def childHasSiblings(self):
        if (self.progeny == []):
            return False
        if(self.progeny == [""]):
            return False
        if(len(self.progeny) < 2):
            return False
        return True
    # Adds the siblings of current node as the children of current node, returns False if no siblings
    def addSiblingsAsChildren(self):
        siblings = self.getSiblings()
        if(siblings == [""] or siblings == []):
            return False        
        for x in range(0, len(siblings)):
            self.addChild(siblings[x])        
        return True
##############################################################################################################        
############################################# TREE CLASS #######################################################
class tree:
    def __init__(self,name):
        self.head = node(name)
    
    #recusive 
    def resetVisited(self):
        tempNode = self.head
        pseudoStack = [self.head]
        while(pseudoStack != []):
            tempNode = pseudoStack.pop()
            tempNode.visited = False            
            if(tempNode.progeny == []):
                continue
            for x in range(0,len(tempNode.progeny)):
                pseudoStack.append(tempNode.progeny[x])            
    #adds the first level 
    def addProgenyToHead(self, progeny = [""]):
        if(progeny == [""]):
            return
        for x in range(0,len(progeny)):           
            self.head.addChild(progeny[x])
    #recusive function to build the tree once the "base" level/level 2 has been built 
    def sortNodeChildren(self, tempNode):
        if(tempNode.childHasSiblings() == False):
            if(len(tempNode.progeny) == 1):
                tempNode = tempNode.progeny[0].addChild(self.head.name) #adds starting point as the ending point for the current path            
            return
        for x in range (0, len(tempNode.progeny)):            
            tempNode.progeny[x].addSiblingsAsChildren()
            self.sortNodeChildren(tempNode.progeny[x])    
    #adds locations to tree
    def addAllLocations(self, locations = [""]):
        if(locations == [""]):
            return        
        self.addProgenyToHead(locations)        
        if(self.head.progeny == []):            
            return        
        self.sortNodeChildren(self.head)
    #add a single location to the tree
    def insertSingleLocation(self, myString):
        if(self.head.progeny == []):
            thisString = [myString]
            self.addAllLocations(thisString)
            return        
        thisString = []
        for x in range(0, len(self.head.progeny)):
            thisString.append(self.head.progeny[x].name)        
        thisString.append(myString)        
        self.head = node(self.head.name)
        self.addAllLocations(thisString)
    #insert an additional list of locations to the tree   
    def insertMultipleLocations(self, myString):
        if(self.head.progeny == []):
            thisString = [myString]
            self.addAllLocations(thisString)
            return        
        thisString = []
        for x in range(0, len(self.head.progeny)):
            thisString.append(self.head.progeny[x].name)     
        for x in range(0, len(myString)):
            thisString.append(myString[x])
        self.head = node(self.head.name)
        self.addAllLocations(thisString)   
        
    #makes use of anyTree in  order to print the tree
    def printTree(self):
        if(self.head == None):
            print("No Tree has been constructed yet")
            return
        print("Printing tree\n")
        self.resetVisited()
        tempNode = self.head    
        myQueue = queue.Queue()    
        myQueue.put(tempNode)    
        while(myQueue.empty() == False):
            tempNode = myQueue.get()
            if(tempNode.visited == True):
                continue    
            tempNode.visited = True
            if(tempNode == self.head):
                self.head.anyTreeNode = Node(tempNode.name)
            else:
                tempNode.anyTreeNode = Node(tempNode.name, tempNode.parent.anyTreeNode)            
            for x in range(0,len(tempNode.progeny)):
                if(tempNode.progeny[x].visited == False):
                    myQueue.put(tempNode.progeny[x])                         
        self.resetVisited()    
        for pre, fill, x in RenderTree(self.head.anyTreeNode):
            print("%s%s  " % (pre, x.name))
############################################################################################################################## 
#returns a list with the route of the current path with the last node in the path passed in
def getPathFromEnd(tempNode):
    currentShortestPath = []
    while(tempNode != None):
        currentShortestPath.reverse()
        currentShortestPath.append(tempNode.name)
        currentShortestPath.reverse()
        tempNode = tempNode.parent
    return currentShortestPath
########################################## DFS #################################################################################        
#DFS for shortest path for a tree        
def DFS(myTree):
    myTree.resetVisited()
    tempNode = myTree.head
    numNodes = 0
    currentShortestDistance = -1
    currentShortestPath = []
    pseudoStack = []
    pseudoStack.append(tempNode)
    while(pseudoStack != []):
        tempNode= pseudoStack.pop()
        if(tempNode.visited == True):           
            continue        
        if( ( (currentShortestDistance <= tempNode.totalDistance) and currentShortestDistance != -1) or tempNode.visited == True): #if the path is longer or node already visited
            continue        
        numNodes = numNodes + 1
        tempNode.visited = True        
        if(tempNode.progeny == []): #lastNode
            if( (currentShortestDistance > tempNode.totalDistance) or currentShortestDistance == -1):
                currentShortestDistance = tempNode.totalDistance
                currentShortestPath = getPathFromEnd(tempNode)        
        if(tempNode.progeny != []):
            x = len(tempNode.progeny)
            for x in range(len(tempNode.progeny)-1, -1,-1):  
                if(tempNode.progeny[x].visited != True):
                    pseudoStack.append(tempNode.progeny[x])    
    print("Shortest Path is:", currentShortestPath)
    print("It's Distance is:", currentShortestDistance)
    print("Number of nodes visited by DFS is:",numNodes)
    myTree.resetVisited()    
########################################## BFS #################################################################################
def BFS(myTree):
    myTree.resetVisited()
    tempNode = myTree.head    
    myQueue = queue.Queue()    
    myQueue.put(tempNode)
    numNodes = 0
    path = []
    currentShortestDistance = -1
    while(myQueue.empty() == False):
        tempNode = myQueue.get()
        if(tempNode.visited == True):
            continue    
        tempNode.visited = True
        numNodes = numNodes+1
        if(tempNode.progeny == []):
            if(currentShortestDistance == -1 or currentShortestDistance > tempNode.totalDistance):
                currentShortestDistance = tempNode.totalDistance
                path = getPathFromEnd(tempNode)   
        for x in range(0,len(tempNode.progeny)):
            if(tempNode.progeny[x].visited == False):
                myQueue.put(tempNode.progeny[x])
    print("Shortest Path is:", path)
    print("It's Distance is:", currentShortestDistance)
    print("Number of nodes visited by BFS is:",numNodes)
    myTree.resetVisited()
    return
##############################################################################################################################    
############################################# main program ##################################################################      
myTree = tree(tuks)
print("Building Search Tree\n")
myTree.addAllLocations(nameOfCities)
print("Search Tree is Fully Built\n")
myTree.resetVisited()
myTree.printTree()   
print("")     
print("------------------------- DFS ----------------------------------")
DFS(myTree)
print("")
print("------------------------------- BFS ---------------------------")
BFS(myTree)