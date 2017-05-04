import math
import random

probC = {}
counts = 0

'''
======================================

    Helper Functions

======================================
'''
def distance(coordA, coordB):
    return (math.sqrt(pow(coordA['x'] - coordB['x'],2) + (pow(coordA['y'] - coordB['y'], 2))))

def rando(ranges):
    return random.uniform(-ranges['max']/2, ranges['max']/2)
'''
    @Load
        Loads the Data Set into a dictionary
'''
def load():
    global probC
    data = {}
    counter = 1
    with open('hw2_testing.txt') as coordinates:
        for line in coordinates:
            line = line[:-1]
            line = line.split()
            data[counter] = {'x' : float(line[1]), 'y' : float(line[2]), 'classifier' : int(line[0])}
            if int(line[0]) not in probC:
                probC[int(line[0])] = 1
            else:
                probC[int(line[0])] += 1
            counter += 1
        for key,value in probC.items():
            probC[key] = value/(counter-1)
    return data

'''
    @scope
        measures max distance and min distance in data
'''
def scope(data):
    distances = []
    for pointA, coordinateA in data.items():#{point : coordinate} :: {1 : {x:y:classifier}
        for pointB, coordinateB in data.items():
            if (coordinateA != coordinateB):
                distances.append(distance(coordinateA, coordinateB))
    return {'max' : max(distances), 'min' : min(distances)}
'''
===========================

    Vector operations

==========================
'''
def initVectors(k, ranges):
    vectors = {}
    for i in range(k):
        vectors[i] = {'x' : rando(ranges), 'y' : rando(ranges), 'collection' : {}}
    return vectors

def reinitVector(index, vectors, ranges):
    vectors[index] = {'x' : rando(ranges), 'y' : rando(ranges), 'collection' : {}}

def clearVector(vectors):
    for i in range(len(vectors)):
        vectors[i]['collection'] = {}

def probInVec(vectors):
    probability = {}
    counter = 0.0
    for i in range(len(vectors)):
        #print("PRINT VECTOR " + str(vectors[i]))
        if i not in (probability):
            probability[i] = {}
        for key, value in vectors[i]['collection'].items():
            #print("VALUE = " + str(value))
            if value['classifier'] not in probability[i]:
                probability[i][value['classifier']] = 1
            else:
                probability[i][value['classifier']] += 1
            counter += 1.0
        for key, value in probability[i].items():
            probability[i][key] = round(probability[i][key] / counter, 3) * 100

        counter = 0
    return probability

'''
==============================

    K-MEANS

==============================
'''
'''
    @Convergence
        if a vector isn't filled reintialize the point
'''
def convergence(vectors,ranges):
    converge = True
    global counts
    counts += 1
    print(counts)
    for i in range(len(vectors)):
        if (len(vectors[i]['collection']) <= 0):
            reinitVector(i, vectors,ranges)
            converge = False
    if (counts > 100000):
        converge = True
    else:
        clearVector(vectors)
    return converge

def sumValues(vectors):
    avgX = 0.0
    avgY = 0.0
    counter = 0.0
    for i in range(len(vectors)):#{vector : {point : {x : 0, y; 0, classifier : 0}}}
        for key, value in vectors[i]['collection'].items():
            avgX += value['x']
            avgY += value['y']
            counter += 1.0
        if (counter == 0):
            counter = 1.0
        vectors[i]['x'] = avgX/counter
        vectors[i]['y'] = avgY/counter
        avgX = 0
        avgY = 0

def kmean(data, ranges, vectors):
    minimum = ranges['max']
    minVec = 0
    for point, coordinate in data.items():#check every point
        for vector, vectorCoord in vectors.items():#against ever vector
            measure = distance(vectorCoord, coordinate)
            if (measure < minimum):#Only add the point to its closest vector
                minimum = measure
                minVec = vector
        vectors[minVec]['collection'][point] = coordinate
        minimum = ranges['max']
        minVec = 0
    return vectors
'''
========================================

    MAIN

========================================
'''
def main():
    global probC#lazy global sorry (-_-)
    points = load()
    ranges = scope(points)
    k = 50
    vectors = initVectors(k, ranges)
    vectors = kmean(points, ranges, vectors)

    counter = 0
    while not convergence(vectors,ranges):
        vectors = kmean(points, ranges, vectors)
        sumValues(vectors)

    for key, value in vectors.items():
        print("VECTOR == " + str(key))
        print("VectorX == " + str(value['x']) + " VectorY == " + str(value['y']))
        print(" ")
        for point, coords in value['collection'].items():
            print("POINT = " + str(point) + " " + "COORDS = " + str(coords))
        print(" ")
    print(probC)

    probability = probInVec(vectors)
    print(probability)




main()

