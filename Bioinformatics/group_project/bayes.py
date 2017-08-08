



'''
	Author = Charles Stevenson
	Date = 04/17/2017
	Description = bayes validation
'''


import pandas as pd
import BayesClassifier as bae




def process(df, rb1=False):
	temp = []
	patients = False
	for i in range(len(df)):
		try:
			if (rb1):
				if (not patients):
					if (df.loc[i]['RB1']):
						temp.append(df.loc[i]['!RB1'])
				else:
					if (df.loc[i]['RB1']):
						temp.append(int(df.loc[i]['number of patients']))
			else:
				if (not patients):
					if (df.loc[i]['!RB1']):
						temp.append(df.loc[i]['!RB1'])
				else:
					if (df.loc[i]['!RB1']):
						temp.append(int(df.loc[i]['number of patients']))
		except:
			pass
	return temp
			
def main():
	meta = 'df_OSU_LMS_METASTATIC.csv'
	osu = 'LMS_OSU_MUTATION.csv'
	tcga = 'LMS_TCGA_MUTATION.csv'

	netA = []
	netB = []
	df = pd.read_csv(meta)
	netA = process(df, rb1=True)
	netB = process(df)

	df = pd.read_csv(osu)
	b = bae.BayesClassifier()
	b.fit(netA, netB, df)
	print(b.attributes)
	
	df = pd.read_csv(tcga)
	b.predict(netA, netB, df)
	
	df = pd.read_csv(tcga)
	be = bae.BayesClassifier()
	be.fit(netA, netB, df)
	print(be.attributes)

	df = pd.read_csv(osu)
	be.predict(netA, netB, df)

	


main()
