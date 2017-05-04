'''

    Author: Charles C. Stevenson
    Date : October 31st, 2016i
    Title: QValueIterator
    Description :

        This is a program that uses value iteration to learn the 
        best path from a starting web link to the best web link.
        Basically an abstract version of a program learning how
        to solve a maze

'''

import math
import sys

error = 0.001

'''these are just the maximum part of the bellham equation'''
def maxi(state, markov):
    maximum = -1
    transitions = dict(state.transition)
    keys = [a for a in dir(state.transition) if not a.startswith('__')]#iterate through fields s{},g{},b{}
    for i in range(len(keys)):#for each transition: s{}, g{}, b{}
        transition = transitions[keys[i]]
        nextState = transition['dest'] - 1#get the index for the next destination
        prob = transition['prob'] * markov.states[nextState].utility#multiply current prob by next states utility
        if (prob > maximum):#find maximum probability
            maximum = prob#set max
            state.policy = transition['action']#set policy or suggested decision
    return maximum


'''objects'''
class Iter(object):
    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            yield attr, value

'''
        The objects are done in a composite pattern where:
        markov contains an array of states
        states contains a transition object
        transition contains 3 dictionaries and which are the transition models
            e.g. {'action': s, 'prob' : [x,y,z] 'dest' : [x,y,z]...}
'''
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

'''Bellhams Equation'''
def valueiteration(markov, error):
    for i in range(len(markov.states)):
        if (len(markov.states[i].transition.s) > 2):
            markov.states[i].utility = markov.states[i].reward + markov.gamma * maxi(markov.states[i], markov)

'''parse function'''
def parse(fPlaces, fTransitions, markov):
    for line in fPlaces:
        line = line[:-1]
        line = line.split(',')
        reward = float(line[3])
        state = State(reward)
        markov.states.append(state)
    for line in fTransitions:
        line = line[:-1]
        line = line.split(',')
        start = int(line[0])
        state = markov.states[int(line[0])-1]
        action = line[1]
        dest = int(line[2])
        prob = float(line[3])
        if (action == 'S'):
            transition = state.transition.s
        elif (action == 'G'):
            transition = state.transition.g
        else:
            transition = state.transition.b
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

    #loop through value iterator
    utility = markov.states[1].utility
    nextUtility = 0
    delta = abs(utility - nextUtility)
    execute = True #make a do-while loop
    while (delta > (error * (1 - markov.gamma)/markov.gamma) or execute):
        utility = markov.states[1].utility
        valueiteration(markov, error)
        execute = False
        nextUtility = markov.states[1].utility
        delta = abs(utility - nextUtility)

    #output
    for i in range(len(markov.states)):
        print("State " + str(i+1) + ": Utility= " + str(markov.states[i].utility) + " Policy= " + str(markov.states[i].policy))

main()

