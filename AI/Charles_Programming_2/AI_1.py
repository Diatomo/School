#
#
#
#  Author : Charles Stevenson
#  Date : 09/03
#  Description: Class based Agent.
#
#
#


from Queue import *


def readFile(f, q):
    for line in f:
        num = int (line[:-1])
        q.put(num)

class testHarness:
    def __init__(self, conveyerA, agent):
        self.conveyerA = conveyerA
        self.agent = agent

    def run(self):
        action = ""
        precept1 = self.conveyerA.get()
        precept2 = self.conveyerA.get()
        while (action != "STOP"):
            print("INPUT PERCEPTION: " + str(precept1) + " " + str(precept2))
            action = self.agent.reflexAgent(precept1, precept2)
            if (action == "ADVANCE"):
                precept1 = precept2
                precept2 = self.conveyerA.get()
            elif (action == "PICKUP"):
                precept1 = 0
            print("OUTPUT ACTION: " + str(action))

class Agent:
    def __init__(self):
        self.action = " "
        self.pCurr = 0
        self.pNext = 0

    def reflexAgent(self,precept1, precept2):
        self.pCurr = precept1#Precept Curr
        self.pNext = precept2#Precept Next
        if (self.pCurr != -1):#if current isn't null
            if (self.pCurr > self.pNext and self.pCurr != 0):#if curr is > next
                self.action = "PICKUP"
            elif (self.pCurr < self.pNext or self.pCurr == 0):
                self.action = "ADVANCE"
        else:
            self.action = "STOP"

        return self.action

def main():
    fileName = "reflex1.txt"

    f = open(fileName, 'r+')
    conveyerA = Queue()

    readFile(f,conveyerA)

    agent = Agent()
    test = testHarness(conveyerA, agent)
    test.run()
   # while not q.empty():
    #    agent.compare(precept1, precept2)
     #   if (simpleAgent.action != "Pickup"):
      #      precept1 = precept2
       #     precept2 = q.get()
        #else:
         #   precept1 = 0
   # if q.empty():
    #    agent.action = "Stop"
     #   agent.pCurr = precept1
      #  agent.output()
main()
