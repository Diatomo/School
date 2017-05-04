'''
======================================================
    Author: Charles C. Stevenson
    Date: The 15th of the Winter of the Solar Eclipse
    Description:
        kNN classifier
======================================================
'''


import pandas as pd
import copy
import operator
import pylab

'''
    @Helper Functions
    =================
'''
'''
    @keyWithMaxVal
        @param: d
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
        @param: d
            +Type = dictionary

        return the key of the minimum value
        in the dictionary data structure
'''
def keyWithMinVal(d):
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(min(v))]
'''
    @Match
        @param: record1
            +Type = String
        @param record2
            +Type = String

    Evaluates nominal data and returns 1 if not matching and
    0 if matching.
'''
def match(record1, record2):
    matching = 1
    if (record1 == record2):
        matching = 0
    return matching
'''
    @nominal
        @param: name
            +Type = string
        @param: income
            +Type = dataframe

    Converts nominal data to numerical value, this converts
    nominal data to be representative by how often it shows
    up in the data set. (normalization function)
'''
def nominal(name, income):
    #calulates and transforms frequency at which it is represented in the data set
    temp = {}
    records = []
    attribute = income.loc[:,name]
    #count
    for i in range(len(attribute)):
        if (attribute[i] not in temp):
            temp.update({attribute[i] : 1})
        else:
            temp[attribute[i]] += 1.0
    #create probabilities
    for key in temp:
        temp[key] = temp[key] / len(attribute)
    for i in range(len(attribute)):
        income.loc[i] = income.loc[i].replace(income.loc[i,name], temp[income.loc[i,name]])
'''
    @scale
        @param: name
            +Type = string
        @param: income
            +Type = dataframe

    Scales the numerical values to values between 0 and 1
    (normalization function)
'''
def scale(name, income):
    #scales values down between 0 and 1
    attribute = income.loc[:,name]
    maximum = float(max(attribute))
    for i in range(len(attribute)):
        income.loc[i] = income.loc[i].replace(income.loc[i,name], income.loc[i,name]/maximum)
'''
    @cleanData
        @param: df
            +Type = dataframe

    Specific for the income data set, cleans up and
    aggregates uneeded fields, this is hard coded specific
    for the income data set.
'''
def cleanData(df):
    df.drop('ID', axis=1, inplace=True)
    df.drop('education', axis=1, inplace=True)
    df.drop('fnlwgt', axis=1, inplace=True)
    nominal('native_country', df)
    nominal('occupation', df)
    scale('education_cat', df)
    scale('hour_per_week',df)
    scale('age', df)
    scale('capital_gain', df)
    scale('capital_loss', df)
    return df
