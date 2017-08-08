

# Artificial Intelligence --Homework 2
This assignment introduced me to the idea of unsupervised learning utilizing and algorithm called k-means. The program reads in a file with points (coordinates x & y) as well as a classifier of which centroid or group each point belongs to.

The algorithms initializes centroid randomly and then calculates all of its nearest neighbors. It then move according to the overall average of its containing points and then repeats until each centroid or center of each group moves no longer.

# To Run
  1) clone github repository
  2) python3 main.py
  
The output is an array of average number of times as k increases that it guesses a point correct on the test set. When k is low the prediction is low but so is the standard deviation. When k is high the prediction is much more accurate but the standard deviation also grows. 
