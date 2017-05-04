
"""

    Title: Artificial Intelligence Search Algorithms
    Author: Charles Stevenson
    Date: 09/12/2016

    Description:
        This takes two inputs as strings that define the initial state
        and searches for the most efficient solution using BFS and Astar

        The problem is four robots who move at different speeds come across a bridge
        they have to figure out how to get over the bridge, when only two can travel
        over the bridge at any time and move at the speed of the slowest robot.
        They are constrained by a powerpack which in a sense allows them to move.

        so... In which order should they cross?

"""
from Queue import *
import sys

#global dictionary
robots = {'A' : 1, 'B' : 2, 'C' : 5, 'D' : 10, 'P' : 0} #robot A takes 1 unit to cross the bridge, P = powerPack

class Node:
    '''A node'''
    def __init__(self,parent,left,right,botWalk,cost,tCost,depth):
        self.parent = parent
        self.left = left
        self.right = right
        self.botWalk = botWalk
        self.cost = cost
        self.tCost = tCost
        self.depth = depth
        self.action = ()#left/right, botWalk
        self.children = PriorityQueue()#(costs, node)
        self.nChild = []

    def output(self):
        print("=====================================================")
        if (self.parent != None):
            print("Parents: " + str(self.parent.left) + " | "+ str(self.parent.right))
        print("ActionLR: " +str(self.left) + " | " + self.botWalk + " | " + str(self.right))
        print("Cost : " + str(self.tCost)) + " Depth: " + str(self.depth)
        print("=====================================================")


class TestHarness:
    '''deliver seed to the agent, to create a graph then searches
       for the optimal path to the solution
    '''
    def __init__(self, agent):
        self.agent = agent
        self.goalState = "ABCDP"
        self.optCost = 100

    def graph(self,root):
        node = root
        q = Queue()
        q.put(node)
        if(node.right != self.goalState):
            while (q.empty() == False):
                node = q.get()
                if (node.parent != None):
                    node.tCost += node.parent.tCost
                    if (node.right == self.goalState):
                        if(node.tCost < self.optCost):
                            self.optCost = node.tCost
                node.output()
                self.agent.genTree(node)
                for v in node.nChild:
                    q.put(v)
        print("optimal solution cost = " + str(self.optCost))

    def search(self,root):
        '''Searches the path for the optimal solution'''
        node = root
        expanded = 0
        path = []
        path.append(root)
        #expand
        if(self.optCost == 100):
            self.optCost = 0
        while(node.tCost != self.optCost):
            if(node.tCost > self.optCost):
                node = node.parent
                path.pop()
            elif (node.children.empty() == True):
                node = node.parent
                path.pop()
            else:
                nAction = node.children.get()
                node = nAction[1]
                path.append(node)
                expanded += 1

        #output
        print("\n\n======================")
        print("Solution")
        print("======================\n\n")
        path.reverse()
        while(len(path) != 0):
            node = path.pop()
            node.output()
        print(expanded)

class Agent:
    '''returns a list of nodes to expand'''
    def __init__(self):
        pPos = ""
        botWalk = ""
        self.state = [pPos, botWalk]

    def pathCost(self,botWalk):
        '''Finds Path Cost of Slowest Robot'''
        maximum = 0
        for i in range(len(botWalk)):
            if (maximum < robots[botWalk[i]]):
                maximum = robots[botWalk[i]]
        return maximum

    def directionState(self,left,right):
        '''Determines which side the powerPack is on'''
        pPos = right
        if (left != ""):
            for i in left:
                if (i == 'P'):
                    pPos = left
                else:
                    pPos = right
        return pPos

    def sortPos(self,pos):
        '''Sorts strings for cleanliness'''
        arr = []
        for i in pos:
            arr.append(i)
        arr.sort()
        pos = ""
        if len(arr) > 0:
            for i in range(len(arr)):
                pos += arr[i]

        return pos

    def genTree(self, parent):
        #initials
        pPos = self.directionState(parent.left,parent.right) #set direction for node generation
        self.state[0] = pPos
        botWalk = ""
        tempL = parent.left
        tempR = parent.right
        action = True

        #pPack Left Decision Nodes
        if (pPos == parent.left):
            action = True
            for i in range(len(pPos)-2):
                for j in range(i+1,len(pPos)-1):
                    #initials
                    botWalk += pPos[i]
                    botWalk += pPos[j]
                    botWalk += 'P'
                    for k in botWalk:
                        tempL = tempL.replace(k,"")
                    tempR += botWalk
                    tempL = self.sortPos(tempL)
                    tempR = self.sortPos(tempR)
                    #Node Generation
                    node = (Node(parent,tempL,tempR,botWalk,self.pathCost(botWalk),self.pathCost(botWalk),parent.depth+1))
                    parent.children.put((self.pathCost(botWalk), node),self.pathCost(botWalk) + parent.cost,node)
                    parent.nChild.append(node)
                    #cleanup
                    botWalk = ""
                    tempL = parent.left
                    tempR = parent.right
        #pPack Right Decision Nodes
        else:
            action = False
            for i in range(len(pPos)-1):
                    #initials
                    botWalk += pPos[i]
                    botWalk += 'P'
                    tempL += botWalk
                    for k in botWalk:
                        tempR = tempR.replace(k,"")
                    tempL = self.sortPos(tempL)
                    tempR = self.sortPos(tempR)
                    #Node Generation
                    node = (Node(parent,tempL,tempR,botWalk,self.pathCost(botWalk), self.pathCost(botWalk),parent.depth+1))
                    node.action = (action, botWalk)
                    parent.children.put((self.pathCost(botWalk), node),self.pathCost(botWalk) + parent.cost,node)
                    parent.nChild.append(node)
                    #cleanup
                    botWalk = ""
                    tempL = parent.left
                    tempR = parent.right

def main():
    #initials
    if len(sys.argv) != 3:
        sys.exit("Check Arguments")
    left = sys.argv[1]
    right = sys.argv[2]

    #Objects
    agent = Agent()
    root = Node(None,left,right,"",0,0,0)
    testHarness = TestHarness(agent)

    #search
    testHarness.graph(root)
    testHarness.search(root)

main()
