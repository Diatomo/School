

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

def maximize(resultLabel, results, labels):
    maxArr = [0,0,0,0,0]
    added = False
    for label in labels:
        temp = results['tValue'][label]
        for i in range(5):
            if (temp > maxArr[i] and added == False):
                maxArr.pop(i)
                resultLabel.pop(i)
                resultLabel.append(label)
                maxArr.append(temp)
                added = True
        added = False
    return maxArr


def main():
    #get data
    test = pd.ExcelFile("Testing_Data.xls")
    train = pd.ExcelFile("Training_Data.xls")

    dfTest = test.parse("Testing_Data")
    dfTrain = train.parse("Training_Data")

    notProg = {}
    prog = {}
    for i in range(len(dfTest)):
        try:
            if (dfTest.ix[i,'Label'] == 0):
                notProg.update(dfTest.ix[i,:])
            else:
                prog.update(dfTest.ix[i,:])
        except:
            pass

    print("BEFORE DATA FRAMED NOTPROG")
    print(notProg)
    print("BEFORE DATA FRAMED Prog")
    print(prog)
    pd.DataFrame(notProg)
    pd.DataFrame(prog)
    #print("AFTER DATA FRAMED NOTPROG")
    #print(notProg)
    #print("AFTER DATA FRAMED Prog")
    #print(prog)


    #analyze metaData (mean, std)
    dfTestAnalysis = dfTest.describe()
    dfTrainingAnalysis = dfTest.describe()

    #create list of attributes (genes)
    labels = []
    for label in dfTestAnalysis:
            labels.append(label)
    labels.remove('Sample_Number')
    labels.remove('Label')

    #create result array
    results = {'x0' : dfTestAnalysis.iloc[1], 'x1' : dfTrainingAnalysis.iloc[2],
               'std0' : dfTestAnalysis.iloc[1], 'std1' : dfTrainingAnalysis.iloc[2],
               'tValue' : {}, 'pValue' : {}}

    #two sample t-test
    for label in labels:
        tTest = (results['x1'][label] - results['x0'][label]) / ((results['std0'][label] / len(labels)) + (results['std1'][label] / len(labels)))
        results['tValue'].update({label : tTest})

    #find top 5 maxmimums
    resultLabel = [0,0,0,0,0]
    maxArr = maximize(resultLabel,results, labels)

    #output
    for i in range(len(maxArr)):
        print(resultLabel[i] + " : " + str(maxArr[i]))

main()
