;
;This is an assembly program for Lab7
;Author :  Charles Stevenson
;Class : CSE2421
;
;REGISTERS = EAX, EBX, ECX, EDX, ESI, EDI

global main
extern printf
extern atoi

format_string_1 db "(%d,%d): %d\n",0xa,0

main:
	;set up the stack frame
	push ebp
	mov ebp, esp
	;allocate space for mains local variables
	sub esp, 16 ; 5 locals

  ;make room for first parameter call to atoi
	sub esp, 4
	;point ecx to the top of the stack
	mov ecx, [ebp+24]
	;copy first parameter to eax
	mov eax, [ecx+4]
	;set[esp] to eax
	mov [esp], eax
	call atoi
	;restore
	add esp, 4
	;store
	mov [ebp-4], eax
	;make room for second parameter call to atoi
	sub esp, 4
	;point ecx to the top of the stack
	mov ecx, [ebp+24]
	;copy second parameter to eax
	mov eax, [ecx+8]
	;set [esp] to eax
	mov [esp], eax
	call atoi
	;restore
	add esp, 4
	;store
	mov [ebp-8], eax
	;counter 1
	mov dword [ebp-12], -1 
	;counter 2
	mov dword [ebp-16], 2
	;Some Static Variable
	mov dword [ebp-20], 0

forOLoop:
	mov dword [ebp-16], 2
	mov [edi-12], edi
	add edi, 1 
	cmp edi, [ebp-4] ;compare ebx to outerlimit
	jge cleanup ; if less then go to innter loop
forILoop:
	mov [ebp-16], esi ;compare edi to innerlimit
	cmp esi, [ebp-8]
	jle forOLoop ;if greater than go to print
print:
	call complexFunction
	call printf
	sub esi, 1
	jmp forILoop
cleanup:
	xor eax, eax
	leave
	ret

complexFunction:

	;set up the stack frame
	push ebp
	mov ebp, esp
	;allocate space for complex_function_locals
	sub esp, 16 ;4 locals

;CREATE LOCALS STACK
	;point ecx to the top of the stack
	mov ecx, [ebp+16]
	;copy first parameter into eax
	mov eax, [ecx+4]
	;sub the first parameter by 7
	sub eax, 7
	;store
	mov [ebp-4], eax ;store first value in top
	mov [ebp-16], eax ;store same value on bottom
	;point ecx to the top of the stack
	mov ecx, [ebp+16]
	;copy second parameter into eax
	mov eax, [ecx+8]
	;store
	mov [ebp-8], eax
	;multiply
	mov [ebp-4], ecx
	mov [ebp-8], edx
	add ecx, 7
	imul ecx,edx ;CHECK THIS MULTIPLY
	mov [ebp-12], eax ; store third value

	;TEMP1 = [ebp-4] = ARG1 - 7
	;TEMP2 = [ebp-8] = ARG2
	;TEMP3 = [ebp-12] = ARG1 * Arg2
	;retval = [ebp-16] = temp1

;IF AND ELSE STATEMENTS 
	mov eax, [ebp - 8]
	cmp eax, 0
	jl addRet
	mov [ebp-16], eax
	sub eax, 13
	jmp switch
addRet:
	mov [ebp-16], eax
	add eax, 17
	jmp switch
switch:
	mov [ebp-4], ecx ;ecx = arg1
	cmp ecx, 0
	je case0
	cmp ecx, 1
	je case1
	cmp ecx, 2
	je case2
	cmp ecx, 3
	je case3
	jmp case4
case0:
	mov [ebp-8], edx ;edx = temp2
	add eax, edx
	add eax, [ebp-20] ;add SOME STATIC VARIABLE
	add eax, 4
case1:
	sub eax, edx
	add eax, 5
	jmp return
case2:
	sub eax, 13
	jmp return
case3:
	mov [ebp-12], ecx
	mov eax, edx
	imul ecx, 7
	sub eax, [ebp-8]
	add eax, edx
case4:
	add eax, 1
return:
	mov [ebp-20], ecx
	sub ecx, [ebp-4]
	add ecx, eax
	mov ecx, [ebp-20]
	mov esp, ebp
	pop ebp
	ret





