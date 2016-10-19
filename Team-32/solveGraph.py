# https://github.com/fireflyes/Team-32-tsum-
import math
import time

class Node:
        """A node storing the data of a single tsum and its connections to
        other tsums of the same type"""
        def __init__(self, x, y, color, name):
                self.name = name
                self.x = x
                self.y = y
                self.color = color
                self.connectedNodes = set()
        def connectNode(self, otherNode):
                """Add connections between this node and another node."""
                self.connectedNodes.add(otherNode)
                otherNode.connectedNodes.add(self)

class NodeSet:
        """A set of nodes of the same type.  Initially this should be a list of
        nodes that are not a path.  Once you call solve value nodeList will
        contain a path. """
        def __init__(self):
                self.low = -1
                self.high = -1
                self.size = 0
                self.value = 0
                self.color = "null"
                self.nodeList = list()
                self.isPath = False
        def add(self, node):
                """Adds a node and all connected nodes(by any number of links)
                to this set."""
                if node not in self.nodeList:
                        self.size = self.size + 1
                if self.low == -1:
                        self.low = node.y
                if self.high == -1:
                        self.high = node.y
                if node.y > self.low:
                        self.low = node.y
                if node.y < self.high:
                        self.high = node.y
                self.nodeList.append(node)
                self.color = node.color
                for surroundingNode in node.connectedNodes:
                        if surroundingNode not in self.nodeList:
                                self.nodeList.append(surroundingNode)
        def display(self):
                """Display data about this nodeSet."""
                print("Node: ", end='')
                print(self)
                print("Low: ",end='')
                print(self.low)
                print("High: ",end='')
                print(self.high)
                print("Size: ",end='')
                print(self.size)
                print("Color: ",end='')
                print(self.color)
        def findLongestPath(self, startNode, endNode, touchedNodeList = list()):
                """Recursively finds the longest path between startNode and
                endNode"""
                touchedNodeList.append(startNode)
                bestPath = list()
                #We found the end node; return path to it.
                if startNode == endNode:
                        tempList= list(touchedNodeList)
                        touchedNodeList.remove(startNode)
                        return tempList
                #Find maximum of all branching paths and return longest of these.
                for node in (startNode.connectedNodes - set(touchedNodeList)):
                        tempList = self.findLongestPath(node, endNode, touchedNodeList)
                        #If tempList is not empty(aka found a path to end node)
                        if tempList != None: 
                                if len(tempList) > len(bestPath):
                                        bestPath = list(tempList)                                              
                #If none of the connecting nodes lead to end node..
                touchedNodeList.remove(startNode)
                if len(bestPath) == 0:
                        return None
                return bestPath
                
        def solveValue(self):
                if len(self.nodeList) == 1:
                        self.value = 1
                        self.isPath = True
                        return self.nodeList
                """Finds the longest path in the entire nodeSet(between any two
                points)"""
                if self.isPath == True:
                        return self.nodeList
                bestPath = None
                for startNode in self.nodeList:
                        destinationNodeSet = set(self.nodeList)
                        destinationNodeSet.remove(startNode)
                        for destNode in destinationNodeSet:
                                thisPath = self.findLongestPath(startNode, destNode)
                                #Error: thisPath is sometimes returning nonetype
                                if thisPath != None:
                                        if bestPath == None or len(thisPath) > len(bestPath):
                                                bestPath = thisPath
                                else:
                                        bestPath = thisPath

                self.nodeList = bestPath
                #print(self.nodeList)
                self.value = len(bestPath)
                self.isPath = True
     
                return bestPath


