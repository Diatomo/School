# DataMining --Significant changes in gene transcription in mice given addictive substances.

This assignment was an attempt to apply a t-test to expression profiles found in mouse brain tissue over time when given addictivesubstances, such as Heroine, Cocaine, etc... We ended up hitting a huge problem with the standard t-test and that was the t-test relies on the a normal distribution, a gaussian. However; genes do not express in DNA under a guassian curve. Some genes are expressed more than others, such as house keeping genes, while others vary depending on the state of the organism, things such as stress, sex, age, or their diet can differ. Therefore, to employ a t-test another method needs to be chosen.

# Dependencies:
	python3 pandas
	python3 numpy
	Custom Statistic.py need to be in the same directory as main.py

# To Run:
	python3 main.py


The output will be a series of matrices
First Matrix = Averages
Second Matrix = Standard Deviations
Third Matrix = T-Scores
Fourth Matrix = p-Values
