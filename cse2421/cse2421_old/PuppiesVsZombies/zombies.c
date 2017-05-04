/*
 *
 *PUPPIES VS. ZOMBIES
 *
 *    Author : Charles Stevenson
 *    DATE : 09/12/2016
 *
 *Description:
 *     This is a simulation of a room filled with puppies
 *     and zombies. Who will survive? The puppies who
 *     eat the zombies or the zombies who infect the puppies?
 *
 */
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
//MACROS
#define NORTH 0
#define SOUTH 1
#define WEST 2
#define EAST 3
#define INFECT 4
#define DESTROY 5
#define CONFUSED 6
#define Square(x) ((x)*(x))

//function declarations (only doing these if needed);
int get_random_direction();

//Helper Functions
int rand(void){
  static unsigned long int next = 0;
  next = next * 1103515245 + 12345;
  return (unsigned int) (next/65536) % 32768;
}

int distance(int zX, int zY, int pX, int pY){
  return Square((zX - pX) + (zY - pY));
}

int vertDistance(int zY, int pY){
  int temp = zY - pY;
  if (temp < 0){
    temp = temp * -1;
  }
  return temp;
}

int horizDistance(int zX, int pX){
  int temp = zX - pX;
  if (temp < 0){
    temp = temp * -1;
  }
  return temp;
}

int get_room_width(FILE *f){
  int w = 0;
  fscanf(f, "%d", &w);
  //printf("WIDTH = %d\n",w);
  return w;
}

int get_room_height(FILE *f){
  int h = 0;
  fscanf(f, "%d", &h);
  //printf("HEIGHT = %d\n",h);
  return h;
}

int get_iterations(FILE *f){
  int i = 0;
  fscanf(f, "%d", &i);
  return i;
}

void load_room(FILE *f, int rows,int cols,char room[][cols]){
  //load file into room array
  int buffer = 100;
  char line[buffer];
  fgets(line,buffer,f);
  fgets(line,buffer,f);
  for(int i = 0; i < rows; i++){
      for(int j = 0; j < cols; j++){
        room[i][j] = line[j];
        printf("%c",room[i][j]);
      }
    printf("\n");
    fgets(line,buffer,f);
    }
  }

void save_room(FILE * f,int rows,int cols,char room[][cols]){
 char temp;
 for(int i = 0; i < rows; i++){
    for(int j = 0; j < cols; j++){
      printf("%c",room[i][j]);
      //fprintf(f,"%c", room[i][j]);
    }
    printf("\n");
    //fprintf(f,"\n");
 }
}

/*
 *
 *
 *Get Zombie Direction
 *
 */

int get_zombie_direction(int rows,int cols,char room[][cols],int currRow,int currCol){
  //initials
  int nPup = Square(rows);//max distance
  int nPupLocVert = 0;
  int nPupLocHoriz = 0;
  char zombie = room[currRow][currCol];
  int zMov = 0;//temp variable to hold distance
  int vertDist = 0;
  int horizDist = 0;
  int dist = 0;
  int currLoc;

  //movement: are 2 puppies near?
  for(int i = 0; i < rows; i++){
    for(int j = 0; j < cols; j++){
      currLoc = room[i][j];
      if (currLoc == 'p' || currLoc == 'P'){
        vertDist = vertDistance(currRow,i);
        horizDist = horizDistance(currCol,j);
        dist = distance(currRow,currCol,i,j);
        if (dist < nPup){//find nearest puppy
          nPupLocHoriz = i;
          nPupLocVert = j;
          nPup = dist;
        }
        else if (nPup = dist || vertDist == horizDist){//if 2 equal distance don't move
          zMov = -1;
        }
      }
    }
  }
  //Find Direction to Nearest Puppy
  if(zMov != -1){
      if(nPupLocHoriz < currCol){
        zMov = WEST;
      }
      else if(nPupLocHoriz > currCol){
        zMov = EAST;
      }
      else if (nPupLocVert < currRow){
        zMov = NORTH;
      }
      else if (nPupLocVert > currRow){
        zMov = SOUTH;
      }
    }

  if(rand()%5){
    //printf("RANDOM\n");
    zMov = get_random_direction();
  }
  return zMov;
}
/*
 *
 *
 *puppy direction
 *
 */
