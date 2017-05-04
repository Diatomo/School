

;Author: Charles C. Stevenson
;Program EliminateNsort
;Description:
;	Takes two list and returns a list of the non-intersection in increasing order




;CreateNewList
;concatenates a list from a non duplicate and list of non-duplicates
(define (createNewList lstA lstB)
(cond
((null? lstA) lstB)
(#t (sort lstA lstB))))

;Sort
;Sorts a list in increasing order
(define (sort head tail)
(cond
((null? tail) (cons head tail));if the tail is null just concatenate the header element to the list
((< head (car tail)) (cons head tail));if the tail is not null but the header is less than the first element of the tail, concatenate or append
(#t (cons (car tail) (sort head (cdr tail))))));if the header element is not less then the tail then recurse

;Eliminate N sort
;removes head of list one and checks for duplicates in list two, if not, it'll recurse to the end of lstA
;and then begin constructing the output list
(define (eliminateNsort lstA lstB)
(cond
((null? lstA) lstA);check if list A is null return an empty list
((null? (cdr lstA)) (createNewList (removeHead lstA lstB lstB) (eliminateNsort (cdr lstA) lstB)));This attempts to avoid duplicates
((eqv? (removeHead lstA lstB lstB) (car (cdr lstA))) (eliminateNsort (cdr lstA) lstB)) ;Checks if the next element in lstA is equivalent to removeHead, which means removeHead skipped ahead so no need to pass it again
(#t (createNewList (removeHead lstA lstB lstB) (eliminateNsort (cdr lstA) lstB)))));creates new list

;RemoveHead
;Removes the head of lstA and checks if duplicates in lstB, which it then removes that from lstA
;lstC here is just to start at the beginning of lstB in case there is a duplicate.
(define (removeHead lstA lstB lstC)
(cond
((null? lstB) (car lstA));if lst B is empty just return the header element as there are no duplicates.
((null? lstA) lstA);if the end of list A is a duplicate just return the empty list
((eqv? (car lstA) (car lstB)) (removeHead (cdr lstA) lstC lstC)); if they are equivalent remove that element from being returned
(#t (removeHead lstA (cdr lstB) lstC))));else recurse

