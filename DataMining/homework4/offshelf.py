
import preProcess as pp
import numpy as np
from sklearn.cluster import KMeans
import pandas as pd


def load(fileName):
	x,y,classifier = [], [], []
	df = pd.read_csv(fileName)
	pp.clean(df)
	for i in range(len(df)):
				x.append(float(df.loc[i][0])**3 + float(df.loc[i][1]) + float(df.loc[i][2])**2 + float(df.loc[i][8])**2)
				y.append(float(df.loc[i][3]) + float(df.loc[i][4])**2 + float(df.loc[i][5]) + float(df.loc[i][6])**2 + float(df.loc[i][7]) + float(df.loc[i][9])**2 + float(df.loc[i][10]))
				classifier.append(int(df.loc[i][11]))
	features = np.empty([len(x),2])
	for i in range(len(x)):
		features[i] = [x[i],y[i]]
	return features

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
	features = load('wine.csv')
	kmeans = KMeans(n_clusters=2, random_state=0).fit(features)
	print(kmeans.cluster_centers_)
	


main()		
