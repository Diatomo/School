'''
Created on Mar 30, 2017

@author: michael
'''

import tensorflow as tf

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

with tf.Session() as sess:
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord)
    for i in range(15):
        # Retrieve a single instance:
        example, label = sess.run([m_lst,f_lst])

coord.request_stop()
coord.join(threads)