#include <stdio.h>

static int some_static_int = 0;

int complex_function(int arg1, int arg2)
{
  int temp1 = arg1 - 7;
  int temp2 = arg2;
  int temp3 = arg1 * arg2;
  int retval = temp1;
  if (temp2 < 0)
    retval += 17;
  else
    retval -= 13;
  switch(arg1)
  {
    case 0:
      printf("CASE ZERO = ");
      printf("%d\n", arg1);
      retval = retval + temp2 + some_static_int + 4;
    case 1:
      printf("CASE ONE = ");
      printf("%d\n", arg1);
      retval = retval - temp2 + 5;
      break;
    case 2:
      printf("CASE TWO = ");
      printf("%d\n", arg1);
      retval = retval - 13 - some_static_int;
      break;
    case 3:
      printf("CASE THREE = ");
      printf("%d\n", arg1);
      retval = retval + (temp3 * 7) - temp2;
    default:
      printf("CASE DEFAULT = ");
      printf("%d\n", arg1);
      retval += 1;
      break;
  }
  some_static_int = some_static_int - arg1 + retval;
  return retval;
}

int main(int argc, char **argv)
{
  int outer_limit = atoi(argv[1]);
  int inner_limit = atoi(argv[2]);
  int counter1;
  int counter2;
  for(counter1=0; counter1 < outer_limit; counter1++)
  {
    for(counter2=2; counter2 > inner_limit; counter2--)
    {
      printf("(%d, %d): %d\n", counter1, counter2, complex_function(counter1, counter2));
    }
  }
  return 0;
}

