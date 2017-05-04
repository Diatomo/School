

'''
	Author : Charles C. Stevenson
	Date : 03/04/2017
	Description:
		This file runs a t-test on expression data
		Ranks them by the most significant && outputs
		the genes with the highest values on the t-test
'''

import numpy as np
import pandas as pd
import math
from scipy.stats import norm

'''
def bonferri(results, labels):
    alpha = .05

    for 
    bonferri = []
'''

'''
	fxn = maximize
	Maximizes The T-test from the expression data
'''
def maximize(resultLabel, results, labels):
    maxArr = [-50,-50,-50,-50,-50]#array of gene scores
    added = False#if added break
    for label in labels:
        temp = results['tValue'][label]#grab gene's tValue
        for i in range(5):#look through array
            if (temp > maxArr[i] and added == False):
                maxArr.pop(i)
                resultLabel.pop(i)
                resultLabel.append(label)
                maxArr.append(temp)
                print(label)
                added = True
        added = False
    return maxArr

def LDAclassifier(df):
    accuracy = 0.0
    total = 0.0
    BBC3 = df.ix[0:,'BBC3']
    CENPA = df.ix[0:,'CENPA']
    CFFM4 = df.ix[0:,'CFFM4']
    for i in range(len(df)):
        if (-8.1028 * CENPA[i] + 3.5380 * BBC3[i] + 0.3239 * CFFM4[i] - 1.9215 > 0):
            accuracy += 1.0
        total += 1.0
    return accuracy / total * 100

def main():
    #get data
    test = pd.ExcelFile("Testing_Data.xls")
    train = pd.ExcelFile("Training_Data.xls")

    dfTest = test.parse("Testing_Data")
    dfTrain = train.parse("Training_Data")

    #analyze metaData (mean, std)
    dfTest.drop('Sample_Number', axis=1, inplace=True)
    dfTrain.drop('Sample_Number', axis=1, inplace=True)
    dfTestAnalysis = dfTest.describe()
    dfTrainingAnalysis = dfTrain.describe()

    #create list of attributes (genes)
    labels = []
    for label in dfTestAnalysis:
            labels.append(label)
    #labels.remove('Sample_Number')
    labels.remove('Label')

    #create result array
    results = {'x0' : dfTestAnalysis.iloc[1], 'x1' : dfTrainingAnalysis.iloc[1],
               'std0' : dfTestAnalysis.iloc[2], 'std1' : dfTrainingAnalysis.iloc[2],
               'tValue' : {}, 'pValue' : {}}

    #two sample t-test
    for label in labels:
	print(label)
	print("avg group1 = " + str(results['x0'][label]))
	print("avg group2 = " + str(results['x1'][label]))
	avg = (results['x0'][label] - results['x1'][label])
	print("avg : %f" % avg)
	print("std group1 = " + str(results['std0'][label]))
	print("std group2 = " + str(results['std1'][label]))
	std = math.sqrt((((results['std0'][label])**2) / 235.0) + (((results['std1'][label])**2) / 60.0))
	print("std : %f" % std)
	tTest = avg/std
	print("tTest = %f" % tTest)
        results['tValue'].update({label : tTest})

    #find top 5 maxmimums
    resultLabel = [0,0,0,0,0]
    maxArr = maximize(resultLabel,results, labels)

    avg = 0
    print(results)
    #print(len(results))
   
    ''' 
    for i in range(len(results)):
        if results[i]['pValue'] <= 0.05/70:
            avg += 1.0
    print(avg)
    '''
 
    #output
    for i in range(len(maxArr)):
        print(str(resultLabel[i]) + " : " + str(maxArr[i]))
    holdout = LDAclassifier(dfTest)
    resub = LDAclassifier(dfTrain)
    print("Holdout = " + str(holdout))
    print("ReSub = " + str(resub))
    
    

main()
