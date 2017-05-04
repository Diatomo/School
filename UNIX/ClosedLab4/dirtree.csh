#!/bin/tcsh -f
#Title: Directory Tree

set decision=0
if($#argv == 0) then #sets the directory
  pwd
  set thisdir="."
else
    set thisdir=$argv[1]
    echo "$thisdir"
endif

while ( ($decision != 1 && $decision != 2 && $decision != 3 && $decision != 4) )
  echo "The current directory is: "
  echo "$thisdir"
  echo "1. Enter a directory name"
  echo "2. Print the directory tree in the screen"
  echo "3. Print the directory tree to a file"
  echo "4. Exit"
  set decision=$<

  if($#argv == 0) then #sets the directory
    set thisdir="."
  else
    set thisdir=$argv[1]
  endif

  if ( $decision == 1) then
    echo "Enter a directory Name"
    set thisdir=$<
  endif

  if ( $decision == 3) then
    echo "File Name : "
    set dirtree=$<
    touch $dirtree
  endif

  if ($?TREEPREFIX) then #if a tree prefix exist
    set prefix="$TREEPREFIX" #set prefix to the tree prefix
  else
    set prefix="" #else set it to nothing
  endif

if ( $decision != 4 ) then
  if ( $decision == 3 || $decision == 2) then
    echo "$prefix|" #print out the prefix
    set filelist=`ls -A $thisdir` #set the file list to environment variable $thisdir
    foreach file ($filelist) #loop through the files
      if ( $decision == 3 ) then
        echo "${prefix}|------${file}" >> $dirtree #print
      else
        echo "${prefix}|------${file}"
      endif

      if (-d "$thisdir/$file") then
        if($file == $filelist[$#filelist]) then #if the file == the file in the file list
          setenv TREEPREFIX "${prefix}     "
        else
          setenv TREEPREFIX "${prefix}|    "
        endif
        if ( $decision == 3) then
          echo $0 "$thisdir/$file" >> $dirtree
        else
          echo $0 "$thisdir/$file" #echo the file and concatenate to thisdir/file
        endif
      endif
    end
  endif
  echo "$prefix"
set decision=0
endif
end
