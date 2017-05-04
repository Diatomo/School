
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
#import pandas as pd
import csv
import os


def getSongs():
	os.system("ls -la ./songs/ | awk '{print $9}' >> temp.txt")



def simulatedData(song):
	fre = range(10,500,10)
	f_s = 100
	
	for f in fre:
		t = np.linspace(0,50, 50 * f_s, endpoint = False)
		x = np.sin(f*2*np.pi*t)

		plt.plot(t,x)
		plt.xlabel('Time[s]')
		plt.ylabel('Signal amplitude')
		plt.show()

		X = np.fft.fft(x)
		freqs = fftpack.fftfreq(len(X) * f_s)
		plt.stem(freqs, np.abs(X))
		plt.xlabel('Hertz')
		plt.ylabel('Frequency Domain')
		plt.show()
	


	
def csvfft(song):

	#initials	
	rate, audio = wavfile.read(song) #read wav file
	audio = np.mean(audio, axis=1) #average all the values
	N = audio.shape[0] #grab mono channel
	print(audio[0])
	print(audio[1])
	print(audio[2])
	print(audio[3])
	'''
	slices = util.view_as_windows(audio, window_shape=(M,), step = 2205) #get slices
	win = np.hanning(M+1)[:-1]
	slices = slices * win
	slices = slices.T #organize into columns
	spectrum = np.fft.fft(slices, axis=0) #do fft of audio
	spectrum = np.abs(spectrum)
	freqs = fftpack.fftfreq(len(spectrum[0]))
	for i in range(len(freqs)):
		freqs[i] = freqs[i] * 1000
	freqs = freqs[:len(freqs)/2]
	#df = pd.DataFrame(index = range(len(spectrum)), columns = freqs)
	print(len(freqs))
	print(len(spectrum))
	print(len(spectrum[0])/2)
	idx = np.argmax(spectrum)
	temp = spectrum
	song = song[:-4]
	for i in range(len(spectrum)):
		#print(float(i) / len(spectrum) * 100)
		temp = spectrum[i]
		#print('Spectrum size = ' + str(spectrum.size/2))
		#print(spectrum)
		print('plotting')
		temp = temp[:len(temp)/2]
		print(len(spectrum))
		print(len(freqs))
		plt.plot(freqs, temp, 'r')
		plt.title('Fast Fourier Transform')
		plt.xlabel('Frequency (Hertz)')
		plt.ylabel('Intensity')
		plt.show()
	#df.loc[i] = temp
	#df.to_csv(line[:-4] + 'csv')
	'''

def main():
	
	song = 'trim_AlbenizI-Tango.wav'
	simulatedData(song)
#	rate, data = wavfile.read(song)
#	data_bis = np.fft.ifft(np.fft.fft(data))
#	data_bis = data_bis.astype('int16')
#	wavfile.write('IFFT.wav', rate, data_bis)
	
main()
