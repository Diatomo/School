



import Statistics
import numpy as np
import pandas as pd
import operator
import copy


def writeToFile(df,s):
	subs = ['COCAINE_REF', 'ETHANOL_REF', 'HEROINE_REF', 'METHAMPHETAMINE_REF', 'MORPHINE_REF', 'NICOTINE_REF']
	for i in range(len(s.pValues)):
		f = open(subs[i], 'w+')
		for j in range(len(s.pValues[i])):
			if (s.pValues[i][j] < .001/46000): #and s.pValues[i][j] > 0.000001):
				f.write(str(j) + '\n')
		f.close()

def writeToFile2(df,s):
	subs = ['COCAINE', 'ETHANOL', 'HEROINE', 'METHAMPHETAMINE', 'MORPHINE', 'NICOTINE']
	for i in range(len(s.pValues)):
		f = open(subs[i], 'w+')
		for j in range(len(s.pValues[i])):
			if (s.pValues[i][j] < .001/46000): #and s.pValues[i][j] > 0.000001):
				f.write(df['geneID'][j] + '\n')
		f.close()
'''
def cleanLabels(df):
	labels = list(df)
	labels.remove('geneID')
	remov = []
	for label in labels:
		delete = True
		for i in label:
			if (i == '1' or i == '8'):
				delete = False
		if (delete == True):
			remov.append(label)
	for i in remov:
		 labels.remove(i)
	labels = labels[:-24]#cutout controls
	return labels
'''

def sort(results, df):
	sg = []
	tempSG = []
	acc = 0
	for i in range(len(results)):
		for j in range(len(results)):
			sg.append('geneID')
	
	c = 'COCAINE'
	h = 'HEROINE'
	m = 'METHAMPHETAMINE'
	a = 'ETHANOL'
	mo = 'MORPHINE'
	n = 'NICOTINE'
	features = [c,a,h,m,mo,n]
	tempRes = []
	for i in range(len(results[0])):
		tempRes.append(results[0][i])
		sg.append(df['geneID'][i])

	for i in range(200):
		max_index, max_value = max(enumerate(tempRes), key=operator.itemgetter(1))
		tempSG.append(sg[max_index])
		del tempRes[max_index]
		del sg[max_index]

	f = open('FEATURES','r')
	for line in f:
		line = line[:-1]
		correct = False
		for i in tempSG:
			if (line == i):
				correct = True
		if (correct):
			acc += 1.0

	
	#print('ACCURACY = ' + str(acc))
				
def test(df, stats):
	results = np.empty([6, len(df)])
	for i in range(6):
		results[i] = abs(stats.avgs[i][0] - stats.avgs[i][3])
	#print(results)
	return results

def generateFeatures():
	c = 'COCAINE_REF'
	h = 'HEROINE_REF'
	m = 'METHAMPHETAMINE_REF'
	a = 'ETHANOL_REF'
	mo = 'MORPHINE_REF'
	n = 'NICOTINE_REF'
	features = [c,h,m,a,mo,n]
	temp = set()
	for i in features:
		f = open(i, 'r')
		for line in f:
			line = line[:-1]
			if (line not in temp):
				temp.add(line)
		f.close()

	f = open('FEATURES_REF', 'w+')
	for i in temp:
		f.write(i + '\n')
	f.close()

def generateFeatures2():
	c = 'COCAINE'
	h = 'HEROINE'
	m = 'METHAMPHETAMINE'
	a = 'ETHANOL'
	mo = 'MORPHINE'
	n = 'NICOTINE'
	features = [c,h,m,a,mo,n]
	temp = set()
	for i in features:
		f = open(i, 'r')
		for line in f:
			line = line[:-1]
			if (line not in temp):
				temp.add(line)
		f.close()

	f = open('FEATURES', 'w+')
	for i in temp:
		f.write(i + '\n')
	f.close()

def writeFeatures(df):
	f = open('FEATURES_REF', 'r')
	fn = open('FEATURES', 'w+')
	for line in f:
		line = line[:-1]
		line = int(line)
		fn.write(df['geneID'][line] + '\n')
			
def main():

	fn = 'MiceAddictionExpressionProfile.csv'
	df = pd.read_csv(fn)
	s = Statistics.Statistics(df)
	print("AVERAGES")
	print(s.avgs)
	print("Standard Deviations")
	print(s.stds)
	print("t-Values")
	print(s.tValues)
	print("p-Values")
	print(s.pValues)
	#test(df,s)
	#sigGenes, Nums = sort(test(df,s), df)
	#print(Nums)
	#print(sigGenes)
	#s.Output()
	writeToFile(df,s)
	writeToFile2(df,s)
	generateFeatures()
	generateFeatures2()
	writeFeatures(df)
	sort(test(df,s), df)


if __name__ == "__main__":
	main()
