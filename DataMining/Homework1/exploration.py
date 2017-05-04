


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly as py
import plotly.graph_objs as go
from sets import Set



def nominal(name, income):
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
        temp[key] = round(temp[key] / len(attribute),3) * 100

    return temp


def values(d):
    values = []
    for key, value in d.items():
        values.append(value)
    return values

def labels(d):
    labels = []
    for key,value in d.items():
        labels.append(key)
    return labels

def main():
    dfIncome = pd.read_csv("income_tr.csv") #read data
    #OccLabels = labels('occupation',dfIncome)
    d = nominal('class', dfIncome)
    lab = labels(d)
    val = values(d)
    for i in range(len(val)):
        val[i] = round(val[i], 3)

    fig = {
            'data': [{'labels': lab,
                      'values': val,
                      'type': 'pie'}],
            'layout': {'title': "Income"}
           }

    py.offline.plot(fig)

main()


'''
    fig = {
            'data': [{'labels': lab,
                      'values': val,
                      'type': 'pie'}],
            'layout': {'title': "Occupations"}
           }
'''
