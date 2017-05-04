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
	sub esp, 60000 ;BY stack
	lea edi, [esp]
	sub esp, 60000 ;Mem stack
	mov dword eax, 60000
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
	sub dword ecx, 4
	jmp switch	   
decValue:; -
	dec dword [edi] ;sub one from the cell
	sub dword ecx, 4
	jmp switch
incDataPtr:; >
	sub dword edi, 4 ;sub edi's address
	sub dword ecx, 4
	jmp switch
decDataPtr:; <
	add dword edi, 4 ;add edi's address
	sub dword ecx, 4
	jmp switch
outputData:; .
	call write_byte ;write current data cell
	sub dword ecx, 4
	jmp switch
inputData:; ,		;get data from current data cell
	jmp read_loop
beginLoop:; [		;begin loop   ;decrement address
	push ecx
	mov ebx, [edi]
	cmp ebx, 0
	jle terminateBegLoop
	sub dword ecx, 4
	jmp switch
endLoop: ; ]
	pop edx
	mov ebx, [edi]
	cmp ebx, 0
	jle terminateEndLoop
	mov ecx, edx
	jmp switch
terminateBegLoop:
	sub dword ecx, 4
	jmp skip
terminateEndLoop:
	sub dword ecx, 4
	jmp switch

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
	mov ecx, edi  ;data to load
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
	xor ecx, ecx
	mov eax, 3 ;std_read
	mov ebx, 0 ;file descriptor stdin
	mov ecx, esi
	mov edx, 1 ;byte count
	int 0x80 ;system call
	;mov esi, ecx
	sub dword esi, 4 ;decrement stack pointer
	;mov edx, [ecx]
	cmp dword [ecx], 35 ;compare if at the end of the line
	jne switch ;if not equal jump to switch	
	cmp dword [ecx], 35
	je exit_read 
	;cleanup
skip:
	mov eax, 3 ; read
	mov ebx, 0
	mov ecx, esi
	mov edx, 1
	int 0x80
	sub dword esi, 4
	cmp dword [ecx], 35 ;if its a terminating character exit_read
	je exit_read		
	cmp dword [ecx], 93 ;if its a closing ']' then jmp to read_loop for next char
	jne skip
	jmp read_loop	    ;if not 
;sift:
	;dec dword ecx
	;mov eax, [ecx]
	;cmp dword eax, 93
	;je decrement
	;jmp
decrement:
	sub dword ecx, 4
	jmp switch


exit_read:
	pop edx ;restore edx
	pop ecx ;restore ecx
	pop esi ;restore esi pointer
	pop ebx ;restore ebx
	;add esp, 8 ;cleanup local stack
	pop ebp ;restore pointer
	;pop ebp
	jmp exit  ;return 
