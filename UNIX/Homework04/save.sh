#!/bin/tcsh -f


echo "which file would you like to copy?"
set file=$<
if ( ! -d "~/Documents/secrets" ) then
  mkdir ~/Documents/secrets
endif
cp $file ~/Documents/secrets/


