
'''
	Author ::= Charles Stevenson
	Date ::= 4/20/2017
	Description ::=
		This script takes the data set of mice exposed to addictive substances
		and extracts a dataframe of the most significant gene changes when exposed 
		to substances.
'''

import pandas as pd
import numpy as np
import scipy.stats as sp



'''
	stats Data Structure

		 1hr		2hr		4hr		8hr
cocaine[[avg		avg		avg		avg]
heroine [avg		avg		avg		avg]
metham. [avg		avg		avg		avg]
.		 ...		...		...		...
.		 ... 		...		...		...
.		 ...		...		...		...]
'''

NTIME = 4  #This is a variable the <Number of TIMEs> the sample is taken
SUBSTANCES = 6 #number of substances
CONTROL = 2 #number of controls

class Statistics():

	def __init__(self,df):
		self.df = df
		self.avgs = self.__initAverages(df)
		self.stds = self.__initStd(self.avgs, df)
		self.tValues = self.tTest()
		self.pValues = self.generatepValues()


	def tTest(self):
		std = self.stds
		avg = self.avgs
		length = len(avg[0][0])
		avgTemp = np.empty([1, length])
		stdTopTemp = np.empty([1, length])
		stdBotTemp = np.empty([1, length])
		tValues = np.empty([SUBSTANCES, length])
		for i in range(SUBSTANCES):
			for j in range(NTIME):
				avgTemp += avg[i][j] - avg[7][j]
				stdTopTemp += ((std[i][j]**2 / len(std[i][j])))
				stdBotTemp += ((std[7][j]**2 / len(std[i][j])))
			
			avgTemp = avgTemp/NTIME
			stdTemp = np.sqrt(stdTopTemp/NTIME + stdBotTemp/NTIME)
			tValues[i] = avgTemp / stdTemp

		return tValues

	def generatepValues(self):
		pValues = np.empty([6, len(self.tValues[0])])
		for i in range(len(self.tValues)):
			pValues[i] = sp.t.sf(np.abs(self.tValues[i]), len(self.tValues[0]))
			#pValues = sp.t.sf(np.abs(self.tValues[0]), 3)
		return pValues

	def Output(self):
		subs = ['COCAINE', 'ETHANOL', 'HEROINE', 'METHAMPHETAMINE', 'MORPHINE', 'NICOTINE']
		print(len(self.pValues))
		for i in range(len(self.pValues)):
			print(subs[i])
			for j in range(len(self.pValues[i])):
				if (self.pValues[i][j] < .000015): #and self.pValues[i][j] > 0.00001):
					print("i = %d && pValue = %f" % (j, self.pValues[i][j]))

	def __initAverages(self, df):
		labels = list(df)							#list of labels
		labels.remove('geneID')						#remove insignificant labels
		substances = labels[:73]				
		controls = labels[73:]		
		cohorts = self.__buildAverages(substances, controls, df)
		return cohorts	
	
	def __buildAverages(self, substances, controls , df):
		sSize = 3
		cSize = 6
		nSubs = (len(substances) / ((sSize * NTIME)))		
		nSubs += 2
		cohorts = np.empty([int(nSubs), NTIME, len(df)])			
		tCounter = 0							
		sCounter = 0
		timeCounter = 0
		labels = [substances, controls]							
		temp = []
		for i in range(len(labels)):
			if (i == 0):
				tSize = sSize #how many mice are in a time sample
			else:
				tSize = cSize #how many mice are in a time sample
			avg = np.empty([len(df), tSize])
			for label in labels[i]:
				if (tCounter % tSize  == 0 and tCounter != 0):
					cohorts[sCounter][timeCounter] = avg.mean(axis=1)
					avg = np.empty([len(df), tSize])
					timeCounter += 1
					if (timeCounter % NTIME == 0 and timeCounter != 0):
						sCounter += 1
						timeCounter = 0
					tCounter = 0
					temp = []
				else:
					avg[:,tCounter] = df[label]
					tCounter += 1
					temp.append(avg)
					
		return cohorts


	def __initStd(self,avgs, df):
		labels = list(df)							
		labels.remove('geneID')						
		substances = labels[:73]				
		controls = labels[73:]		
		std = np.empty([8, NTIME, len(df)])	
		temp = []
		subs = 0
		time = 0
		for i in range(0, len(substances)-3, 3):
			mouseA = df[substances[i]]
			mouseB = df[substances[i+1]]
			mouseC = df[substances[i+2]]
			tempAvgs = avgs[subs][time]
			temp.append((((mouseA - tempAvgs + mouseB - tempAvgs + mouseC - tempAvgs)**2)**0.5))
			time += 1
			if (time % NTIME == 0 and time != 0):
				std[subs] = temp
				temp = []
				time = 0
				subs += 1
		return std		
