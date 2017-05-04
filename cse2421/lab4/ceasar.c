
#include "ceasar.h"
//[A-Z] = 65-90
//[a-z] = 97-122

#define MINLC 96
#define MAXLC 122
#define MINUC 64
#define MAXUC 90


void ceasar(int integer, char line[]){
  int temp;
  int i = 0;
  while (line[i] != 0){
    temp = line[i];
    if (line[i] > 64 && line[i] < 123){
      if (line[i] > 64 && line[i] < 91){//UpperCase
        temp = line[i] + integer;
        if (temp > MAXUC){
          temp = MINUC + (temp - MAXUC);
        }
      }
      else if(line[i] > 96 && line[i] < 123){//LowerCase
        temp = line[i] + integer;
        if (temp > MAXLC){
          temp = MINLC + (temp - MAXLC);
        }
      }
    }
   line[i] = temp;
   i++;
  }
}
