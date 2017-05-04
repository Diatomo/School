
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <ncurses.h>

typedef struct{
  long double a;
  long double b;
} complex_t;


complex_t* complex_add(complex_t* z, complex_t* point);
complex_t* complex_multiply(complex_t* z, complex_t* c);
complex_t* complex_sub(complex_t* z, complex_t* point);

int is_in_set(complex_t* point){
  int contains = 1;
  int counter = 0;
  long double convergence = 1000;
  long double prevA;
  complex_t* z = (complex_t*) malloc(sizeof(complex_t));
  prevA = 0;
  z->a = 0;
  z->b = 0;
  while ((z->a) - (prevA) < convergence && counter < 100){
    prevA = z->a;
    z = complex_multiply(z,z);
    z = complex_add(z,point);
    counter++;
  }
  if (counter >= 100){
    contains = 0;
  }
  return contains;
}

complex_t* complex_multiply(complex_t* z, complex_t* c){
  complex_t* element = (complex_t*) malloc(sizeof(complex_t));
  long double tempA = z->a * c->a;
  long double tempB = z->b * c->b * -1;
  long double tempC = 2 * z->a * c->b;
  element->a = tempA + tempB;
  element->b = tempC;
  return element;
}

complex_t* complex_add(complex_t* z, complex_t* point){
  complex_t* element = (complex_t*) malloc(sizeof(complex_t));
  element->a = z->a + point->a;
  element->b = z->b + point->b;
  return element;
}

complex_t* complex_sub(complex_t* z, complex_t* point){
  complex_t* element = (complex_t*) malloc(sizeof(complex_t));
  element->a = z->a - point->a;
  element->b = z->b - point->b;
  return element;
}

long double complex_magnitude(complex_t* z){
  complex_t* element = (complex_t*) malloc(sizeof(complex_t));
  element = z;
  return (long double) sqrt(((element->a * element->a) + (element->b * element->b)));
}

void load_curses(){
  initscr();
  resizeterm(100,300);
  curs_set(0);
  start_color();
  for (int i = 0; i < 256; i++){
    init_pair(i+1, i, 0);
  }
  //resizeterm(200,200);
}

int main(){
  int rows = 50;
  int columns = 50;
  char input = 'a';
  long double Hmin = -4.0;
  long double Hmax = 1.0;
  long double Vmin = -1;
  long double Vmax = 1;
  long double change = 0.2;
  load_curses();

  while(input != 'o'){
  long double dimX = (long double) rows;
  long double dimY = (long double) columns;
  long double intervalA = abs(Hmin - Hmax)/dimX;
  long double intervalB = abs(Vmin - Vmax)/dimY;
  long double counterA = Hmin;
  long double counterB = Vmax;
  complex_t* mandelbrot[columns][rows];

  //populate structure
  for (int i = 0; i < rows; i++){
    for (int j = 0; j < columns; j++){
      int row = i;
      int column = j;
      complex_t* element = (complex_t*) malloc(sizeof(complex_t));
      element->a = counterA;
      element->b = counterB;
      mandelbrot[column][row] = element;
      counterA += intervalA;
    }
    counterA = Hmin;
    counterB -= intervalB;
  }

  //test
  int x = 0;
  int color = 0;
  for (int i = 0; i < rows; i++){
    for (int j =0; j < columns; j++){
      int row = i;
      int column = j;
        x = is_in_set(mandelbrot[column][row]);
        if (x){
          attron(COLOR_PAIR(color%255));
          mvprintw(10+i, 75+j,"x");
        }
        else{
          mvprintw(10+i, 75 + j, " ");
        }
        color++;
    }
  printw("\n");
  }
  endwin();
  //clear();
  refresh();
  scanf("%c", &input);
  if (input == 'a'){//pan left
    Hmin -= change;
    Hmax -= change;
  }
  else if (input == 'd'){//pan right
    Hmin += change;
    Hmax += change;
  }
  else if (input == 's'){//pan down
    Vmin += change;
    Vmax += change;
  }
  else if (input == 'w'){//pan down
    Vmin -= change;
    Vmax -= change;
  }
  else if (input == 'e'){//zoom in
    rows -= 5;
    columns -= 5;
  }
  else if (input == 'q'){//zoom out
    rows += 5;
    columns +=5;
  }
  clear();
  }
  clear();
  endwin();
  return 0;
}
