#!/bin/tcsh -f

echo "Which file would you like to copy"
ls ~/Documents/secrets
set file=$<
set fPath="~/Documents/secrets/$file"
set dir=`pwd`

cp $fPath $dir
