
import pandas as pd
import operator

def keyWithMaxVal(d):
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(max(v))]

def keyWithMinVal(d):
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(min(v))]

def similarity(iris, r):
    proximity = {}
    average = 0
    for i in range(len(iris)):
        print(i)
        for j in range(len(iris)):
            for k in range(len(iris.loc[i])-1):
                if (r <= 1):
                        average += round(abs(iris.loc[i][k] - iris.loc[j][k]),3)
                else:
                        average += round(pow(iris.loc[i][k] - iris.loc[j][k],r),3)

            if (i not in proximity):
                proximity.update({i : {}})
            proximity[i].update({j : average})
            average = 0
    return proximity

def proximity(sim, iris, k):
    proxMin = {}
    for i in range(len(iris)):
        for j in range(k):
            if (i not in proxMin):
                proxMin.update({i : {}})
            minimum = keyWithMinVal(sim[i])
            if (j != 0):
                proxMin[i].update({minimum : round(sim[i][minimum],2)})
            sim[i].pop(minimum, None)
    return proxMin

def main():
    dfIris = pd.read_csv("Iris.csv") #read data
    irisProx = open("irisProxEuclid.txt" , "w")

    k = 4
    for i in range(1,k,1):
        irisProx.write("\n")
        irisProx.write("Record    Record:Dissimilarity, k = " + str(k) + "\n")
        sim = similarity(dfIris, 1)
        prox = proximity(sim, dfIris, i+1)
        for key,value in prox.items():
            sortedProx = sorted(prox[key].items(), key=operator.itemgetter(1))
            irisProx.write("Record = " + str(key) + " " + str(sortedProx) + "\n")
            print("Record = " + str(key) + " " + str(sortedProx))
    irisProx.close()

main()

