#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "matrixOP.h"
#define value_at_index(a,i,j,k,m,n) (a)[(i)*m*n + (j)*n + (k)]
/*
	Name = Charles Stevenson
	DATE = 2/21/2016
	Class = CSE2421 T/TH 5:20PM
	ID: 0x05194445
*/
int main(){
	//initials
	FILE * fp;
	int x,y,z,i,j,k,operation;
	float arg1, arg2;
	int (*addP) (struct spacialData *, float, float);
	int (*multP) (struct spacialData *,float,float);
	int (*squareRootP) (struct spacialData *,float,float);
	int (*squareP) (struct spacialData *,float,float);
	addP = add; 
	multP = multiply;
	squareRootP = squareRoot;
	squareP = square;
	//open file
	fp = fopen("testfile","r");
	if (fp == NULL){
		printf("File didn't open!");
		exit(EXIT_FAILURE);
	}
	
	//get array sizes
	fscanf(fp,"%d",&x);
	fscanf(fp,"%d",&y);
	fscanf(fp,"%d",&z);

	//allocate contiguous space in memory
	spacialData (*spacialDataArr) = (spacialData*)malloc(x*y*z*sizeof(spacialData));
	int (*functionArr[4]) (struct spacialData *, float, float); 
	//fill in information
	functionArr[0] = addP;
	functionArr[1] = multP;
	functionArr[2] = squareRootP;	
	functionArr[3] = squareP;
	for (i = 0; i < z; i++){
		for(j = 0; j < y; j++){
			for(k = 0; k < x; k++){
				fscanf(fp,"%f%f",&(value_at_index(spacialDataArr,i,j,k,(z-1),(y-1)).temp), &(value_at_index(spacialDataArr,i,j,k,(z-1),(y-1)).density));
			}
		}
	}
//transform array;
	while(fscanf(fp, "%d%f%f",&operation, &arg1, &arg2) == 3){
		for (i = 0; i < z; i++){
			for(j = 0; j < y; j++){
				for (k = 0; k < x; k++){
					functionArr[operation](&value_at_index(spacialDataArr,i,j,k,(z-1),(y-1)),arg1,arg2);
				}
			}
		}
	
	}

	//output
	for (i = 0; i < z; i++){
		for(j = 0; j < y; j++){
			for(k = 0; k < x; k++){
				printf("%f ",(value_at_index(spacialDataArr,i,j,k,(z-1),(y-1)).temp));
				printf("%f\n",(value_at_index(spacialDataArr,i,j,k,(z-1),(y-1)).density));
			}
		}
	}
	return EXIT_SUCCESS;
}
