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
section .data
var_s dd 0
.case_zero: db "CASE ZERO", 10
.case_zero.l equ $-.case_zero
.case_one: db "CASE ONE", 10
.case_one.l equ $-.case_one
.case_two: db "CASE TWO", 10
.case_two.l equ $-.case_two
.case_three: db "CASE THREE", 10
.case_three.l equ $-.case_three
.case_default: db "CASE DEFAULT = ", 10
.case_default.l equ $.case_default


main:
	;set up the stack frame
	push ebp
	mov ebp, esp
	;allocate space for mains local variables
	sub esp, 16 ; 5 locals

  ;make room for first parameter call to atoi
	;point ecx to the top of the stack
	mov ecx, [ebp+16]
	;copy first parameter to eax
	mov eax, [ebp+12]
  add eax, 4
  mov eax, [eax]
	;set[esp] to eax
	mov [esp], eax
	call atoi
	;restore
	add esp, 4
	;store
	mov [ebp-4], eax ; outlimit = ebp-4
	;make room for second parameter call to atoi
	sub esp, 4
	;point ecx to the top of the stack
	mov eax, [ebp+16]
  mov eax, dword [ebp+12]
  add eax, 8
  mov eax, [eax]
	;copy second parameter to eax
	;mov eax, [ebx+8]
	;set [esp] to eax
	mov [esp], eax
	call atoi
	;restore
	add esp, 4
	;store
	mov [ebp-8], eax ; inner limit = ebp-8

  ;[ebp-4] = outer limit
  ;[ebp-8] = inner limit
  ;[ebp-12] = counter 1
  ;[ebp-16] = counter 2


initLoop:
	mov dword [ebp-12], 0 ; counter 1
outerLoop:
  mov dword ecx, [ebp-12]
	cmp dword ecx, [ebp-4] ;compare counter 1 to outer limit
	jge cleanup ; if less then go to innter loop
	mov dword [ebp-16], 2 ; counter 2
forILoop:
  mov dword ecx, [ebp-16]
	cmp dword ecx, [ebp-8]
	jle outerLoop ;if greater than go to print
print:
	call complexFunction
  mov ecx, eax
  mov eax, format_string_1
  mov [esp], eax
	call printf
  sub dword [ebp-16], -1
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
	mov ecx, [ebp+16];point ecx to the top of the stack
	mov eax, [ecx+4] ;ARG 1
	sub eax, 7
	mov [ebp-4], eax ;TEMP 1
	mov [ebp-16], eax ;RETVAL
	mov ecx, [ebp+16]
	mov eax, [ecx+8] ;ARG 2
	mov [ebp-8], eax ;TEMP 2
  mov eax, [ebp+4]
	imul dword eax, [ebp+8] ;CHECK THIS MULTIPLY
	mov [ebp-12], eax ; TEMP 3

	;TEMP1 = [ebp-4] = TEMP 1
	;TEMP2 = [ebp-8] = TEMP 2
	;TEMP3 = [ebp-12] = TEMP 3
	;retval = [ebp-16] = RETVAL

;IF AND ELSE STATEMENTS
	mov edx, [ebp+4]; arg1
	cmp edx, 0
	jl addRet
	mov [ebp-16], edx
	sub dword[ebp-16], 13
	jmp switch
addRet:
	mov [ebp-16], eax
	add dword [ebp-16], 17
switch:      ;SWITCH ARG1
	cmp edx, 0
	je case0
	cmp edx, 1
	je case1
	cmp edx, 2
	je case2
	cmp edx, 3
	je case3
	jmp case4
case0:
	add dword [ebp-16], 4
  mov dword ecx, [ebp-16]
  add dword ecx, [ebp-8]
	add eax, var_s ;add SOME STATIC VARIABLE
  jmp return
case1:
  mov dword ecx, [ebp-16]
	sub dword ecx, [ebp-8]
  add dword [ebp-16], 5
	jmp return
case2:
	sub dword [ebp-16], 13
  sub dword [ebp-16], var_s
	jmp return
case3:
  mov dword eax, [ebp-12]
	imul dword eax, 7
	sub eax, [ebp-8]
  add [ebp-16], eax
	jmp return
case4:
	add dword [ebp-16], 1
return:
  xor ecx, ecx
  add edx, [ebp-16]
 ; mov dword ecx, var_s
	sub [var_s], edx
;  mov dword var_s, ecx
	mov dword eax, [ebp-16] ;SET RETURN VALUE (retval)
	mov esp, ebp
	pop ebp
  leave
	ret





