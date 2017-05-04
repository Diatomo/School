#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "matrixOP.h"
/*
	Name = Charles Stevenson
	DATE = 02/21/2016
	Class = CSE 2421, T/TH 5:20PM
	ID: 0x05194445
*/


int add(struct spacialData *spacialDataArr, float arg1, float arg2){
        spacialDataArr->temp += arg1;
        spacialDataArr->density += arg2;
        return 0;
}

int multiply(struct spacialData *spacialDataArr, float arg1, float arg2){
        spacialDataArr->temp *= arg1;
        spacialDataArr->density *= arg2;
        return 0;
}

int squareRoot(struct spacialData *spacialDataArr, float arg1, float arg2){
        if (arg1 > 0.0000001 || arg1 < -0.000001){
                spacialDataArr->temp = sqrt(spacialDataArr->temp);
        }
        if (arg2 > 0.0000001 || arg2 < -0.000001){
                spacialDataArr->density = sqrt(spacialDataArr->density);
        }
        return 0;
}

int square(struct spacialData *spacialDataArr, float arg1, float arg2){
        if (arg1 > 0.000001 || arg1 < -0.000001){
                spacialDataArr->temp = spacialDataArr->temp * spacialDataArr->temp;
        }
        if (arg2 > 0.000001 || arg2 < -0.000001){
                spacialDataArr->density = (spacialDataArr->density) * (spacialDataArr->density);
        }
        return 0;
}

