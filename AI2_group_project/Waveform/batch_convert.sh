#!/bin/bash
for song in $( ls $1 ); do
	ffmpeg -i ${1}/$song ${2}/${song:0:${#song} - 4}.wav
done
