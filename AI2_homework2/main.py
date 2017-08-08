
import kmeansoop as km
import numpy as np

def load(fileName):
    x,y,classifier = [], [], []
    with open(fileName) as coordinates:
        for line in coordinates:
            line = line[:-1]
            line = line.split()
            x.append(float(line[1]))
            y.append(float(line[2]))
            classifier.append(int(line[0]))
    return np.array([x,y,classifier])

def probabilities(kMeans):
    probabilities = {}
    for i in range(len(kMeans.trainData)):
        if (kMeans.trainData[i].c) not in probabilities:
            probabilities[kMeans.trainData[i].c] = 1.0
        else:
            probabilities[kMeans.trainData[i].c] += 1.0
    for key, value in probabilities.items():
        probabilities[key] = (value / len(kMeans.trainData))
    for key, value in probabilities.items():
        print("Class : " + str(key) + " Probability : " + str(value))
    return probabilities

def stats(averages,stdDev,kMeans,k):
    tempData = []
    for key, value in kMeans.testAccuracy.items():
        tempData.append(value)
    averages.append(np.average(tempData))
    stdDev.append(np.std(tempData))
    tempData = []
    print("==================================================================================")
    print("Averages for k = " + str(k) + " is " + str(averages))
    print("StdDev for k = " + str(k) + " is " + str(stdDev))

def main():
    averages = []
    stdDev = []
    k = [2,5,6,8,12,15,20,50]
    testData = load('hw2_training.txt')
    trainData = load('hw2_testing.txt')
    for i in k:
        kMeans = km.Kmeans(trainData, testData, i)
        kMeans.train()
        kMeans.test()
        #kMeans.results(kMeans.testData, False, True, True)
        #probabilities(kMeans)
        stats(averages,stdDev,kMeans,k)
    averages = []
    stdDev = []
main()
