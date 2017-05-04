;Assembly


;Author = Charles Stevenson
;Date = 4/12/16
;Class = cse2421
;
USE32
global _start
_start:

main:
	;create stack
	push ebp
	mov ebp, esp
	lea esi, [esp]
	sub esp, 30000 ;BY stack
	lea edi, [esp]
	sub esp, 30000 ;Mem stack
	mov dword eax, 30000
	lea ecx, [edi]
	lea ebx, [esi]
initializeZero:
	mov dword ecx, 0
	mov dword ebx, 0
	dec dword ecx
	dec dword ebx
	dec dword eax
	cmp eax, 0
	jge initializeZero
	call read_byte
;	call write_byte
exit:
	add esp, 60000
	mov ebx, 0
	mov eax, 1
	int 80h

switch:
	;extract value from stack
	cmp dword [ecx], 43; + ; increment value where data pointer is
	je incValue
	cmp dword [ecx], 45; - ; decrement value where data pointer is
	je decValue
	cmp dword [ecx], 62; > ; increment data pointer
	je incDataPtr
	cmp dword [ecx], 60; < ; decrement data pointer
	je decDataPtr
	cmp dword [ecx], 46; . ;output
	je outputData
	cmp dword [ecx], 44; , ;accept one byte of input
	je inputData
	cmp dword [ecx], 91; [ ;while where point is at has value
	je beginLoop
	cmp dword [ecx], 93; ] ;jump back to beg loop if something has value.
	je endLoop
	jmp read_loop

incValue:; +
	inc dword [edi] ;add one to the cell 
	dec dword ecx
	jmp switch	   
decValue:; -
	dec dword [edi] ;sub one from the cell
	dec dword ecx
	jmp switch
incDataPtr:; >
	dec dword edi ;sub edi's address
	dec dword ecx
	jmp switch
decDataPtr:; <
	inc dword edi ;add edi's address
	dec dword ecx
	jmp switch
outputData:; .
	call write_byte ;write current data cell
	inc dword ecx
	jmp switch
inputData:; ,		;get data from current data cell
	jmp read_loop
beginLoop:; [		;begin loop
	push ecx	;save adress
	dec dword ecx   ;decrement address
	mov ebx, [edi]
	cmp ebx, 0
	jle endingEndLoop
	jmp switch	;jump to switch
endLoop: ; ]
	mov ebx, [edi]  ;see if cell is 0
	cmp ebx, 0
	jle endingEndLoop
continue:		;if it isn't continue with switch
	pop ecx		;pop address
	;sub dword ecx, 4
	jmp switch	;continue w/ switch
endingEndLoop:		;if it is
	pop ecx		;pop address
	jmp read_loop	;and jump to read loop.

write_byte:
	
	;create stack
	push ebp
	mov ebp, esp
	;save registers
	push eax
	push ebx
	push ecx
	push edx	
	;write
	mov eax, 4 ;sys call write
	mov ebx, 1 ;file descriptor (stdout)
	mov ecx, [edi]  ;data to load
	mov edx, 1 ;byte size
	int 0x80   ;system call
	
	;clean up
	pop edx
	pop ecx
	pop ebx
	pop eax
	pop ebp
	ret

read_byte:	
	;create stack
	push ebp
	mov ebp, esp
	;save registers
	;sub esp, 8
	;mov dword[ebp-4],'0'
	push ebx
	push esi
	push ecx
	push edx
	;sub esp, 8
	;mov dword [ebp-4], '0'
	;xor ecx, ecx
read_loop:
	;xor eax, eax ;clear eax
	mov eax, 3 ;std_read
	mov ebx, 0 ;file descriptor stdin
	mov ecx, esi
	mov edx, 1 ;byte count
	int 0x80 ;system call
	mov esi, ecx
	dec dword esi ;decrement stack pointer
	cmp dword [ecx], 35 ;compare if at the end of the line
	jne switch ;if not equal jump to switch	
	;cleanup
	pop edx ;restore edx
	pop ecx ;restore ecx
	pop esi ;restore esi pointer
	pop ebx ;restore ebx
	;add esp, 8 ;cleanup local stack
	pop ebp ;restore pointer
	;pop ebp
	jmp exit  ;return 
