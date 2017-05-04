
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
import os


def getSongs():
	os.system("ls -la ./songs/ | awk '{print $9}' >> temp.txt")
	
def csvfft(f):

	for line in f:
		try:
			M = 2205 #window size
			f_s = 100
			#initials	
			song = line[:-1] #song?
			print('Song = ' + str(song))
			rate, audio = wavfile.read(song) #read wav file
			audio = np.mean(audio, axis=1) #average all the values
			N = audio.shape[0] #grab mono channel

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
			df = pd.DataFrame(index = range(len(spectrum)), columns = freqs)
			print(len(freqs))
			print(len(spectrum))
			print(len(spectrum[0])/2)
			temp = spectrum
			for i in range(len(spectrum)):
				#print(float(i) / len(spectrum) * 100)
				temp = spectrum[i]
				#print('Spectrum size = ' + str(spectrum.size/2))
				#print(spectrum)
				temp = temp[:(temp.size/2)]
				df.loc[i] = temp
			df.to_csv(line[:-4] + 'csv')
			#freqs = np.fft.fftfreq(len(spectrum[300])) * f_s
			#freqs = fftpack.fftfreq(len(spectrum[200]))
			#for i in range(len(freqs)):
			#	freqs[i] = freqs[i] * 1000
			#for i in range(len(spectrum[30])):
			#	print(freqs[i])
			#plt.plot(np.abs(freqs), spectrum[250], 'r')
			#plt.show()
		except ValueError:
			pass

def main():
	#os.system("ls -la | awk '{print $9}' >> temp.txt")
	f = open('temp.txt', 'r')
	csvfft(f)
	f.close()
	#os.system('rm temp.txt')

main()
