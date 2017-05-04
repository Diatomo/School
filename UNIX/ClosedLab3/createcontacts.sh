#!/bin/bash
#TITLE: createcontacts.sh
#AUTHOR: Charles Stevenson
#DATE: October 10, 2016
#DESCRIPTION : A script file that creates a contacts file

echo "
1. Enter a Contact
2. Show contacts
3. Exit
"
input=1

while [ "$input" != 3 ]
do
  read -p "Select an Option: " input
  if (("$input" == 1))
  then
    read -p "1. friend's full name: " name
    read -p "2. his/her birth date (dd-mm): " birth
    read -p "3. his/her phone number (xxx-yyy-yyyy): " phone
    read -p "4. his/her email (name@domain.xyz): " email
    echo "$name  $birth  $phone   $email" >> contacts
  elif (("$input" == 2))
  then
    cat contacts
  fi
done
