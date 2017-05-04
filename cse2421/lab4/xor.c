
#include <stdlib.h>
#include "xor.h"

void xor(char key[], char line[]){

  long theKey;
  char * ptr;
  //printf("%s",key);
  theKey = strtol(key, &ptr, 0);
  int i = 0;
  while (line[i] != 0){
    line[i] = line[i] ^ theKey;
    //printf("%i\n", line[i]);
    i++;
  }
}
