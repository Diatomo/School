#include <stdio.h>
#include <stdbool.h>

unsigned int read_integer(void)
{
  unsigned int n;
  scanf("%u",&n);
  return n;
}

void print_prime(void)
{
  printf("prime\n");
}

void print_not_prime(void)
{
  printf("not prime\n");
}

int main(void){

  unsigned int i;
  unsigned int n=read_integer();
  bool is_prime;

  while (n!=0)
  {
    if (n==1) {
      print_not_prime();
    }
    else{
      is_prime=true;
      for (i=2; i*i<=n; i++) {
        if ((n%i)==0){
          is_prime=false;
          break;
        }
      }
      if (is_prime){
        print_prime();
      }
      else{
        print_not_prime();
      }
    }
    n=read_integer();
  }
}
