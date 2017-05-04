

'''
    Author: Charles C. Stevenson
    Date: 01/26/2017
    Description: Create Proximity table for the income data set
'''

import pandas as pd
import numpy as np
import operator
import math


def keyWithMaxVal(d):
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(max(v))]

def keyWithMinVal(d):
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(min(v))]

def match(record1, record2):
    matching = 1
    if (record1 == record2):
        matching = 0
    return matching

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

def scale(name, income):
    #scales values down between 0 and 1
    attribute = income.loc[:,name]
    maximum = float(max(attribute))
    for i in range(len(attribute)):
        income.loc[i] = income.loc[i].replace(income.loc[i,name], income.loc[i,name]/maximum)

def similarity(income, r):
    proximity = {}
    average = 0
    for i in range(len(income)):
        print(i)
        for j in range(len(income)):
            for k in range(len(income.loc[i])-1):
            #workclass = 1 #race = 7 #marital_status = 3 #relationship = 6 #occupation = 5 (Matching descriptors)
                if (r <= 1):
                    if (k == 1 or k == 7 or k == 3 or k == 6 or k == 5):
                        average += round(abs(match(income.loc[i][k], income.loc[j][k])),3)
                    else:
                        average += round(abs(income.loc[i][k] - income.loc[j][k]),3)
                else:
                    if (k == 1 or k == 7 or k == 3 or k == 6 or k == 5):
                        average += round(abs(match(income.loc[i][k], income.loc[j][k])),3)
                    else:
                        average += round(pow(income.loc[i][k] - income.loc[j][k],r),3)

            if (i not in proximity):
                proximity.update({i : {}})
            #average = average / (len(income.loc[i])-1)
            proximity[i].update({j : average})
            average = 0
    return proximity

def proximity(sim, income, k):
    proxMin = {}
    for i in range(len(income)):#look through all the records
        for j in range(k):#kth nearest neighbor
            if (i not in proxMin):
                proxMin.update({i : {}})
            minimum = keyWithMinVal(sim[i])
            if (j != 0):
                proxMin[i].update({minimum : round(sim[i][minimum],2)})#Add minimums
            sim[i].pop(minimum, None)#remove minum as to not grab it again

    return proxMin

def main():
    dfIncome = pd.read_csv("income_tr.csv") #read data
    incomeProx = open("incomeProxEuclid.txt" , "w")

    #drop irrelevant attributes
    dfIncome.drop('ID', axis=1, inplace=True)
    dfIncome.drop('education', axis=1, inplace=True)
    dfIncome.drop('fnlwgt', axis=1, inplace=True)

    #clean data
    nominal('native_country', dfIncome)
    nominal('occupation', dfIncome)
    scale('education_cat', dfIncome)
    scale('hour_per_week',dfIncome)
    scale('age', dfIncome)
    scale('capital_gain', dfIncome)
    scale('capital_loss', dfIncome)

    k = 10
    #calculates similarities, creates a proximity matrix, sorts the proximity matrix and outputs to a file
    #for i in range(1,k,1): TODO uncomment to calculate kth neighbors
    incomeProx.write("\n")
    incomeProx.write("Record    Record:Dissimilarity, k = " + str(k) + "\n")
    sim = similarity(dfIncome, 1) #Similarity
    prox = proximity(sim, dfIncome, k+1) #Proximity Matrix
    for key,value in prox.items():
        sortedProx = sorted(prox[key].items(), key=operator.itemgetter(1))#Sorts
        incomeProx.write("Record = " + str(key) + " " + str(sortedProx) + "\n")#Output
        print("Record = " + str(key) + " " + str(sortedProx))
    incomeProx.close()

    incomeProx = open("incomeProxSquare.txt" , "w")
    #calculates similarities, creates a proximity matrix, sorts the proximity matrix and outputs to a file
    #for i in range(1,k,1): TODO uncomment to calculate kth neighbors
    incomeProx.write("\n")
    incomeProx.write("Record    Record:Dissimilarity, k = " + str(k) + "\n")
    sim = similarity(dfIncome, 2) #Similarity
    prox = proximity(sim, dfIncome, k+1) #Proximity Matrix
    for key,value in prox.items():
        sortedProx = sorted(prox[key].items(), key=operator.itemgetter(1)) #Sorts
        incomeProx.write("Record = " + str(key) + " " + str(sortedProx) + "\n") #Output
        print("Record = " + str(key) + " " + str(sortedProx))
    incomeProx.close()

main()

