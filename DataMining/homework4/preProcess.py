
'''
	Author : Charles C. Stevenson
	Date : 04/11/2017
	Description:
		Exploratory analysis
		Classification analysis
'''

from exploration import Exploration
import pandas as pd


'''
	Pre-processing
==================================================================
'''
'''
	@Exploration
		params = dataframe
		Description:
			Does exploratory analysis on the data frame
'''
def dfExplore(df):
	explore = Exploration(df)
	explore.scatter()
	explore.classGraph()
'''
	@quality
		params = dataframe
	Reclassifies quality following the rule
		quality <= 5 -> class = "Low", quality > 5 -> class = "High"
'''
def quality(df):
	qual = df.loc[:,'quality']
	for i in range(len(qual)):
		if (df.loc[i,'quality'] <= 5):
			df.loc[i] = df.loc[i].replace(df.loc[i,'quality'], 0)
		else:
			df.loc[i] = df.loc[i].replace(df.loc[i,'quality'], 1)

'''
	@quality2
		params = dataframe
	Description:
		For some reason the quality output is a little screwed up.
'''
def quality2(df):
	qual = df.loc[:,'quality']
	for i in range(len(qual)):
		if (df.loc[i,'quality'] != 0 and df.loc[i,'quality'] != 1):
			df.loc[i] = df.loc[i].replace(df.loc[i,'quality'], 1)
'''
	@scale
		param: name
		    +Type = string
		@param: income
		    +Type = dataframe
	Description:
	    Scales the numerical values to values between 0 and 1
'''
def scale(name, df):
	#scales values down between 0 and 1
	attribute = df.loc[:,name]
	maximum = float(max(attribute))
	minimum = float(min(attribute))
	for i in range(len(attribute)):
		if (name != 'quality'):
			df.loc[i] = df.loc[i].replace(df.loc[i,name], (df.loc[i,name] - minimum)/(maximum - minimum))
'''
    @clean
        @param: df
            +Type = dataframe
    cleans data by dropping values, scaling, and discretizing the quality attribute.
'''
def clean(df):
	df.drop('ID', axis=1, inplace=True)
	df.drop('class', axis=1, inplace=True)
	quality(df)
	labels = list(df)
	labels.remove('quality')
	for label in labels:
		scale(label, df)
	quality2(df)
'''
	fxn : bayes
	params:
		df = pandas dataframe
	desciption: discretizes values into a high, medium and low values
'''
def bayes(df):
	labels = list(df)
	for label in labels:
		if (label != 'quality'):
			temp = list(df.loc[:,label])
			maximum = max(temp)
			minimum = min(temp)
			interval = ((maximum - minimum) / 6)
			for i in range(len(temp)):
				if (df.loc[i,label] < (minimum + interval)):
					df.loc[i,label] = 'a'
				elif (df.loc[i,label] > (minimum + interval) and df.loc[i,label] < (minimum + 2 * interval)):
					df.loc[i,label] = 'b'
				elif (df.loc[i,label] > (minimum + 2 * interval) and df.loc[i,label] < minimum + 3 * interval):
					df.loc[i,label] = 'c'
				elif (df.loc[i,label] > (minimum + 3 * interval) and df.loc[i,label] < minimum + 4 * interval):
					df.loc[i,label] = 'd'
				elif (df.loc[i,label] > (minimum + 4 * interval) and df.loc[i,label] < minimum + 5 * interval):
					df.loc[i,label] = 'e'
				else:
				#elif (df.loc[i,label] > (maximum + 5 * interval) and df.loc[i,label] < minimum + 6 * interval):
					df.loc[i,label] = 'f'
				
'''
==================================================================
'''
