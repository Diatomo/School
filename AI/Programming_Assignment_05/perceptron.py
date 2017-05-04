'''
    Author: Charles C. Stevenson
    Date: 11/25/2016
    Description: Perceptron
'''
from random import choice
import numpy
from numpy import dot, random
import time
import os


def perceptron(trainingData, weights):
    unit_step = lambda x: 0 if x <= 0 else 1

    w = random.rand(weights)#bias is included in the vectors
    n = 10000

    for i in range(n):
        x, expected = choice(trainingData)#choose and x and an expected
        result = dot(w, x)#calculate weighted sum
        error = expected - unit_step(result)#if error
        w += error * x#update the weights

    print("WEIGHTS (w): " + str(w))
    for x, _ in trainingData:
        result = dot(x,w)
        print("{}: {} -> {}".format(x[:3], result, unit_step(result)))


def loadTrainingSet(f):
    training = []
    arr = []
    for line in f:
        line = line[:-1]
        temp = line.split(',')
        for i in range(len(temp)-1):
            arr.append(int(temp[i]))
        tempArr = (numpy.array(arr), int(temp[-1]))
        training.append(tempArr)
        arr = []
    print(training)

    return training

def main():
    files = []
    #fileRes = open('results.txt', 'w')
    for fileName in os.listdir('.'):
        if (fileName != "perceptron.py" and fileName != "results.txt" and fileName != "README"):
            files.append(fileName)

    print (str(files))
    for data in files:
        f = open(data, 'r+')
        print("=========================")
        print("FILE: " + data)
        weights = int(f.readline())
        trainingData = loadTrainingSet(f)
        perceptron(trainingData, weights)
        print
        print("=========================")
        f.close()

main()
