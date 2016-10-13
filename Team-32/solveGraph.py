import math
import time
class Node:
        def __init__(self, x, y, color, name):
                self.name = name
                self.x = x
                self.y = y
                self.color = color
                self.connectedNodes = set()
        def connectNode(self, otherNode):
                self.connectedNodes.add(otherNode)
                otherNode.connectedNodes.add(self)

class NodeSet:
        def __init__(self):
                self.low = -1
                self.high = -1
                self.size = 0
                self.value = 0
                self.color = "null"
                self.nodeList = set()
        #Adds a node and all connected nodes to this set.
        #Called recursively.
        def add(self, node):
                if node not in self.nodeList:
                        self.size = self.size + 1
                        self.value = self.value + 1
                if self.low == -1:
                        self.low = node.y
                if self.high == -1:
                        self.high = node.y
                if node.y > self.low:
                        self.low = node.y
                if node.y < self.high:
                        self.high = node.y
                self.nodeList.add(node)
                self.color = node.color
                for surroundingNode in node.connectedNodes:
                        if surroundingNode not in self.nodeList:
                                self.add(surroundingNode)
        def display(self):
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
 #               print(startNode.name, end='')
  #              print(endNode.name)
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
#                touchedNodeList = set()
                
        def solveValue(self):
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
                return bestPath


class NodeMap:
        distanceThreshold = 250
        def __init__(self):
                self.allNodes = list()
                self.nodeSetList = set()
        def add(self, node):
                self.allNodes.append(node)
        def connectNodes(self):
                i = 0
                for node in self.allNodes[:]:
                        i = i + 1
                        for checkNode in self.allNodes[i:]:
                                if (node.color == checkNode.color and node != checkNode and checkNode not in node.connectedNodes):
                                        #print(str(node.x)+ "    " + str(node.y))
                                        distance = math.sqrt(abs(float(node.x - checkNode.x)) **2 + abs(float(node.y - checkNode.y))** 2)
                                        if distance <= NodeMap.distanceThreshold:
                                                node.connectNode(checkNode)
        def formNodeSets(self):
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
                                unformedNodes.remove(node)

        def getNextPattern(self):
                for nodeSet in self.nodeSetList:
                        if not bestNodeSet:
                               bestNodeSet = nodeSet 
                        if nodeSet.value > bestNodeSet.value:
                                bestNodeSet = nodeSet
                        elif nodeSet.value == bestNodeSet.value:
                                #If new node is closer to the top of the screen...
                                if nodeSet.low < bestNodeSet.low:
                                        bestNodeSet = nodeSet
                return bestNodeSet
        
#40 tsums


timeA = time.time()

def createMap(inputMap):
        thisMap = NodeMap()
        #FIX check for empty lists
        for type in range(len(inputMap)):
                thisType = inputMap[type]
                for node in thisType:
                        thisMap.add(Node(node[0],node[1], type, str(node[0]) + " " + str(node[1])))
        thisMap.connectNodes()
        thisMap.formNodeSets()
        for nodeSet in thisMap.nodeSetList:
                #REMOVE THIS
#                nodeSet.display()
                solvedPath =nodeSet.solveValue()
                if(solvedPath is not None):
                    for node in solvedPath:
                            print(node.name, end ='->')
                    print("")
                    return solvedPath
                return []

#tsums = list()
#tsums.append([5,8,1])
#tsums.append([3,8,1])
#tsums.append([1,8,1])
#types = list([tsums,list(),list(),list(),list()])
##fullMap = list([types])
#createMap(types)
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
