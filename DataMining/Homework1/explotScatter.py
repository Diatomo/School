import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly as py
import plotly.graph_objs as go
from sets import Set



def nominal(name, income):
    temp = {name : []}
    for i in range(len(income)):
        temp[name].append(income.loc[i,name])
    return temp

def makingMoney(name,income):
    temp = {name: []}
    for i in range(len(income)):
        if (income.loc[i,name] == " <=50K"):
            temp[name].append(0)
        else:
            temp[name].append(1)
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
    #d = nominal('class', dfIncome)

    age = nominal('hour_per_week',dfIncome)
    income = makingMoney('class',dfIncome)
    plt.xlabel("Class")
    plt.ylabel("Hours_Per_Week")
    plt.title("Hours_Per_Week vs Money_Made")
    plt.scatter(income['class'],age['hour_per_week'])
    plt.show()

main()
