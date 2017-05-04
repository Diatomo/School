#include <stdio.h>
#include <stdlib.h>
#include <time.h>


typedef struct Date{
	int month;
	int day;
	int year;
} Date;

typedef struct Event{
	int uniqueID; 
	char title[50];
	struct Date *date;
	struct Event *next;
	struct Event *previous;

} Event;


void initEvent(Event **curr, Event **head, time_t sec){

	//Struct Init memory space
	Event * temp = malloc(sizeof(Event));
	//*curr = malloc(sizeof(Event));
	Date * date =  malloc(sizeof(Date));
	
	//local variables
	char title[50];
	int month;
	int day;
	int year;

	//Get Event Data From User	
	printf("\nTitle of your event : ");
	scanf("%s", title);
	printf("Date : Month of your event : " );
	scanf("%d", &month);
	printf("Date : Day of your event : " );
	scanf("%d",&day);
	printf("Date : Year of your event : ");
	scanf("%d",&year);
	
	//set attributes to struct
	temp->date = date;
	temp->uniqueID = sec/3600;
	strcpy(temp->title, title);
	temp->date->day = day;
	temp->date->month = month;
	temp->date->year = year;

	//Receipt Information About newly Created Event
	printf("\nEvent Created!\n");
	printf("============================\n");
	printf("\nUNIQUE ID : ");
	printf("%d", temp->uniqueID);
	printf("\nEvent Title : ");
	printf("%s", temp->title);
	printf("\nDATE:month : ");
	printf("%d", temp->date->month);
	printf("\nDATE:day : ");
	printf("%d", temp->date->day);
	printf("\nDATE:year : ");
	printf("%d", temp->date->year);
	printf("\n\n");
	temp->next = NULL;
	temp->previous = NULL;
	(*curr) = temp;
}
/*	//sort things are inserted
	sortingOfList(curr, head, &temp);
	*curr = *head;

}
	
void sortingOfList(Event **curr, Event **head, Event **temp){
	
	printf("\nPARAMETER PASS TEST!\n");
	printf("============================\n");
	printf("\nUNIQUE ID : ");
	printf("%d", (*temp)->uniqueID);
	printf("\nEvent Title : ");
	printf("%s", (*temp)->title);
	printf("\nDATE:month : ");
	printf("%d", (*temp)->date->month);
	printf("\nDATE:day : ");
	printf("%d", (*temp)->date->day);
	printf("\nDATE:year : ");
	printf("%d", (*temp)->date->year);
	printf("\n\n");
	
	while((*curr)->uniqueID != 0){
		//if nodes date is > year or if year is equal then is node's month > curr month etc...
		printf("EXECUTING loop");
		if ((((*temp)->date->year) < ((*curr)->date->year)) || 
			((*temp)->date->year == (*curr)->date->year) && ((*temp)->date->month < (*curr)->date->month) || 
			((*temp)->date->year == (*curr)->date->year && (*temp)->date->month == (*curr)->date->month && (*temp)->date->day < (*curr)->date->day)){
			//link up new node : temp before
			printf("LESS THAN");
			printf("LINE 1");
			(*temp)->next = *curr;
			printf("LINE 2");
			(*temp)->previous = (*curr)->previous;
			//modify links for already existing node : curr
			printf("LINE 3");
			if((*curr)->previous != NULL){
			//	(*curr)->previous->next = *temp;
			}
			printf("LINE 4");
			(*curr)->previous = *temp;
			printf("LINE 5");
			if ((*temp)->previous == NULL){
				*head = *temp;
			}
			break;
		}

		else{ 
			printf("GREATER THAN");
			//link up new node : temp after
			(*temp)->next = (*curr)->next;
			(*temp)->previous = (*curr);
			//modify links for already existing node : curr
			(*curr)->next->previous = *temp;
			(*curr)->next = *temp;
			break;
		}
		*curr = (*curr)->next;
	}
	if ((*curr)->uniqueID != 0){	
		printf("\nCURR PASS TEST!\n");
		printf("============================\n");
		printf("\nUNIQUE ID : ");
		printf("%d", (*curr)->uniqueID);
		printf("\nEvent Title : ");
		printf("%s", (*curr)->title);
		printf("\nDATE:month : ");
		printf("%d", (*curr)->date->month);
		printf("\nDATE:day : ");
		printf("%d", (*curr)->date->day);
		printf("\nDATE:year : ");
		printf("%d", (*curr)->date->year);
		printf("\n\n");
	}
	else{
		printf("SINGLE NODE");
		*curr = *temp;
		//(*curr)->next = *head;
		//(*curr)->previous = NULL;
		*head = *curr;
	}

	printf("\nHEAD TEST\n");
	printf("============================\n");
	printf("\nUNIQUE ID : ");
	printf("%d", (*head)->uniqueID);
	printf("\nEvent Title : ");
	printf("%s", (*head)->title);
	printf("\nDATE:month : ");
	printf("%d", (*head)->date->month);
	printf("\nDATE:day : ");
	printf("%d", (*head)->date->day);
	printf("\nDATE:year : ");
	printf("%d", (*head)->date->year);
	printf("\n\n");
	while((*curr)->next != NULL){
		printf("\nLINKING TEST!\n");
		printf("============================\n");
		printf("\nUNIQUE ID : ");
		printf("%d", (*curr)->uniqueID);
		printf("\nEvent Title : ");
		printf("%s", (*curr)->title);
		printf("\nDATE:month : ");
		printf("%d", (*curr)->date->month);
		printf("\nDATE:day : ");
		printf("%d", (*curr)->date->day);
		printf("\nDATE:year : ");
		printf("%d", (*curr)->date->year);
		printf("\n\n");
		*curr = (*curr)->next;
	}
	*curr = *head;
}*/

