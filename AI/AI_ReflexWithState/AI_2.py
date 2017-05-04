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


def loadHarness(f, q):
    for line in f:
        num = int (line[:-1])
        q.put(num)

class testHarness:
    #The testHarness contains all the info on the belts
    #It feeds this info to the agent who decides
    #which action to take
    #   Pickup, Advance, Drop, Fill
    def __init__(self, conveyerA, conveyerB, agent):
        #ConveyerA
        self.conveyerA = conveyerA
        self.convACurr = conveyerA.get()
        self.convANext = conveyerA.get()
        #ConveyerB
        self.conveyerB = conveyerB
        self.convBCurr = conveyerB.get()
        self.convBNext = conveyerB.get()
        #Slots
        self.slotOne = Queue()
        self.slotTwo = Queue()

        self.item = 0
        #Power
        self.power = 20
        self.agent = agent

    def run(self):
        action = ""
        while(action != "stop"):
            action = self.agent.reflexAgentWithState(self.convACurr, self.convANext, self.convBCurr, self.convBNext, self.power)

            if (action ==  "pickUpA"):
                self.item = self.convACurr
                self.convACurr = 0
            elif (action == "pickUpB"):
                self.item = self.convBCurr
                self.convBCurr = 0

            elif (action == "advanceA"):
                self.convACurr = self.convANext
                self.convANext = self.conveyerA.get()
            elif (action == "advanceB"):
                self.convBCurr = self.convBNext
                self.convBNext = self.conveyerB.get()

            elif (action == "dropOne"):
                self.slotOne.get()
            elif (action == "dropTwo"):
                self.slotTwo.get()

            elif (action == "fillOne"):
                self.slotOne.put(self.item)
            elif (action == "fillTwo"):
                self.slotTwo.put(self.item)

            self.power -= 1
            #print("OUTPUT ACTION: " + str(action))


class Agent:
    #Reflex Agent with State
    #Contains a State variable to keep track of its actions
    #The test harness feeds in data and the agent
    #returns with an action for the test harness
    #to perform.
    def __init__(self):
        fillOne = 0
        fillTwo = 0
        pickup = 0
        self.state = [fillOne, fillTwo, pickup]

    def reflexAgentWithState(self, currA, nextA, currB, nextB, power):
        #alias state variables
        slotOne = self.state[0]
        slotTwo = self.state[1]
        held = self.state[2]
        #declare return value: action
        action = " "

        print("INPUT PERCEPTION: " + str(currA) + " " + str(nextA) + " " + str(currB) + " " + str(nextB) + " "+ str(power))
        if (power > 0):

            #evaluate Agent's state for action
            if (held > slotOne and slotOne != 0 and slotTwo != 0):
                action = "dropOne"
                self.state[0] = 0
            elif (held > 0 and slotOne == 0):
                action = "fillOne"
                self.state[0] = self.state[2]
                self.state[2] = 0
            elif (held > 0 and slotTwo == 0):
                action = "fillTwo"
                self.state[1] = self.state[2]
                self.state[2] = 0
            elif (held > slotTwo and slotTwo != 0):
                action = "dropTwo"
                self.state[1] = 0

            #evaluate beltA for pickup action
            elif (currA == 0 or (currA > nextA and currA > currB)):
                if (currA > slotOne or currA > slotTwo):
                    action = "pickUpA"
                    self.state[2] = currA
                else:#currA is maximum, but not when in relation with slots
                    action = "advanceA"

            #evaluate beltB for pickup action
            elif (currB == 0 or (currB > nextB and currB > currA)):
                if (currB > slotOne or currB > slotTwo):
                    action = "pickUpB"
                    self.state[2] = currB
                else:#currB is maximum, but not when in relation with slots
                    action = "advanceB"

            #Maximum Next gets Advanced
            elif (nextA  < nextB):
                action = "advanceB"
            elif (nextB < nextA):
                action = "advanceA"

            #if both belts are empty stop
            elif (currA == -1 and currB == -1):
                action = "stop"

        #else out of power: stop
        else:
            action = "stop"

        print("AGENT STATE: " + "(" + str(slotOne) + "," + str(slotTwo) + "," + str(held) + ")" + " " + str(currA) + " " + str(nextA) + " " + str(currB) + " " + str(nextB))
        print("OUTPUT ACTION: " + str(action))
        print(" ")
        return action



def main():
    #file I/O
    fileA = "conveyerA.txt"
    fileB = "conveyerB.txt"

    fA = open(fileA, 'r+')
    fB = open(fileB, 'r+')

    #build Queues
    conveyerA = Queue()
    conveyerB = Queue()

    loadHarness(fA, conveyerA)
    loadHarness(fB, conveyerB)

    #Create && Run
    agent = Agent()
    test = testHarness(conveyerA, conveyerB, agent)
    test.run()

main()