'''
    @createConfusion
        @param actual
            +Type = list
        @param predicted
            +Type = list

    Creates a Confusion Matrix to visualize a diagnosis
    on the performance of the kNN classifier
'''
'''def createConfusion(actual, predicted):
    y_actu = pd.Series(actual, name='Actual')
    y_pred = pd.Series(predicted, name='Predicted')
    df_confusion = ConfusionMatrix(y_actu, y_pred)
    return df_confusion
'''

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
        self.train = cleanData(pd.read_csv(train))
        self.test = cleanData(pd.read_csv(test))
        self.classAcc = 0.0
        self.proximity = {} #{Test Point : {Train Point : ProximityMeasure,...}, ...}
        self.NN = {}#sorted proximity dictionary
        self.aClass = []#actual class
        self.pClass = []#predicted class
        self.postProb = []
        self.stats = {}
        self.TP = []
        self.FN = []
        self.FP = []
        self.TN = []
        self.Pre = []
        self.Rec = []
        self.TPR = []
        self.FPR = []
        self.Fmeas = []
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
        for i in range(len(self.test)):
            print(i)
            for j in range(len(self.train)):
                for k in range(len(self.train.loc[i])-1):
                    #workclass = 1 #race = 7 #marital_status = 3 #relationship = 6 #occupation = 5 (Matching descriptors)
                    if (r <= 1):#Matching nominal data
                        if (k == 1 or k == 7 or k == 3 or k == 6 or k == 5):
                            average += round(abs(match(self.test.loc[i][k], self.train.loc[j][k])),3)
                        else:
                            average += round(abs(self.test.loc[i][k] - self.train.loc[j][k]),3)
                    else:#euclidean distance
                        if (k == 1 or k == 7 or k == 3 or k == 6 or k == 5):
                            average += round(abs(match(self.test.loc[i][k], self.train.loc[j][k])),3)
                        else:
                            average += round(pow(self.test.loc[i][k] - self.train.loc[j][k],r),3)
                if (i not in self.proximity):
                    self.proximity.update({i : {}})
                self.proximity[i].update({j : average})
                average = 0.0
        return self.proximity
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
        self.stats ={'tPos' : 0.0, 'fNeg' : 0.0, 'fPos' : 0.0, 'tNeg' : 0.0 }
        for key, value in self.NN.items():#looks at test house
            temp = {}
            self.aClass.append(self.test.loc[key,'class'])
            for point, average in self.NN[key].items():#looks through all the trained neighbors
                if self.train.loc[point, 'class'] not in temp:#add classes if not in dict
                    temp[self.train.loc[point, 'class']] = 1.0
                else:
                    temp[self.train.loc[point, 'class']] += 1.0
            self.pClass.append(max(temp.iteritems(), key=operator.itemgetter(1))[0])#classify test as max
            maximum = keyWithMaxVal(temp)
            self.postProb.append((temp[maximum]/len(self.NN[key]))*100)
            if (self.aClass[-1] == ' <=50K' and self.pClass[-1] == ' <=50K'):#calculate total classification accuracy
                self.classAcc += 1.0
                self.stats['tPos'] += 1.0
            elif (self.aClass[-1] == ' >50K' and self.pClass[-1] == ' >50K'):
                self.stats['tNeg'] += 1.0
                self.classAcc += 1.0
            elif (self.aClass[-1] == ' <=50K' and self.pClass[-1] == ' >50K'):
                self.stats['fNeg'] += 1.0
            else:
                self.stats['fPos'] += 1.0
        self.classAcc = round((self.classAcc / len(self.NN)) * 100,4)
    '''
        Outputs
            Print Functions to output dictionaries
    '''
    def printNeighbors(self,income):
        for key,value in self.NN.items():
            sortedNN = sorted(self.NN[key].items(), key=operator.itemgetter(1))
            print("Record = " + str(key) + " " + str(sortedNN))
            income.write("Record = " + str(key) + " " + str(sortedNN) + '\n')

    def printNeighborhood(self,income):
        for key,value in self.proximity.items():
            sortedNN = sorted(self.proximity[key].items(), key=operator.itemgetter(1))
            print("Record = " + str(key) + " " + str(sortedNN))
            income.write("Record = " + str(key) + " " + str(sortedNN) + '\n')

    def printResults(self,income):
        print("ID :   Actual Class :   Predicted Class :   Probability")
        income.write("ID :   Actual Class :   Predicted Class :   Probability")
        for i in range(len(self.aClass)):
            print(str(i) + "        " + str(self.aClass[i]) + "        " +
                  str(self.pClass[i]) + "       " + str(round(self.postProb[i],2)))
            income.write(str(i) + "        " + str(self.aClass[i]) + "        " +
                  str(self.pClass[i]) + "       " + str(round(self.postProb[i],2)) + '\n')

    def printStats(self,income):
        print("Classification Accuracy = " + str(self.classAcc))
        income.write("Classification Accuracy = " + str(self.classAcc) + '\n')

def main():
    #evaluate iris dataset
    incomekNN = kNN("income_tr.csv", "income_te.csv")
    income = open("incomeResults.txt" , "w")
    incomekNN.proxMeasure(2)
    for i in range(2,50,5):
        print("k = " + str(i))
        income.write("k = " + str(i) + '\n')
        incomekNN.findNN(i)
        incomekNN.classify()
        print("==================================")
        incomekNN.printResults(income)
        incomekNN.printStats(income)
        #confusion = createConfusion(incomekNN.aClass, incomekNN.pClass)
        #print(confusion)
        #income.write(str(confusion))
        a = incomekNN.stats['tPos']
        b = incomekNN.stats['fNeg']
        c = incomekNN.stats['fPos']
        d = incomekNN.stats['tNeg']
        print("TP : " + str(a))
        print("FN : " + str(b))
        print("FP : " + str(c))
        print("TN : " + str(d))
        print("PRE : " + str(a / (a + c)))
        print("Rec : " + str(a / (a + b)))
        print("Fmeas : " + str((2*a) / (2*a + b + c)))
        income.write("TP : " + str(a) + '\n')
        income.write("FN : " + str(b) + '\n')
        income.write("FP : " + str(c) + '\n')
        income.write("TN : " + str(d) + '\n')
        income.write("PRE : " + str(a / (a + c)) + '\n')
        income.write("Rec : " + str(a / (a + b)) + '\n')
        income.write("Fmeas : " + str((2*a) / (2*a + b + c)) + '\n')
        incomekNN.TP.append(a)
        incomekNN.FN.append(b)
        incomekNN.FP.append(c)
        incomekNN.TN.append(d)
        incomekNN.Pre.append((a / (a + c)))
        incomekNN.Rec.append(a / (a + b))
        incomekNN.Fmeas.append((2*a) / (2*a + b + c))
    #incomekNN.linePlot(range(2,50,5))
    income.close()

main()

