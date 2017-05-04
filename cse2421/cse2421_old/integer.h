#ifndef createLL
#define createLL


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
#endif
