'''

    Author: Charles C. Stevenson
    Date : October 31st, 2016
    Description :

        This is a program that uses value iteration to learn the 
        best path from a starting web link to the best web link.
        Basically an abstract version of a program learning how
        to solve a maze

'''

import math
import sys

error = 0.001

def maxi(state, markov):
    maximum = -1
    transitions = dict(state.transition)
    keys = [a for a in dir(state.transition) if not a.startswith('__')]
    for i in range(len(keys)):
        transition = transitions[keys[i]]
        nextState = transition['dest'] - 1
        prob = transition['prob'] * markov.states[nextState].utility
        if (prob > maximum):
            maximum = prob
            state.policy = transition['action']

    return maximum

class Iter(object):
    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            yield attr, value

class Markov(Iter):
    def __init__(self):
        self.states = []
        self.gamma = 0.9

class State(Iter):
    def __init__(self, reward):
        self.reward = reward
        self.utility = 0
        self.policy = ""
        self.transition = Transition()

class Transition(Iter):
    def __init__(self):
        self.s = {}
        self.g = {}
        self.b = {}


def valueiteration(markov, error):
    for i in range(len(markov.states)):
        if (len(markov.states[i].transition.s) > 2):
            markov.states[i].utility = markov.states[i].reward + markov.gamma * maxi(markov.states[i], markov)

def parse(fPlaces, fTransitions, markov):
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
    #print()
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
        dest = int(line[2])
        prob = float(line[3])
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
            markov.states[i].utility = markov.states[i].reward

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
    fPlaces.close()
    fTransitions.close()

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
    utility = markov.states[1].utility
    nextUtility = 0
    counter = 0
    delta = abs(utility - nextUtility)
    execute = True
    while (delta > (error * (1 - markov.gamma)/markov.gamma) or execute):
        utility = markov.states[1].utility
        print("UTILITY\n" + str(utility))
        valueiteration(markov, error)
        execute = False
        counter+=1
        nextUtility = markov.states[1].utility
        print("NEXTUTILITY \n" + str(nextUtility))
        delta = abs(utility - nextUtility)
        print("DELTA \n")
        print(delta)
        print("============")

    #for i in range(100):
     #   valueiteration(markov, error)

    print("results")
    print(counter)
    for i in range(len(markov.states)):
        print("State " + str(i+1) + ": Utility= " + str(markov.states[i].utility) + " Policy= " + str(markov.states[i].policy))

main()

