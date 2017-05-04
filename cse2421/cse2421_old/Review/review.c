#include <stdio.h>
#include <stdlib.h>


//structures


int main(void){

int x = 3;
int y = 2;
printf("X = %d\n",x);
printf("Y = %d\n",y);
int *ptrX;
int *ptrY;
//pointers
	//pointer assignment
	printf("POINTER ASSIGNMENTS\n");
	ptrX = &x;
	ptrY = &y;
	printf("ptrX = %p\n",ptrX);
	printf("ptrY = %p\n",ptrY);
	printf("\n");
	ptrY = ptrX;
	printf("ptrY = %d\n", *ptrY);

	/*
	ptrX++;
	printf("ptrX = %p\n",ptrX);
	printf("ptrX = %d\n",*ptrX);
	*/

	
//arrays


}
