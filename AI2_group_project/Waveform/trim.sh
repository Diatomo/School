#!/bin/bash
#Trims all the .wav files within a specified DIRECTORY
#Adds files to a new directory called "trimmed"
#If no DIRECTORY given, defaults to local directory
mkdir trimmed
DIRECTORY=${1: -$PWD}
for f in $DIRECTORY*.wav
do
    sox $f temp.wav silence 1 0.1 1% reverse
    OUT="trimmed/trim_$f"
    sox temp.wav $OUT silence 1 0.1 1% reverse
    rm temp.wav
done
echo "DONE: Success"
