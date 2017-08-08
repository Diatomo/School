/*
 *
 *
 *    Author : Charles C. Stevenson
 *    Date   : 09/30/2016
 *    Description:
 *      This is a program that runs two different ciphers
 *       1)Ceasar Cipher
 *         Is a direct substitution cipher
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "xor.h"
#include "ceasar.h"

//[A-Z] = 65-90
//[a-z] = 97-122

#define MINLC 96
#define MAXLC 122
#define MINUC 64
#define MAXUC 90


void printUsage(){
    printf("==========================================================\n");
    printf("try the forms ./lab4 (encyption) (plaintext) or\n");
    printf("              ./lab4 (encryption) (flag) (key) (plaintext)\n\n");
    printf("Encryption = xor || ceasar\n");
    printf("flag = -k for xor && flag = -r for ceasar\n");
    printf("key = an int || hex (e.g. 0xFF)\n");
    printf("plain text = " " if a space exist use quotesi\n");
    printf("\nExamples\n");
    printf("./lab4 xor -k 0x22 Hello\n which returns jGNNM\n");
    printf("./lab4 ceasar -r 3 \"Hello, World!\"\n which returns Khoor,Zruog!\n");
    printf("==========================================================\n");
}
/*
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
*/
int main(int argc, char *argv[]){
  //test input!
  //for (int i  = 0; i < argc; i++){
    //printf("argument %d: %s\n", i, argv[i]);
  //}
  //initials
  char cipher[10];
  char line[20];
  memset(line,'\0',sizeof(line));
  char option[10];
  int integer = -1;
  char key[10];
  memset(key, '\0',sizeof(key));

  //grab args
  if (argc == 3){
    strcpy(cipher, argv[1]);
    strcpy(line, argv[2]);
    integer = 13; //default value
  }
  else if (argc == 5){
    strcpy(cipher, argv[1]);
    strcpy(option, argv[2]);
    if ((strcmp(option, "-k") == 0) || (strcmp(option, "-r") == 0)){
    }
    else{
      printf("%s is an INVALID FLAG\n", option);
      printUsage();
      return 0;
    }
    integer = atoi(argv[3]);
    strcpy(line, argv[4]);
  }
  else{
    printf("INVALID NUMBER OF ARGUMENTS\n");
    printUsage(0);
    return 0;
  }

  //determine control flow
  //printf("BEFORE INPUT %s\n", line);
  if (strcmp(cipher, "ceasar") == 0){
    ceasar(integer,line);
  }
  else if (strcmp(cipher, "xor") == 0){
    strcpy(key,argv[3]);
    xor(key,line);
  }
  else{
    printf("%s is an INVALID CIPHER ARGUMENT\n", argv[1]);
    printUsage(1);
    return 0;
  }
  printf("%s\n",line);
  memset(line,'\0',sizeof(line));
  return 0;
}
