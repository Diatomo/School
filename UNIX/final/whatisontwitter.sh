#!/bin/bash


Turl=$(<.url) #grab url
#
#
#   MENU
#
#
  echo
  echo
  cat .title
  sleep 2
while [[ $input != 0 ]];
do
  echo
  echo "1. Would you like to continue with the current url: " `cat .url`
  echo "2. Choose another url"
  echo "3. Add word to excludedwords"
  echo "4. Analyze Text"
  echo "0. Exit"
  read -p "Select an Option: " input

  if [[ $input == 2 ]];#grab new url
  then
    read -p "Enter in a twitter url" Turl
    echo $Turl > .url
  fi

  echo
  echo
#
#
# Create Log File
#
#
if [[ $input == 1 || $input == 2 ]]
then
    currentDate="$(echo `date` | awk '{ print $1_$2_$3 }')"
    time="$(echo `date` | awk '{ print $4 }')"
    size="$(ls -la | grep twitter.html | awk '{print $5}')"
    echo `date`  "     "    $Turl      "          twitter.html" "                                 ${size}" >> .logfile

  #
  #
  #  HTML generation && Message Extraction
  #
  #
    wget -O twitter.html $Turl

    sed -n '/<p class="TweetTextSize  js-tweet-text tweet-text" lang="en" data-aria-label-part="0">.*<\/p>/{s/<[^>]*>//g;p}' twitter.html > messages.txt #cleanup html
    sed 's/[@#&]//g' messages.txt > test.txt #cleanup undesirable characters
    sed 's/quot//g' test.txt > messages.txt
    sed 's/http.*//g' messages.txt > test.txt
    sed 's/39//g' test.txt > messages.txt
    sed 's/pic.*//g' messages.txt > test.txt
    sed -e 's/^[ \t]*//' test.txt > messages.txt #clears whitespace
    cat test.txt > messages.txt

  #
  #
  #  Generate Message Log File
  #
  #
  header="$(cat twitter.html | grep StreamsHero-header | sed 's/<h2 class="StreamsHero-header">//g' | sed 's/<.*//g' | sed 's/^[ \t&]*//g' | sed 's/amp//g')"
    echo "$header" > log.txt #grabs header file
    echo "$currentDate" >> log.txt
    echo "Messages" >> log.txt
    echo "------------------------------------------" >> log.txt

    file="messages.txt"
    counter=1
    while IFS= read -r line
    do
      echo "$counter)$line" >> log.txt
      counter=$((counter+1))
    done<"$file"

    cat messages.txt | (tr ' ' '\n' | sort | uniq -c | awk '{print $2"@"$1}') > temp2.txt #print numbers
    for word in $(<.excludedwords); do sed -i '/'$word'/d' temp2.txt; done
    sort -t"@" -k2,2 -nr temp2.txt | sed '1d' | sed '21,/$d/d' > temp3.txt #sort and trim numbers
    awk -F'@' '{ print $2 }' temp3.txt > numbers.txt
    total=$(awk 'BEGIN{ total=0 } {total=total+$1 } END { printf total}' numbers.txt)
    awk -v total=$total '{print $1/total*100}' numbers.txt > percentages.txt
    sed 's/^/@/' percentages.txt > percentTemp.txt
    paste temp3.txt percentTemp.txt > pasted.txt
    END=20
    for ((i=1;i<=END;i++)); do
      echo "$i@ " >> wordsT.txt
    done
    paste wordsT.txt pasted.txt > pasted2.txt
    echo "Number@Top-words@frequency@Pecentage" > wordsT3.txt
    echo "----------@----------@---------@-----------'" >> wordsT3.txt
    #column -s"@" -t wordsT2.txt > words.txt
    cat pasted2.txt >> wordsT3.txt
    column -s"@" -t  wordsT3.txt >> words.txt


    rm test.txt
    rm numbers.txt
    rm percentages.txt
    rm wordsT.txt
    rm wordsT3.txt
    rm temp3.txt
    rm temp2.txt
    rm percentTemp.txt
    rm pasted.txt
    rm pasted2.txt
    rm twitter.html

    mkdir -p $currentDate
    mkdir -p $time
    mkdir -p current
    cp ./*.txt ./$time
    mv ./*.txt ./current
    mv ./$time ./$currentDate
fi

#
#
#  Text Analysis
#
#
if [[ $input == 3 ]]
then
  read -p "Which word would you like to exclude: " word
  echo $word >> .excludedwords
fi

if [[ $input == 4 ]]
then
  echo
  echo "1. Summary"
  echo "2. Word Summary"
  echo "3. Exit"
  read -p "Select an Option: " input
  if [[ $input == 1 ]]
  then
    sed '3,8!d' current/words.txt | awk '{print $1}' > temp.txt
    for word in $(<temp.txt); do grep $word ./current/messages.txt; done
    rm temp.txt
  fi
  if [[ $input == 2 ]]
  then
    echo "Which word would you like to analyze?"
    cat ./current/words.txt
    read -p "Select a Number: " input
    input=$((input+2))
    word="$(sed -n "$input,$input"p ./current/words.txt | awk '{print $2}')"
    grep -R $word ./ > temp.txt
    head -10 temp.txt
    rm temp.txt
  fi
fi
done
rm -r current
echo "BYE!"
exit