int get_puppy_direction(int rows,int cols,char room[][cols],int currRow,int currCol){
  int nZom = Square(rows);//nearest zombie; (min)
  int nZomLocHoriz = 0;//nearest zombie location horizontal
  int nZomLocVert = 0;//nearest zombie location vertical
  int pMov = 0;
  int dist = 0;
  int vertDist = 0;
  int horizDist = 0;
  int currLoc;

  char puppy = room[currRow][currCol];
  //find closest zombies!!
  for(int i = 0; i < rows; i++){
    for(int j = 0; j < cols; j++){
      currLoc = room[i][j];
      vertDist = (currRow, i);
      horizDist = (currCol, j);
      if (currLoc == 'z' || currLoc == 'Z'){
        if (dist < nZom){
          nZomLocHoriz = i;
          nZomLocVert = j;
          nZom = dist;
        }
        else if (dist == nZom || vertDist == horizDist){
          pMov = -1;
        }
      }
    }
  }

  //Find Direction away from Nearest Zombie
  if (pMov != -1){
      if(nZomLocHoriz < currCol){
        pMov = EAST;
      }
      else if(nZomLocHoriz > currCol){
        pMov = WEST;
      }
      else if (nZomLocVert < currRow){
        pMov = SOUTH;
      }
      else if (nZomLocVert > currRow){
        pMov = NORTH;
      }
    }

  //random direction
  if (rand()%5 == 0){
    pMov = get_random_direction();
  }
  return pMov;
}

int get_random_direction(){
  return (rand()%4);
}

int cast_action(int rows, int cols, char room[][cols], int currRow, int currCol, char unit){
  int action = 0;
  int puppies = 0;
  int locR = currRow;
  int locC = currCol;
  //checking for adjacent puppies
  if(room[currRow+1][currCol] == 'p' || room[currRow+1][currCol] == 'P'){
    puppies++;
    locR = currRow + 1;
  }
  if(room[currRow-1][currCol] == 'p' || room[currRow-1][currCol] == 'P'){
    puppies++;
    locR = currRow - 1;
  }
  if(room[currRow][currCol+1] == 'p' || room[currRow][currCol] == 'P'){
    puppies++;
    locC = currCol + 1;
  }
  if(room[currRow][currCol-1] == 'p' || room[currRow][currCol] == 'P'){
    puppies++;
    locC = currCol - 1;
  }
  if(puppies > 1){//Destroy
    room[currRow][currCol] = ' ';
    action = 1;
  }
  else if (puppies == 1){//Infect
    room[locR][locC] = 'z';
    room[currRow][currCol] = 'z';
    action = 1;
  }
  return action;
}
void movement(int mov, int rows, int cols, char room[][cols],int currRow,int currCol,char unit){
    int iRow = currRow;
    int iCol = currCol;
    if (mov == NORTH){
      currRow = currRow - 1;
    }
    else if (mov == SOUTH){
      currRow = currRow + 1;
    }
    else if (mov == EAST){
      currCol = currCol + 1;
    }
    else if (mov == WEST){
      currCol = currCol - 1;
    }

    if(room[currRow][currCol] == ' '){
      room[currRow][currCol] = unit;
      if(room[currRow][currCol] == 'P'){
        room[currRow][currCol] = 'p';
      }
      if(room[currRow][currCol] == 'Z'){
        room[currRow][currCol] = 'z';
      }
      room[iRow][iCol] = ' ';
    }
}

void printMov(int mov, char unit){
  printf("%c Movement = %d\n",unit,mov);
}

/*
 *
 *
 *
 *Simulation Loop
 *
 *
 */

void iteration_simulation(int rows, int cols, char room[][cols]){

  int mov = 0;
  int action = 0;

  //Rested
  for (int i = 0; i < rows; i++){
    for (int j = 0; j < cols; j++){
      if(room[i][j] == 'p'){
        room[i][j] = 'P';
      }
      if(room[i][j] == 'z'){
        room[i][j] = 'Z';
      }
    }
  }
  //puppy Movement
  for (int i = 0; i < rows; i++){
    for (int j = 0; j < cols; j++){
      if(room[i][j] == 'P'){
        mov = get_puppy_direction(rows,cols,room,i,j);
        movement(mov,rows,cols,room,i,j,room[i][j]);
      }
    }
  }
  //Zombie Movement
  for(int i = 0; i < rows; i++){
    for(int j = 0; j < cols; j++){
      if(room[i][j] == 'Z'){
        action = cast_action(rows,cols,room,i,j,room[i][j]);
        if(action == 0){
          mov = get_zombie_direction(rows,cols,room,i,j);
          movement(mov,rows,cols,room,i,j,room[i][j]);
        }
      }
     action = 0;
    }
  }
}

int main(void){

  //file
  FILE * f;
  f = fopen("maze","r");
  if (f == NULL){
    exit(EXIT_FAILURE);
  }
  char line[1000];

  //width && height
  fscanf(f, "%s", line);
  int rows = get_room_height(f);
  int cols = get_room_width(f);

  //iterations
  fscanf(f, "%s", line);
  int itr = get_iterations(f);

  //LoadArray
  char room[rows][cols];//room[rows][columns];
  load_room(f,rows,cols,room);
  fclose(f);
  f = fopen("results","w+");

  //loop
  while(itr){
    usleep(100000);
    iteration_simulation(rows,cols,room);
    save_room(f,rows,cols,room);
    itr--;
  }

  //save
  save_room(f,rows,cols,room);
  fclose(f);
}




