
# Advanced Artificial Intelligence -- Homework 1

This was a "Hello, World!" assignment for advanced artificial intelligence. The aim was to write a bayesian classifier for a data set that consisted of mushrooms. Variables were identifiers for characteristics of each mushroom collected. For example, l would be for mushrooms whose stalks were long and s were for mushrooms that had short stalks. Then at the end they would be classified as either 'p' for poisonous or 'e' for edible. 

A naive approach was implemented which basically suggest that each set of characteristics were independent from the rest. For example just because a mushroom has a long stalk doesn't mean it bruises when damaged. Therefore the data was read to calculate the prior probability for each characteristic in the data set and then weighed the likelihood (via the test set) of which hypothesis were to be true if the mushroom were poisonous 'p' compared to which mushrooms were edible 'e'. The one with a more likely hypothesis or rather a greater posterior was deemed the predicted type of mushroom (either 'p' or 'e').


# To Run:
  1) Clone git repository
  2) python3 mushroom.py
  
If it worked correctly the output is 99.9, meaning 99.9% of the data was predicted correctly.
