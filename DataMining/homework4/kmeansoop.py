

import numpy as np
import scipy as sipy
import point as pt
import centroid as cent
import math

def distance(x1, x2, y1, y2):
    return (math.sqrt(pow(x1-x2,2) + pow(y1-y2,2)))

class Kmeans(object):
    '''
        @@Constructors
            kMeans object
            Point object
            Centroid object
====================================================================================
    '''

    def __init__(self, trainData, testData, k):
        #@private
        self._xRange = testData[0]
        self._yRange = testData[1]
        #@public
        self.centroids = self.initCentroids(k)
        self.trainData = (self.initPoints(trainData))
        self.testData = (self.initPoints(testData))
        self.testAccuracy = {}

    def initCentroids(self,k):
            centroids = []
            for i in range(k):
                centroids.append(cent.Centroid(self._xRange,self._yRange))#Ranges needed to generate random centroid
            return centroids

    def initPoints(self, data):
        points = []
        for i in range(len(data[1])):
            points.append(pt.Point(i, data[0][i],data[1][i],data[2][i]))
        return points

    '''
    @train && @test
        This function uses |nearestNeighbor && |matchingCentroids
        it
            Populates centroid Vectors with its nearest points.
            Reinits centroids which vectors are empty
            Adjust centroid location with respect to the means of its vector
                until
                    prevCentroid.vector = currCentroid.vector
===================================================================================
    '''
    def train(self):
        #kmeans algorithm
        x = self.trainData[0]
        y = self.trainData[1]
        self.nearestNeighbor(self.trainData)
        while (not self.matchingCentroids()):
            for i in range(len(self.centroids)):#reinit if centroid contains empty vector
                if (len(self.centroids[i].cVector) == 0):
                    self.centroids[i] = cent.Centroid(self._xRange, self._yRange)
            for i in range(len(self.centroids)):#adjust new (centroid.x, centroid.y)
                self.centroids[i].adjust()
            self.nearestNeighbor(self.trainData)#gain new set of neighbors
        for i in range(len(self.centroids)):
            self.centroids[i].classify()

    def test(self):
		self.nearestNeighbor(self.testData)
		accuracy = 0.0
		#test each point against centroid classifier
		for i in range(len(self.centroids)):
			for j in range(len(self.centroids[i].cVector)):
				#print(str(self.centroids[i].classifier) + ' ' + str(self.centroids[i].cVector[j].c))
				if (self.centroids[i].classifier == self.centroids[i].cVector[j].c):
					accuracy += 1.0
					#print(accuracy)
		#if (self.centroids[i].classifier != None):
		#	self.testAccuracy[i] = ((accuracy / len(self.centroids[i].cVector * 100)))
    '''
    ===================================================================================================
    '''
    def nearestNeighbor(self,data):
        for i in range(len(self.centroids)):
            self.centroids[i].pVector = list(self.centroids[i].cVector)#convergence measure
            self.centroids[i].cVector = []#clear current nN
        distances = []
        for i in range(len(data)):
            for j in range(len(self.centroids)):
                distances.append(distance(data[i].x, self.centroids[j].x, data[i].y, self.centroids[j].y))
            self.centroids[distances.index(min(distances))].cVector.append(data[i])
            distances = []

    def matchingCentroids(self):
        match = True
        for i in range(len(self.centroids)):
            if (len(self.centroids[i].cVector) != len(self.centroids[i].pVector)):
                match = False
        return match

    def results(self, data, points, centroids, accuracy):
        if (points):
            print("==============================")
            print("   POINTS     " )
            print("==============================")
            for i in range(len(self.trainData)):
                print("Point : " + str(data[i].pointid) + " : "
                                 + str(data[i].x) + " : "
                                 + str(data[i].y) + " | "
                                 + str(data[i].c))
        if (centroids):
            rCentroids = []
            print("==============================")
            print("   Centroids     " )
            print("==============================")
            for i in range(len(self.centroids)):
                cCentroid = self.centroids[i]
                #for j in range(len(cCentroid.cVector)):
                 #   rCentroids.append((cCentroid.cVector[j].x, cCentroid.cVector[j].y, cCentroid.cVector[j].c))
                print("Centroid : " + str(i) + " : Class = " +str(cCentroid.classifier))
                print("Centroid : " + str(i) + " : P(C|V) = " +str(cCentroid.classFreq))
                rCetroids = []

        if (accuracy):
            for key,value in self.testAccuracy.items():
                print("Centroid : " + str(key) + " : Accuracy = " +str(value))

