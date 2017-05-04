
'''
	Author: Charles C. Stevenson =^.^= Diatomo
	Date: 04/12/2017
	Description:
		a youtube-dl script for a songlist.txt file.
		the file consist of : '<name>  <url>'
		
		***
			This Script is Being
			used for a group_project
			in Artificial Intelligence 2

			youtube-dl requires a dependency: Please Download to successfuly 
			download and extract audio in mp3 files.
			
			if Ubuntu 16.04:
				sudo apt-get install -y libav-tools
			else:
				check online sources (youtube-dl) avprobe or ffprobe
		***
'''

import os
import sys
import subprocess
import re
import time
'''
	fxn : download
	params:
		line = String
	Description:
		Captures name of file downloaded from youtube-dl
		Moves it into folder <song> and renames it according
		to the name in the file <songlist.txt>
'''
def download(line):
	name = line[0]
	url = line[1]

	#bash commands and string manipulation
	os.system('find ./ -printf "%f\n" > logB')#captures directory before file is downloaded
	os.system('youtube-dl --extract-audio --audio-format mp3 {}'.format(url))
	os.system('find ./ -printf "%f\n" > logA')#captures directory after file is downloaded
	output = subprocess.check_output('diff logB logA | tail -1 | cut --complement -c1-2', shell=True)
	
	#string processing
	output = output[:-1]
	output = re.escape(output)
	name = re.escape(name)
	print('NAME: ' + name)
	ext = '.mp3'
	output = output.decode('utf8', 'replace')

	#converting to wav and moving them into separate directory	
	os.system('mv {} {}{}'.format(output,name,ext))
	os.system('sudo mpg123 -w {}{} {}{}'.format(name,'.wav',name,'.mp3'))
	os.system('mv {}{} ./songs/{}{}'.format(name,'.wav',name,'.wav'))
	os.system('rm {}{}'.format(name,'.mp3'))

'''
	fxn : processFile
	params:
		f = file
	Description:
		creates two log files <logA> && <logB> which are used to get the newest added
		file to the directory and reads through the file <f> to download
		and process mp3s.
'''
def processFile(f):
	os.system('touch logA')
	os.system('touch logB')
	try:
		os.system('mkdir songs')
	except:
		pass
	for line in f:
		line = line[:-1]
		line = re.split('\t', line)
		line = list(filter(('').__ne__, line))
		line = list(filter(('\t').__ne__,line))
		print("LINE = " + str(line))
		download(line)
	os.system('rm logA')
	os.system('rm logB')
'''
	fxn : main
	params:
		No formal parameters in function signature, 
		but requires an input text file.
	Description:
		Checks input file and then processes the file
		to download and process files from youtube
'''		
def main():
	try : 
		f = open(sys.argv[1], 'r')
	except IndexError:
		print("Requires Input file 'songList.txt'")
		sys.exit(1)

	processFile(f)
	f.close()
	print("Downloads Complete!!")

if __name__ == "__main__":
	main()

