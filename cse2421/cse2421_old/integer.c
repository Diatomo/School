#include <stdio.h>
#include <stdlib.h>

/*
	NAME: CHARLES STEVENSON
	DATE: 02/14/2016
	CLASS: CSE2421 T\TH 5:20pm
	ID: 0x05194445
*/

struct node{
	struct node *next;
	int data;
};

int createLL(struct node** head, struct node** curr, struct node** tail,char ch){
	int length = 0;
	int number = 0;
	while ((scanf("%c",&ch)) && (ch != '\n')){
		*curr = (struct node*)malloc(sizeof(struct node)); //allocate space
		number = ch - '0' ; //convert char to number
		(*curr)->data = number;
		(*curr)->next = *head;
		*head = *curr;
		if (length == 0){
			*tail = *curr;
		}
		length++;
	}
	*curr = *head;
	return length;
	}
void destroyLL(struct node** head, struct node** curr){
	while (*head){
		*curr = *head;
		*head = (*curr)->next;
		free(*curr);
	}
}

void addition(struct node** currOne,  struct node** currTwo, struct node** headThree, struct node** currThree, int lengthOne, int lengthTwo){
	int numberOne, numberTwo, sum;
 	int longest;
	if (lengthTwo > lengthOne){//find longest to decrement while loop
		longest = lengthTwo;//could do with pointing to pointers.
	}
	else{
		longest = lengthOne;
	}
	while(longest){
		//COLLECT DATA FROM LL
		if(*currOne){//check if currOne != NULL
			numberOne = (*currOne)->data;
			*currOne = (*currOne)->next;
		}
		else{//if NULL
			numberOne = 0;
		}
		if(*currTwo){//check if currTwo != NULL
			numberTwo = (*currTwo)->data;
			*currTwo = (*currTwo)->next;
		}
		else{//if NULL
			numberTwo = 0;
		}
		sum = numberOne + numberTwo + sum;//sum data from both linked list
		//APPEND SUM TO RESULTING LL
		*currThree = (struct node*)malloc(sizeof(struct node));//construct node
		if(sum > 9){//if sum is greater than 9 (subtract 10 and grab the left over tens place, i.e. the '1' in '18')
			(*currThree)->data = (sum-10);
			sum = sum/10;
		}
		else{//else append sum and set it to 0;
			(*currThree)->data = (sum);
			sum = 0;
		}
		(*currThree)->next = *headThree;
		*headThree = *currThree;
		longest--;
	}
	if(sum){//If there is an extra sum left over append to a the head of the third LL
		*currThree = (struct node*)malloc(sizeof(struct node));
		(*currThree)->data = sum;
		(*currThree)->next = *headThree;
		*headThree = *currThree;
	}
	*currThree = *headThree;
}

void subtraction(struct node** currOne, struct node** headOne,struct node** currTwo, struct node** headTwo, struct node** currThree, struct node** headThree, int lengthOne, int lengthTwo){
	int numberOne, numberTwo, diff;
	int carry = 0;
	struct node* longest;
	struct node* shortest;
	//CHECK WHICH NUMBER IS BIGGER (first by length)
	/*if(lengthTwo > lengthOne){
		longest = *currTwo;
		shortest = *currOne;
	}
	else if (lengthOne > lengthTwo){
		longest = *currOne;
		shortest = *currTwo;
	}
	//then if they are the same length by tail number
	else{
		if(((*headOne)->data) > ((*headTwo)->data)){
			longest = *currOne;
			shortest = *currTwo;
		}
		else{
			logest = *currTwo;
			shortest = *currOne;
		}
	}*/
	longest = *currOne;
	shortest = *currTwo;
	while(longest){
	//I cooked up some of my own math on this...
	//so I'll do my best to explain..
		if(shortest){
			//get data from LL
			numberOne = (*longest).data;
			longest = (*longest).next;
			numberTwo = (*shortest).data;
			shortest = (*shortest).next;
			if(carry && (numberOne == 0)){//If the difference of two numbers required a carry and is 0
				numberOne += 10;//add the number by 10
				numberOne--;//and subtract by 1; so this would by the '2101 - 9); (2191 - 9 )
			}
			else if (carry && (numberOne > 0)){//if the difference of two number required a carry and is !0
				numberOne--;//subtract numberOne
				carry--;//set flag to say carry complete
			}
			if (numberOne - numberTwo < 0){//if diff of two numbers is less than zero
				numberOne += 10;//add 10 to the bigger number
				carry++;//and a carry just happened.
			}
			diff = numberOne - numberTwo;//diff the numbers
			*currThree = (struct node*)malloc(sizeof(struct node));//add to node
			(*currThree)->data = diff;
		}
		else if (longest && carry){//when shortest is out of numbers and a carry was left over
			//get data
			numberOne = (*longest).data;
			longest = (*longest).next;
			//simulate carry events
			if (numberOne != 0){
				numberOne--;
				carry--;
			}
			else{	
				numberOne += 10;
				numberOne--;
			}
			*currThree = (struct node*)malloc(sizeof(struct node));
			(*currThree)->data = numberOne;
			}
		else{
			//assign number to data.
			numberOne = (*longest).data;
			longest = (*longest).next;
			*currThree = (struct node*)malloc(sizeof(struct node));
			(*currThree)->data = numberOne;
		}
	(*currThree)->next = *headThree;
	*headThree = *currThree;
	}
	*currThree = *headThree;
}
int main(){
	//initials
	int lengthOne, lengthTwo; 
	int leadingZeros = 1;
	char ch = 1;
	//node pointers (a lot of them)
	struct node* headOne = NULL;
	struct node* currOne = NULL;
	struct node* tailOne = NULL;
	struct node* headTwo = NULL;
	struct node* currTwo = NULL;
	struct node* tailTwo = NULL;
	struct node* headThree = NULL;
	struct node* currThree = NULL;
	//create linked list and return length for use in subtraction and addition
	lengthOne = createLL(&headOne,&currOne, &tailOne, ch);
	lengthTwo = createLL(&headTwo,&currTwo, &tailTwo, ch);
	
	scanf("%c",&ch);
	if (ch == '+'){
		addition(&currOne, &currTwo, &headThree, &currThree, lengthOne, lengthTwo);
	}
	else if(ch == '-'){
		subtraction(&currOne, &tailOne, &currTwo, &tailTwo, &currThree, &headThree, lengthOne, lengthTwo);
	}
	//OUTPUT
	while((currThree)){
		if ((currThree->data == 0) && (leadingZeros > 0)){
			currThree = currThree->next;
		}
		else{
			printf("%d",currThree->data);
			currThree = currThree->next;
			leadingZeros--;
		}
	}
	printf("\n");
	currThree = headThree;
	destroyLL(&headOne, &currOne);
	destroyLL(&headTwo, &currTwo);
	destroyLL(&headThree, &currThree);
	return 0;
}