class NodeMap:
        """Management class for all nodes."""
        distanceThreshold = 145
        def __init__(self):
                self.allNodes = list()
                self.nodeSetList = set()
        def add(self, node):
                self.allNodes.append(node)
        def createMap(self, inputMap):
                """Creates and sets up a map of all nodes."""
                #print(inputMap)
                #print(self.nodeSetList)
                #Create node map and add all nodes to it.
                typeIndex = 0
                for thisType in inputMap:
                        for node in thisType:
                                self.add(Node(node[0],node[1], typeIndex, str(node[0]) + " " + str(node[1])))
                        typeIndex = typeIndex + 1
                i = 0
                for node in self.allNodes[:]:
                        i = i + 1
                        for checkNode in self.allNodes[i:]:
                                if (node.color == checkNode.color and node != checkNode and checkNode not in node.connectedNodes):
                                        if (abs(float(node.x - checkNode.x))) > NodeMap.distanceThreshold or (abs(float(node.y - checkNode.y))) > NodeMap.distanceThreshold:
                                                distance = math.sqrt(abs(float(node.x - checkNode.x)) **2 + abs(float(node.y - checkNode.y))** 2)
                                                if distance <= NodeMap.distanceThreshold:
                                                        node.connectNode(checkNode)

                #for nodeSet in thisMap.nodeSetList:
                 #       solvedPath =nodeSet.solveValue()
                  #      if(solvedPath is not None):
                   #         for node in solvedPath:
                    #                print(node.name, end ='->')
                    #        print("")
                    #        return solvedPath
                    #    return []
                #Deep copy node list into a new set.
                unformedNodes = set(self.allNodes)
                formedNodes = set()
                #While there are still unformed nodes...
                while unformedNodes:
                        nodeSet = NodeSet()
                        self.nodeSetList.add(nodeSet)
                        node = unformedNodes.pop()
                        #Seems kind of ugly but is actually the fastest way to get an element without removing.
                        unformedNodes.add(node)
                        nodeSet.add(node)
                        for node in nodeSet.nodeList:
                                if node in unformedNodes:
                                        unformedNodes.remove(node)
        def getAllPaths(self, paths=None):
                if paths == None:
                        paths = []
                self.nodeSetList
                if not self.nodeSetList:
                        return []
                bestPath = None
                for nodeSet in self.nodeSetList:
                        if bestPath == None:
                                nodeSet.solveValue()
                                bestPath = nodeSet
                        if not nodeSet.isPath:
                                if len(nodeSet.nodeList) >= bestPath.value:
                                        nodeSet.solveValue()
                                        if(nodeSet.value > bestPath.value):
                                                bestPath = nodeSet
                                        elif(nodeSet.value == bestPath.value):
                                                if(nodeSet.low < bestPath.low):
                                                        bestPath = nodeSet
                                else:
                                        break
                #Remove all nodeSets above the low point
                for nodeSet in list(self.nodeSetList):
                        if nodeSet.high <= bestPath.low:
                                self.nodeSetList.remove(nodeSet)
                fPath = list()
                for node in bestPath.nodeList:
                        fNode = list()
                        fNode.append(node.x)
                        fNode.append(node.y)
                        fPath.append(fNode)
                paths.append(fPath)
                self.getAllPaths(paths)
                return(paths)
        
        
#40 tsums


#timeA = time.time()


#tsums = list()
#tsums.append([5,8,1])
#tsums.append([3,8,1])
#tsums.append([1,8,1])
#types = list([tsums,list(),list(),list(),list()])
##fullMap = list([types])
#NM = NodeMap()
#NM.createMap(types)
#print(NM.getAllPaths())
##a = list()
##a.append(Node(0,0,"red", "a1"))
##a.append(Node(1,1,"red", "a2"))
##a.append(Node(2,1,"red", "a3"))
##a.append(Node(3,2,"red", "a4"))
##a.append(Node(3,0,"red", "a5"))
##a.append(Node(4,1,"red", "a6"))
##NM = NodeMap()
##for node in a:
##        NM.add(node)
##NM.connectNodes()
##NM.formNodeSets()
##for z in NM.allNodes:
##        print("Node: ", end='')
# #       print(z.name, end='')
#  #      print(": ", end='')
#   #     print(z)
#       # print(z.x)
#    #    print("x: " + str(z.x) + " y: " + str(z.y))
#     #   print("Nodes: ",end='')
##        for za in z.connectedNodes:
#   #             print(za.name, end='')
#   #     print('')

##for zb in NM.nodeSetList:
##        zb.display()
##        for node in  (zb.solveValue()):
##                print(node.name)
##print("END")

#timeB =time()
#print("Elapsed Time: ", end='')
#print(timeB - timeA)
