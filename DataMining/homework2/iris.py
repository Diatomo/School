
'''
======================================================
    Author: Charles C. Stevenson
    Date: The 15th of the Winter of the Solar Eclipse
    Description:
        kNN classifier
======================================================
'''


import pandas as pd
import math
import copy
import operator

'''
    @Helper Functions
    =================
'''
'''
    @keyWithMaxVal
        @param d
            +Type = dictionary

        return the key of the maximum value
        in the dictionary data structure
'''
def keyWithMaxVal(d):
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(max(v))]
'''
    @keyWithMinVal
        @param d
            +Type = dictionary

        return the key of the minimum value
        in the dictionary data structure
'''

def keyWithMinVal(d):
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(min(v))]

'''
    @createConfusion
        @param actual
            +Type = list
        @param predicted
            +Type = list

    Creates a Confusion Matrix to visualize a diagnosis
    on the performance of the kNN classifier
'''
def createConfusion(actual, predicted):
    y_actu = pd.Series(actual, name='Actual')
    y_pred = pd.Series(predicted, name='Predicted')
    df_confusion = pd.crosstab(y_actu, y_pred)
    return df_confusion
'''
    @Class kNN
        @param test
            +Type = csv
        @param train
            +Type = csv

        This class represents an object containing the
        kNN algorithm. This plots all the points test points
        and then the NN on the train set guess the class
        on the test set. The idea is depending on how
        one separates their data via the proximity measure
        one can get better results on the kNN classifier.
'''
class kNN(object):

    def __init__(self, train, test):
        self.train = pd.read_csv(train)
        self.test = pd.read_csv(test)
        self.classAcc = 0.0
        self.proximity = {} #{Test Point : {Train Point : ProximityMeasure,...}, ...}
        self.NN = {}#sorted proximity dictionary
        self.aClass = []#actual class
        self.pClass = []#predicted class
        self.postProb = []
    '''
        @proxMeasure
            @param r
                +Type = integer

        compares one record with all other records and populates
        a dictionary of all the comparisons. The proximity measure
        is either a 1 to 0 comparison or a variation of euclidean
        distance depending on r.
    '''
    def proxMeasure(self, r):
        average = 0.0
        self.proximity = {}
        for i in range(len(self.test)):#compare one record of test
            for j in range(len(self.train)):#with all records of train
                for k in range(len(self.test.loc[i])-1):#against the averages of all the attributes
                    if (r <= 1):
                            average += round(abs(self.test.loc[i][k] - self.train.loc[j][k]),3)#matching || no matching
                    else:
                            average += round(pow(self.test.loc[i][k] - self.train.loc[j][k],r),3)#variation of euclidean distance
                if (i not in self.proximity):
                    self.proximity.update({i : {}})
                average = (math.sqrt(average))
                self.proximity[i].update({j : average})
                average = 0.0
    '''
        @findNN
            @param k
                +Type = int

        findNN finds a minimum in a proximity and moves to NN
        so NN is the same dictionary format as proximity except,
        it only contains k NN as opposed to all of its neighbors
    '''
    def findNN(self, k):
        self.NN = {}
        tempProx = copy.deepcopy(self.proximity)
        for i in range(len(self.proximity)):
            for j in range(k):
                if (i not in self.NN):
                    self.NN.update({i : {}})
                minimum = keyWithMinVal(tempProx[i])
                if (j != 0):
                    self.NN[i].update({minimum : round(tempProx[i][minimum],2)})
                tempProx[i].pop(minimum, None)
    '''
        @classify()

        Takes a vote on NN classes to predict the record's class from the
        test set.
    '''
    def classify(self):
        self.aClass = []
        self.pClass = []
        self.postProb = []
        self.classAcc = 0.0
        for key, value in self.NN.items():#{point : {point : average}
            temp = {}
            self.aClass.append(self.test.loc[key,'class'])
            for point, average in self.NN[key].items():
                if self.train.loc[point, ' class'] not in temp:
                    temp[self.train.loc[point, ' class']] = 1.0
                else:
                    temp[self.train.loc[point, ' class']] += 1.0
            self.pClass.append(max(temp.items(), key=operator.itemgetter(1))[0])
            maximum = keyWithMaxVal(temp)
            self.postProb.append(temp[maximum]/len(self.NN[key])*100)
            if (self.aClass[-1] == self.pClass[-1]):
                self.classAcc += 1.0
        self.classAcc = round((self.classAcc / len(self.NN)) * 100,4)
    '''
        Outputs
            Print Functions to output dictionaries
    '''
    def printNeighbors(self):
        for key,value in self.NN.items():
            sortedNN = sorted(self.NN[key].items(), key=operator.itemgetter(1))
            print("Record = " + str(key) + " " + str(sortedNN))

    def printNeighborhood(self):
        for key,value in self.proximity.items():
            sortedNN = sorted(self.proximity[key].items(), key=operator.itemgetter(1))
            print("Record = " + str(key) + " " + str(sortedNN))

    def printResults(self,iris):
        print("ID :   Actual Class :   Predicted Class :   Probability")
        iris.write("ID :   Actual Class :   Predicted Class :   Probability\n")
        for i in range(len(self.aClass)):
            print(str(i) + "        " + str(self.aClass[i]) + "        " +
                    str(self.pClass[i]) + "       " + str(round(self.postProb[i],2)))
            iris.write(str(i) + "        " + str(self.aClass[i]) + "        " +
                    str(self.pClass[i]) + "       " + str(round(self.postProb[i],2)) + '\n')

    def printStats(self,iris):
        print("Classification Accuracy = " + str(self.classAcc))
        iris.write("Classification Accuracy = " + str(self.classAcc) +'\n')


def main():
    #evaluate iris dataset
    iriskNN = kNN("Iris.csv", "Iris_Test.csv")
    iris = open("irisResults.txt", "w")
    iriskNN.proxMeasure(2)
    for i in range(2,50,5):
        print("k = " + str(i))
        iris.write("k = " + str(i) + '\n')
        iriskNN.findNN(i)
        iriskNN.classify()
        print("==================================")
        iriskNN.printResults(iris)
        iriskNN.printStats(iris)
        confusion = createConfusion(iriskNN.aClass, iriskNN.pClass)
        print(confusion)
        iris.write(str(confusion) + '\n')
    iris.close()

main()

