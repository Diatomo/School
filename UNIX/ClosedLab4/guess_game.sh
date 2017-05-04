#!/bin/tcsh -f

clear
set decision=4
touch records
while ( $decision != 1 && $decision != 2 )
  echo "1. Run the guessing game"
  echo "2. Exit"
  set decision=$<
  if ( $decision == 1 ) then
    echo "\nguess the number" #output
    set answer=$< #set answer to input
    set goal=`tr -dc A-Za-z0-9 < /dev/urandom | od -d | head -c 10 | tr -d 0 | tr -d ' '` #set goal to random number
    set count=1 #counter
    while ( $answer != $goal ) #while the answer is not the randomly generated number
      if ( $answer < $goal ) then #if the answer is less than the goal
        echo "too small"
      else
        echo "too large" #if the answer if is larger than the goal
      endif
      @ count ++ #increment counter
      set answer = $< # get the next guess
    end
  echo "correct!"  #output correct
  echo "$count" >> records
  echo "using $count rounds" #How many guesses did you try?
  set decision=4
  endif
end

if ( $decision == 2) then
  @ sum=0
  @ itr=0
  foreach line (` cat records `)
    @ sum=`expr $sum + $line`
    @ itr ++
  end
  echo "Exiting the guessing game"
  @ sum = `expr $sum / $itr`
  echo "Your average of rounds is: $sum"
  echo "Your scores are: "
  foreach line (` cat records `)
    echo $line
  end
endif

