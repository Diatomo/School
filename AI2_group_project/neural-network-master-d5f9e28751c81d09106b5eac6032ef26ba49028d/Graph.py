'''
Created on Mar 24, 2017

@author: michael
'''

from __future__ import print_function

# Import MNIST data

import tensorflow as tf
import numpy as np

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

def get_data():
    midi_queue = tf.train.string_input_producer(["midi.csv"])
    fft_queue = tf.train.string_input_producer(["fft.csv"])
    m_reader = tf.TextLineReader()
    m_key, m_value = m_reader.read(midi_queue)
    f_reader = tf.TextLineReader()
    f_key, f_value = f_reader.read(fft_queue)
    m_def = [[] for _ in xrange(127)]
    f_def = [[] for _ in xrange(2205)]
    m_lst = tf.decode_csv(m_value, record_defaults=m_def)
    f_lst = tf.decode_csv(f_value, record_defaults=f_def)
    features = tf.stack(m_lst)
    labels = tf.stack(f_lst)
    print("loading "+ str(features)+ "line(s)\n")
    print("loading "+ str(labels)+ "line(s)\n")
    return labels, features


learning_rate = 0.001
training_epochs = 50
batch_size = 100
display_step = 1

n_hidden_1 = 1000 # 1st layer number of features
n_hidden_2 = 1000 # 2nd layer number of features
n_input = 2205 # MNIST data input (#FFT classes per sample)
n_classes = 127 # Keys on the piano

x = tf.placeholder("float", shape=[None, n_input])
y = tf.placeholder("float", shape=[None, n_classes])

m_lst, f_lst = get_data()
print (tf.shape(m_lst))

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

# Launch the graph
with tf.Session() as sess:
    sess.run(init)
    
    # Training cycle
    for epoch in range(50):
        avg_cost = 0.
        for i in range(15):
            _, c = sess.run([optimizer, cost], feed_dict={x:f_lst.eval(), y:m_lst.eval()})
            avg_cost += c / 15
        
        # Display logs per epoch step
        if epoch % display_step == 0:
            print("Epoch:", '%04d' % (epoch+1), "cost=", \
                  "{:.9f}".format(avg_cost))
                
    print("Optimization Finished!")

    # Test model
    correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
    # Calculate accuracy
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    print("Accuracy:", accuracy.eval({x: f_lst, y: m_lst}))
