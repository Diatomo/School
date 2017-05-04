'''
Created on Apr 1, 2017

@author: michael
'''

import tensorflow as tf
import csv
import numpy as np
import pandas as pd

def multilayer_perceptron(x, weights, biases):
    # Hidden layer with RELU activation
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    layer_1 = tf.nn.relu(layer_1)
    # Hidden layer with RELU activation
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    layer_2 = tf.nn.relu(layer_2)
    # Output layer with linear activation
    out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
    return out_layer

def load_csv(filename):
	with open(filename, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar=None)
		rows = []
		for row in spamreader:
			floaty = [float(i) for i in row]
			rows.append(floaty)  
		return rows

def load_pdcsv(filename):
		df = pd.read_csv(filename)
		rows = []
		for i in range(len(df)):
			temp = df.loc[i]
			floaty = [float(j) for j in temp]
			rows.append(floaty)
		return rows
				
learning_rate = 0.001
training_epochs = 50
batch_size = 100
display_step = 1

n_hidden_1 = 850 # 1st layer number of features
n_hidden_2 = 850 # 2nd layer number of features
n_input = 1758 # MNIST data input (#FFT classes per sample)
n_classes = 127 # Keys on the piano

x = tf.placeholder("float", shape=[None, n_input])
y = tf.placeholder("float", shape=[None, n_classes])

weights = {
    'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
    'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_hidden_2, n_classes])) }

biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'b2': tf.Variable(tf.random_normal([n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_classes])) }

pred = multilayer_perceptron(x, weights, biases)
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)
init = tf.global_variables_initializer()

ffts = load_pdcsv('fft2Real.csv')
print('fft complete')
midis = load_csv('albe.csv')
print('midi_complete')

with tf.Session() as sess:
    sess.run(init)
    
    # Training cycle
    for epoch in range(50):
        avg_cost = 0.
        for i in range(1758):
            _, c = sess.run([optimizer, cost], feed_dict={x:ffts, y:midis})
            avg_cost += c / 1758
        
        # Display logs per epoch step
        if epoch % display_step == 0:
            print("Epoch:", '%04d' % (epoch+1), "cost=", \
                  "{:.9f}".format(avg_cost))
                
    print("Optimization Finished!")

    # Test model
    correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
    # Calculate accuracy
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    print("Accuracy:", accuracy.eval({x: ffts, y: midis}))
