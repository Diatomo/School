; skeleton.asm
; my required comments
; NAME = CHARLES STEVENSOn
; DATE = 03/05/2016
; CLASS =  CSE 2421, T/TH 5:20PM
; ID: 0x05194445

USE32 ; tell nasm to assemble 32 bit code
global _start ; export the start symbol for our program
_start: ; tell the linker where our program begins

; beginning of program
; my code here
; exit
; functions here
main:
;set up stack frame
push ebp
mov ebp, esp
;declare variables
;mov ecx, eax ; eax is going to be needed for operations so store in edx
sub esp, 8 ; allocate enough room for 3 integers
mov dword [ebp-4], 0 ; declare first variable as 0
mov dword [ebp-8], 0

whileLoop: ;start while loop
call read_integer
mov ecx, eax
mov eax, 2 ; iterator
cmp ecx, 0 ;compare to zero
je exit ;jump if equal and exit the program
cmp ecx, 1
je print_not_prime ; if equal jump to print_not_prime
mov dword [ebp-4], 1 ;set boolean to "true"

;then do some for loop stuff
;mov destination, source
forLoop:
mov edx, eax
imul edx, eax ; multiply eax by edx value stored in eax
cmp edx, ecx
jg skip ; if greater than jump to skip.
mov edx, 0
mov ebx, eax ; copy iterator to divisor
push eax
mov eax, ecx ; copy n to numerator
div ebx ; divide EAX/EBX
pop eax
add eax, 1 ; inc iterator
cmp edx, 0
jne forLoop
mov dword [ebp-4], 0
jmp skip

skip:
cmp dword [ebp-4], 1 ; compare boolean to one
je print_prime ; jump if equal to print_prime
cmp dword [ebp-4], 0 ; compare boolean to zero
je print_not_prime ; jump if equal to print_not_prime
jmp whileLoop ;jump whileLoop

print_not_prime:
; set up stack frame
push ebp ; save the current stack frame
mov ebp, esp ; set up a new stack frame
; save modified registers
push eax ; save eax
push ebx ; save ebx
push ecx ; save ecx
push edx ; save edx
; write not prime to stdout
mov eax, 4 ; syscall 4 (write)
mov ebx, 1 ; file descriptor (stdout)
mov ecx, .not_prime ; pointer to data to load
mov edx, .not_prime.l ; byte count
int 0x80 ; issue system call
; cleanup
pop edx ; restore edx
pop ecx ; restore ecx
pop ebx ; restore ebx
pop eax ; restore eax
pop ebp ; restore ebp
jmp main ; return to caller

.not_prime: db "not prime", 10
.not_prime.l equ $-.not_prime

print_prime:
; set up stack frame
push ebp ; save the current stack frame
mov ebp, esp ; set up a new stack frame
; save modified registers
push eax ; save eax
push ebx ; save ebx
push ecx ; save ecx
push edx ; save edx
; write prime to stdout
mov eax, 4 ; syscall 4 (write)
mov ebx, 1 ; file descriptor (stdout)
mov ecx, .prime ; pointer to data to load
mov edx, .prime.l ; byte count
int 0x80 ; issue system call
; cleanup
pop edx ; restore edx
pop ecx ; restore ecx
pop ebx ; restore ebx
pop eax ; restore eax
pop ebp ; restore ebp
jmp main ; return to caller

.prime: db "prime", 10
.prime.l equ $-.prime

read_integer:
; set up stack frame
push ebp ; save the current stack frame
mov ebp, esp ; set up a new stack frame
; set up local variables
sub esp, 8 ; allocate space for two local ints
mov dword [ebp-4], '0' ; digit: initialize to '0'
mov dword [ebp-8], 0 ; value: initialize to 0
; save modified registers
push ebx ; save ebx
push ecx ; save ecx
push edx ; save edx
.read_loop:
; update number calculation
mov eax, 10 ; load multiplier
mul dword [ebp-8] ; multiply current value by 10, store in eax
add eax, [ebp-4] ; add new digit to current value
sub eax, '0' ; convert digit character to numerical equivalent
mov [ebp-8], eax ; save new value
; read in digit from user
mov eax, 3 ; syscall 3 (read)
mov ebx, 0 ; file descriptor (stdin)
lea ecx, [ebp-4] ; pointer to data to save to
mov edx, 1 ; byte count
int 0x80 ; issue system call
; loop until enter is pressed
cmp dword [ebp-4], 10 ; check if end of line reached
jne .read_loop ; if not, continue reading digits
; cleanup
mov eax, [ebp-8] ; save final value in eax
pop edx ; restore edx
pop ecx ; restore ecx
pop ebx ; restore ebx
add esp, 8 ; free local variables
pop ebp ; restore ebp
ret ; return to caller

exit:
mov ebx,0
mov eax,1
int 80h
