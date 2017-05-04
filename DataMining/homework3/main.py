
'''
	Author : Charles C. Stevenson
	Date : 04/11/2017
	Description:
		Exploratory analysis
		Classification analysis
		of the wine.csv dataset.
'''

import pandas as pd
import preProcess as pp
import classification as clf
import featureSelection as fs 
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

'''
	fxn : createX
	params:
		df = dataframe (pandas dataframe)
	Description:
		Creates the X vector, which is a two
		dimensional array containing all the rows and
		thier attributes
'''
def createX(df):
	x = []
	for i in range(len(df)):
		sample = list(df.loc[i])
		sample.remove(sample[-1])
		x.append(sample)
	return x
'''
	fxn : createY
	params:
		df = dataframe (pandas dataframe)
	Description:
		Creates the Y vector, which is an one
		dimensional array containing the classes
		of each row.
'''
def createY(df):
	y = []
	for i in range(len(df)):
		sample = list(df.loc[i])
		sample = sample.pop()
		y.append(sample)
	return y
'''
	fxn : confMatrixOutput
	params:
		classifier = a string of the name of the classifier
		results = a confusion matrix dictionary see fxn crossValidation in classification.py
'''
def confMatrixOutput(classifier, results):
	print('\n' + str(classifier) + ':')
	print("Accuracy of " + str(classifier) + ' is ' + str(results['accuracy']))
	print("TPR of " + str(classifier) + ' is ' + str(results['TPR']))
	print("FPR of " + str(classifier) + ' is ' + str(results['FPR']))
	print("precision of " + str(classifier) + ' is ' + str(results['precision']))
	print("recall of " + str(classifier) + ' is ' + str(results['recall']))
	print("f-measure of " + str(classifier) + ' is ' + str(results['f-measure']))
	print('\n')

def main():
	df = pd.read_csv('wine.csv')
	#pp.dfExplore(df) #exploration function for paper analysis
	pp.clean(df) #Normalizes data
	#df.drop('resid_sugar', axis = 1, inplace=True)
	#df.drop('free_sulf_d', axis = 1, inplace=True)
	#df.drop('citric_acid', axis = 1, inplace=True)
	#df.drop('density', axis = 1, inplace=True)
	#df.drop('fx_acidity', axis = 1, inplace=True)
	x = createX(df)
	y = createY(df)
	
	#Feature selection
	temp = list(df)
	print(temp)
	fs.recursiveFeatureElimination(x,y)
	fs.featureImportance(x,y)

	#classifiers
	results = clf.decisionTree(x, y)
	confMatrixOutput('Decision Tree', results)
	results = clf.supportVectorMachine(x,y)
	confMatrixOutput('Support Vector Machine', results)
	results = clf.ANN(x,y)
	confMatrixOutput('Artificial Neural Network', results)
	results = clf.randomForest(x,y)
	confMatrixOutput('Random Forest', results)
	results = clf.rulesBased(x,y)
	confMatrixOutput('Rules Based Classifier', results)
	
	pp.bayes(df) # discretizes all the data to low, medium, and high.
	x = createX(df)
	y = createY(df)
	results = clf.bayesClassifier(x,y)
	confMatrixOutput('Naive Bayesian Classifier', results)
	#df.to_csv('bayes.csv')

main()

