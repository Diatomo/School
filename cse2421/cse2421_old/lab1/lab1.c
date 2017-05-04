
/*
 *
 *Author : CHARLES STEVENSON
 *DATE : AUGUST 29th, 2016
 *CLASS : CSE2421 MW 4:10 - 6:15pm
 *
 */


#include <stdio.h>
#include <stdlib.h>


int isPrime(long int num){
  int prime = 1; // bool 
  long int i = 2; //int i > 1
  if (num % 2 == 0 || num == 1){
    prime = 0;
  }
  else{
    //linear test for primality
    for (i; i < num; i++){
      if (num % i == 0){
        prime = 0;
        break;//break if not prime
      }
    }
  }
  return prime;
}



int main(){
  long int num = 1;//input
  int prime;//boolean
  while(num != 0){
    scanf("%ld", &num);//read number
    if (num != 0){//if number is 0 terminate
      prime = isPrime(num);//test if prime
      if (prime == 0){
        printf("not prime\n");
      }
      else{
        printf("prime\n");
      }
    }
  }
  return 0;
}
