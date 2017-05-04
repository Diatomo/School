
import kmeansoop as km
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

colors = ['r', 'g', 'b', 'y','m','k','c']

def load(fileName):
	x,y,classifier = [], [], []
	df = pd.read_csv(fileName)
	df.drop('ID', axis = 1, inplace = True)
	for i in range(len(df)):
		x.append(float(df.loc[i][0]))
		y.append(float(df.loc[i][1]))
		classifier.append(int(df.loc[i][2]))
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
		pass
        #print("Class : " + str(key) + " Probability : " + str(value))
    return probabilities

def stats(averages,stdDev,kMeans,k):
    tempData = []
    for key, value in kMeans.testAccuracy.items():
        tempData.append(value)
    averages.append(np.average(tempData))
    stdDev.append(np.std(tempData))
    tempData = []
    #print("==================================================================================")
    #print("Averages for k = " + str(k) + " is " + str(averages))
    #print("StdDev for k = " + str(k) + " is " + str(stdDev))

def sumSquare(kMeans):
	sse = 0.0
	for centroid in kMeans.centroids:
		temp = 0.0
		for point in centroid.cVector:
			temp += (point.x - centroid.x)**2 + (point.y - centroid.y)**2
		sse += temp
	print("The sum of squares is %d" % sse)

def sumBetSquare(kMeans):
	sse = 0.0
	for centroidA in kMeans.centroids:
		temp = 0.0
		for centroidB in kMeans.centroids:
			for point in centroidA.cVector:
				temp += (point.x - centroidB.x)**2 + (point.y - centroidB.y)**2
			sse += temp
	print("The sum between squares is %d" % sse)

def main():
	averages = []
	stdDev = []
	k = [int(sys.argv[1])]
	testData = load('TwoDimHard.csv')
	trainData = load('TwoDimHard.csv')
	fig, ax = plt.subplots()
	for i in k:
		kMeans = km.Kmeans(trainData, testData, i)
		kMeans.train()
		kMeans.test()
		kMeans.results(kMeans.testData, False, True, False)
		probabilities(kMeans)
		stats(averages,stdDev,kMeans,k)
		sumSquare(kMeans)
		sumBetSquare(kMeans)
		for centroid in kMeans.centroids:
			print(centroid.x)
			print(centroid.y)
	averages = []
	stdDev = []
	'''
	k = 50
	for k in range(1,50,5):
		kMeans = km.Kmeans(trainData, testData, k)
		kMeans.train()
		probs = probabilities(kMeans)
		for i in range(len(kMeans.centroids)):#mutliplies probability of class through the (V|C)
			for key, value in kMeans.centroids[i].classFreq.items():
				kMeans.centroids[i].classFreq[key] = value*probs[key]
		kMeans.test()
		kMeans.results(kMeans.testData, False, True, True)
		probabilities(kMeans)
		stats(averages,stdDev,kMeans,k)
	'''
main()
