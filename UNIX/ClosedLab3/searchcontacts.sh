#!/bin/bash
#TITLE: searchcontacts.sh
#AUTHOR: Charles Stevenson
#DATE: October 10, 2016
#DESCRIPTION : A script file that searches and sorts a contact list

fName=$1 #first name
lName=$2 #last name

#Intro itemsi
num=$(wc -l contacts)
echo "Hello, $fName $lName!"
echo "Today is `date +"%A"` and the current time is `date +"%r"`"
echo "These contacts are having a birthday today: "

grep `date +"%d-%m"` contacts

found=false
while [ "$found" == false ]
do
  read -p "What is the last name of a friend? " friendLastName
  if (grep -q "$friendLastName" contacts)
  then
      found=true
      grep "$friendLastName" contacts
  fi
  if [ "$found" == false ]
  then
    echo "Number of lines: $num"
    sort contacts
  fi
done
echo "GOODBYE `date +"%H"` "
