'''

    Author: Charles C. Stevenson
    Date : October 31st, 2016
    Description :

        This is a program that uses value iteration to learn the
        best path from a starting web link to the best web link.
        Basically an abstract version of a program learning how
        to solve a maze

'''

from math import *
import sys

error = 0.001


'''these are just the maximum part of the bellham equation'''
def maxutil(utility):
    maximum = -1
    actions = ['S','G','B']
    for i in range(len(actions)):
        util = utility[actions[i]]
        if (util > maximum):
            maximum = util
    return maximum

def maxprob(state, markov, i):
    maximum = -1
    prob = 0
    transitions = dict(state.transition)
    keys = [a for a in dir(state.transition) if not a.startswith('__')]
    #for i in range(len(keys)):
    transition = transitions[keys[i]]
    for j in range(len(transition['dest'])):
            nextState = markov.states[transition['dest'][j] - 1]
            utility = nextState.utility
            prob += transition['prob'][j] * maxutil(utility)
            #print("PROBABILITY MAX + " + str(prob))
        #if (prob > maximum):
            #maximum = prob

            #state.policy = transition['action']

    return prob

'''objects'''
class Iter(object):#an explicit iterator
    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            yield attr, value

'''The objects are done in a composite pattern where:
        markov contains an array of states
        states contains a transition object
        transition contains 3 dictionary and is the transition model
'''
class Markov(Iter):
    def __init__(self):
        self.states = []
        self.gamma = 0.9

class State(Iter):
    def __init__(self, reward):
        self.reward = reward
        self.utility = {'S' : 0, 'G' : 0, 'B' : 0}
        self.policy = ""
        self.transition = Transition()

class Transition(Iter):
    def __init__(self):
        self.s = {}
        self.g = {}
        self.b = {}

'''This is the main value iteration loop'''
def valueiteration(markov, error):
    for i in range(len(markov.states)):
        if (len(markov.states[i].transition.s) > 2):
            markov.states[i].utility['S'] = markov.states[i].reward + markov.gamma * maxprob(markov.states[i], markov,0)
            markov.states[i].utility['G'] = markov.states[i].reward + markov.gamma * maxprob(markov.states[i], markov,1)
            markov.states[i].utility['B'] = markov.states[i].reward + markov.gamma * maxprob(markov.states[i], markov,2)


def parse(fPlaces, fTransitions, markov):#parses the file
   # print()
    #print("PLACES")
    #print("=================================")
    for line in fPlaces:
        line = line[:-1]
        line = line.split(',')
        #print(line)
        reward = float(line[3])
        state = State(reward)
        markov.states.append(state)
    #print("TRANSITIONS")
    #print("================================")
    for line in fTransitions:
        line = line[:-1]
        line = line.split(',')
        #print(line)
        #aliases
        start = int(line[0])
        state = markov.states[int(line[0])-1]
        action = line[1]
        dest = [int(line[2]), int(line[4]), int(line[6])]
        prob = [float(line[3]),float(line[5]),float(line[7])]
        #select which transition to populate
        if (action == 'S'):
            transition = state.transition.s
        elif (action == 'G'):
            transition = state.transition.g
        else:
            transition = state.transition.b
        #populate transitions
        transition["start"] = start
        transition["action"] = action
        transition["dest"] = dest
        transition["prob"] = prob

    for i in range(len(markov.states)):
        if (len(markov.states[i].transition.s) < 2):
            markov.states[i].utility['S'] = markov.states[i].reward
            markov.states[i].utility['G'] = markov.states[i].reward
            markov.states[i].utility['B'] = markov.states[i].reward

def main():
    #open files
    if (len(sys.argv) != 3):
        sys.exit("CHECK ARGUMENTS")
    fPlaces = open(sys.argv[1], 'r+')
    fTransitions = open(sys.argv[2], 'r+')
    if (fPlaces == None or fTransitions == None):
        sys.exit("FILES DID NOT OPEN CORRECTLY")

    #populate objects
    markov = Markov()
    parse(fPlaces, fTransitions, markov)
    #Bellham's Equation
    #valueiteration()

    #PARSE TEST
    '''
    print()
    print("=====================================================")
    print("MARKOV")
    print("MARKOV STATES: " + str(markov.states))
    print("MARKOV STATES (0 - 9)")
    for i in range(10):
        print("MARKOV STATE[" + str(i) + "]: " +str(markov.states[i]))

    print
    print("MARKOV STATES AND TRANSITIONS")
    for i in range(10):
        print("MARKOV STATE TRANSITION: " + str(markov.states[i].transition.s))
        print("MARKOV STATE TRANSITION: " + str(markov.states[i].transition.g))
        print("MARKOV STATE TRANSITION: " + str(markov.states[i].transition.b))

    print("=====================================================")
    '''
    #runs value iterator until the error is matches.
    utility = markov.states[1].utility['S']
    nextUtility = 0
    counter = 0
    delta = abs(utility - nextUtility)
    execute = True
    while (delta > (error * (1 - markov.gamma)/markov.gamma) or execute):
        execute = False
        utility = markov.states[1].utility['S']
        print("UTILITY\n" + str(utility))
        valueiteration(markov, error)
        counter+=1
        nextUtility = markov.states[1].utility['S']
        print("NEXTUTILITY \n" + str(nextUtility))
        delta = abs(utility - nextUtility)
        print("DELTA \n")
        print(delta)
        print("============")

    print("results")
    print(counter)
    for i in range(len(markov.states)):
        if (len(markov.states[i].transition.s) > 2):
               print("QState (" + str(i+1) + "," + str(markov.states[i].transition.s['action']) + "): Utility=" + str(markov.states[i].utility[markov.states[i].transition.s["action"]]))
               print("QState (" + str(i+1) + "," + str(markov.states[i].transition.g['action']) + "): Utility=" + str(markov.states[i].utility[markov.states[i].transition.g["action"]]))
               print("QState (" + str(i+1) + "," + str(markov.states[i].transition.b['action']) + "): Utility=" + str(markov.states[i].utility[markov.states[i].transition.b["action"]]))

main()



