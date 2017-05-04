#include <stdio.h>
static int var_s = 30;
int main(int argc, char **argv)
{
  int var_x = atoi(argv[1]);
  int var_y = atoi(argv[2]);
  printf("%d\n", var_x + var_s);
  var_y += var_s;
  printf("%d\n", var_y);
  return 0;
}