void saveFile(Event **curr, Event **head){
	
	FILE *fp; //open file
	fp = fopen("saveFile.txt", "w");
	
	//write to file (iterate through LL)
	while(((*curr)->next) != NULL){
		fprintf(fp,"%d\n", (*curr)->uniqueID);
		fprintf(fp,"%s\n", (*curr)->title);
		fprintf(fp,"%d\n", (*curr)->date->month);
		fprintf(fp,"%d\n", (*curr)->date->day);
		fprintf(fp,"%d\n", (*curr)->date->year);
		fprintf(fp, "\n");
		*curr = (*curr)->next;
	}
	
	*curr = *head;//reset LL
	fclose(fp); // close file
}

void loadFile(Event **curr, Event **head){
	
	//initials	
	int uniqueID;
	char title[50];
	int month;
	int day;
	int year;
	char space;
	char fileName[50];

	scanf("%s", fileName);
	FILE *file;
	file = fopen(fileName, "r");
	//fscanf(file, "%d", &uniqueID);
	
	while (!feof(file)){
		fscanf(file,"%d", &uniqueID); 
		fscanf(file,"%s", title);
		fscanf(file,"%d", &month);
		fscanf(file,"%d", &day);
		fscanf(file,"%d", &year);
		fscanf(file,"%c", &space);

		//create Struct		
		*curr = malloc(sizeof(Event));
		Date * date = malloc(sizeof(Date));

		//TEST SCANF
		printf("SCANF TEST : loadfile()\n");
		printf("============================\n");
		printf("\nUniqueID : ");
		printf("%d", uniqueID);
		printf("\nEvent Title : ");
		printf("%s", title);
		printf("\nDATE:month : ");
		printf("%d", month);
		printf("\nDATE:day : ");
		printf("%d", day);
		printf("\nDATE:year : ");
		printf("%d", year);
		printf("\n\n");
	
		//Fill in struct
		(*curr)->date = date;
		(*curr)->uniqueID = uniqueID;
		strcpy((*curr)->title, title);
		(*curr)->date->day = day;
		(*curr)->date->month = month;
		(*curr)->date->year = year;
		
		//Create LL
		(*curr)->next = *head;
		*head = *curr;
		fgetc(file);
	}
	fclose(file); //close file
}


int main(void){
	
	//Unique ID generated based on Time (Unix Clock)
	time_t sec;
	sec = time (NULL);
	
	//Linked List	
	Event * curr  = malloc(sizeof(Event));
	curr->uniqueID = 0;
	Event * head;// = malloc(sizeof(Event));
	
	int temp;
	//Test for correct return
	printf("\n Please Enter a Task: (1) InitEvent (0) LoadFile (2) Exit");
	while(scanf("%d",&temp) != 2){
			//scanf test
			printf("SCANF TEST");
			printf("\n================");
			printf("%d\n", temp);
			printf("\n\n");
		if (temp == 1){	
			initEvent(&curr, &head, sec);
			//return Test	
			printf("RETURN TEST!\n");
			printf("============================\n");	
			printf("\nUniqueID : ");
			printf("%d",curr->uniqueID);
			printf("\nEvent Title : ");
			printf("%s", curr->title);
			printf("\nDATE:month : ");
			printf("%d", curr->date->month);
			printf("\nDATE:day : ");
			printf("%d", curr->date->day);
			printf("\nDATE:year : ");
			printf("%d", curr->date->year);
			printf("\n\n");
		}
		
		else if(temp == 0){
			loadFile(&curr, &head);
			//load test
			printf("\n\n\n");
			while(curr->next != NULL){
			printf("LOADED TEST!\n");
			printf("============================\n");
			printf("\nUniqueID : ");
			printf("%d", curr->uniqueID);
			printf("\nEvent Title : ");
			printf("%s", curr->title);
			printf("\nDATE:month : ");
			printf("%d", curr->date->month);
			printf("\nDATE:day : ");
			printf("%d", curr->date->day);
			printf("\nDATE:year : ");
			printf("%d", curr->date->year);
			curr = curr->next;
			}
		}
		//reset current
		curr = head;
		printf("\n\n Please Enter a Task: (1) InitEvent (0) LoadFile (2) Exit");
	}
	//save File
	saveFile(&curr, &head);
	//print(&curr,&head);
	
	return EXIT_SUCCESS;	
};
