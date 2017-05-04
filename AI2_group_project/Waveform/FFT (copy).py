
'''
	Author: Charles C. Stevenson
	Date: 3/26/2017
	Description: Performs an FFT on a sound file
'''

import matplotlib.pyplot as plt
from scipy.io import wavfile
import wave
from scipy import fftpack
import numpy as np
from skimage import util
import pandas as pd



def xpSample():

	song = 'AlbenizI-Tango.wav'
	rate, audio = wavfile.read(song)
	audio = np.mean(audio, axis=1)
	N = audio.shape[0]
	M = 2205
	slices = util.view_as_windows(audio, window_shape=(M,), step = 2205)
	win = np.hanning(M+1)[:-1]
	slices = slices * win
	slices = slices.T
	spectrum = np.fft.fft(slices, axis=0)
	spectrum = np.abs(spectrum)
	#spectrum = 20 * np.log10(spectrum / spectrum.max())
	f_s = 100
	freqs = np.fft.fftfreq(len(spectrum[300])) * f_s
	L = N / rate
	print('Audio Length: {:.2f} seconds'.format(L))
	print(len(audio))
	#print(slices.shape)
	#fig, ax = plt.subplots()
	#print(len(spectrum))
	#print(len(spectrum[300]))
	#print(spectrum)
	#spectrum = np.fft.fft(spectrum)
	#spectrum = np.abs(spectrum)
	#print(spectrum[i])
	freqs = fftpack.fftfreq(len(spectrum[200]))
	print(len(freqs))
	print(len(spectrum))
	print(len(spectrum[0]))
	for i in range(len(freqs)):
		freqs[i] = freqs[i] * 1000
	for i in range(len(spectrum[30])):
		print(freqs[i])
	plt.plot(np.abs(freqs), spectrum[250], 'r')
	#plt.plot(np.abs(spectrum[300]),freqs, 'r')
	#plt.show()
	#ax.plot(freqs, np.abs(spectrum[1]), 'r')
	plt.show()

	
	
	'''
	fig, ax = plt.subplots()
	t = np.linspace(0,2,2*f_s, endpoint=False)
	x = np.sin(f * 2 * np.pi * t)
	ax.plot(t,x)
	ax.set_xlabel('Time (s)')
	ax.set_ylabel('Signal amplitude')
	#plt.show()

	X = fftpack.fft(x)
	freqs = fftpack.fftfreq(len(x)) * f_s
	fig, ax = plt.subplots()
	ax.plot(freqs,np.abs(X))
	ax.set_xlabel('Frequency in Hertz')
	ax.set_ylabel('Frequency Domain')
	ax.set_xlim(-f_s / 2, f_s /2)
	ax.set_ylim(-5, 110)
	plt.show()
	'''


def main():
	
	
	rate, audio = wavfile.read('AlbenizI-Tango.wav')
	audio = np.mean(audio, axis=1)
	N = audio.shape[0]
	L = N / rate
	
	print('Audio Length: {:.2f} seconds'.format(L))

	f, ax = plt.subplots()
	ax.plot(np.arange(N) / rate, audio)
	ax.set_xlabel('Time [s]')
	ax.set_ylabel('Amplitude [unknown]')
	plt.show()
	xpSample()

	'''
	M = 1024

	slices = util.view_as_windows(audio, window_shape=(M,), step=100)
	print('Audio shape: {}, Sliced audio shape: {}'.format(audio.shape, slices.shape))
	'''

main()
