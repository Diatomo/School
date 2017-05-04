
import numpy as np

class Centroid(object):
    '''
        @Centroid
            central position of a vector
            contains neighestNeighbors information
    '''
    def __init__(self, x, y):
        self.x = np.random.uniform(min(x), max(x))
        self.y = np.random.uniform(min(y), max(y))
        self.cVector = []
        self.pVector = []
        self.classifier = None
        self.classFreq = {}

    def adjust(self):
        distX = 0.0
        distY = 0.0
        if (len(self.cVector) != 0):
            for i in range(len(self.cVector)):
                distX += self.cVector[i].x
                distY += self.cVector[i].y
            self.x = distX / len(self.cVector)
            self.y = distY / len(self.cVector)

    def classify(self):
        maximum = 0
        classifier = None
        for i in range(len(self.cVector)):
            if self.cVector[i].c not in self.classFreq:
                self.classFreq[self.cVector[i].c] = 1.0
            else:
                self.classFreq[self.cVector[i].c] += 1.0
        for key,value in self.classFreq.items():
            self.classFreq[key] = value / len(self.cVector) * 100
            if (maximum < (value / len(self.cVector) * 100)):
                maximum = (value / len(self.cVector) * 100)
                classifier = key
        self.classifier = classifier
