

'''
	Author: Charles C. Stevenson
	Date : 04/11/2017
	Description: 
		Data exploration file to make graphs of the wine.csv
'''

import matplotlib.pyplot as py
import scipy
import numpy as np
import pandas as pd

class Exploration:

	def __init__(self, df):
		self.df = df

	def hist(self, x, y):
		return 0

	'''
	correlation coefficient:
		params : x = df.ix[,label]
			 y = df.ix[,label]
	'''
	def correlation(self, x, y):
		labelA = list(x)
		labelB = list(y)
		coeff = np.corrcoef(labelA, labelB)
		return coeff[0][1]
	
	def classGraph(self):
		labels = list(self.df)
		classes = list(self.df.ix[:,'class'])
		temp = []
		counter = 0
		for cls in classes:
			if (cls == 'Low'):
				temp.append(0)
			else:
				temp.append(1)
		labels = labels[1:-1]
		for label in labels:
			py.figure(counter)
			py.scatter(temp, self.df.ix[:,label])
			py.xlabel('Class')
			py.ylabel(label)
			counter += 1
		print('class')
		py.show()
	
	def scatter(self):
		labels = list(self.df)
		labels = labels[1:-1]
		counter = 0
		for labelA in labels:
			for labelB in labels:
				if (labelA != labelB):
					corr = self.correlation(self.df.ix[:,labelA], self.df.ix[:,labelB])
					if (corr > 0.6):
						py.figure(counter)
						py.scatter(self.df.ix[:,labelA], self.df.ix[:,labelB])
						py.xlabel(labelA)
						py.ylabel(labelB)
						counter += 1
		py.show() 

	
		
		
		
