

;lab8.asm
;Author = Charles C Stevenson
;Date = 11/22/2016


section .data
; the global array "message" stores 128 bytes, initialized to 0,
; and can be accessed through the "message" label.
message: times 128 db 0

section .text
USE32

global _start
_start:
main:
  call decode_message
  call print_message
  jmp exit

get_bit:
  ;setup stack frame
  push ebp
  mov ebp, esp

  call read_character;get bit
  sub eax, 48 ;48 is the decimal ascii for 0

  ;cleanup
  leave
  ret

get_byte:
  ;setup stack frame
  push ebp
  mov ebp, esp
  push ecx
  push ebx
  push edx

  xor edx, edx ;edx is the shifter
  xor ebx, ebx
  xor ecx, ecx
  mov dword edx, 0
  mov dword ebx, 8 ;limit of loop
  mov dword ecx, 0 ;iterator

get_byte_loop: ; for loop
  call get_bit
  or edx, eax ;copy values into edx
  inc ecx
  cmp ecx, ebx
  je get_byte_loop_exit
  shl edx, 0x1 ;shift bits left
  jmp get_byte_loop

;cleanup
get_byte_loop_exit:
  mov eax, edx
  pop edx
  pop ebx
  pop ecx
  leave
  ret

decode_message:
  ;setup stack frame
  push ebp
  mov ebp, esp
  push ecx
  xor ecx, ecx

decode_message_loop:
  call get_byte;get a byte
  mov dword [message+edx*4], eax;move into message array
  inc edx
  cmp eax, ecx;if its all zeroes
  jne decode_message_loop;terminate

  ;cleanup
  pop ecx
  leave
  ret

print_message:
  ;setup stack frame
  push ebp
  mov ebp, esp
  push ecx
  push ebx
  xor edi, edi
  xor ecx, ecx
  xor ebx, ebx

print_message_loop:
  sub esp, 0x4
  mov dword ebx, [message+ecx*4]
  push ebx
  call print_character
  add esp, 0x4
  inc ecx
  cmp ecx, edx
  jne print_message_loop

  ;cleanup
  pop ebx
  pop ecx
  leave
  ret

print_character:
  ;set up stack frame
  push ebp ;save the current stack frame
  mov ebp, esp ;set up a new stack frame
  push ebx ;save ebx
  push ecx
  push edx

  ;print character to stdout
  mov eax, 4 ;syscall 4 (write)
  mov ebx, 1 ;file descriptor (stdout)
  lea ecx, [ebp+8] ;pointer to data to write
  mov edx, 1 ;byte count
  int 0x80 ;issue system call

  ;cleanup
  pop edx
  pop ecx
  pop ebx ;restore ebx
  leave ;restore ebp and stack
  ret ;return to caller

read_character:
  ;setup stack frame
  push ebp ;save the current stack frame
  mov ebp, esp ;set up a new stack frame
  sub esp, 4 ;allocate space for one local int
  push ebx ;save ebx
  push ecx
  push edx

  ;read character
  mov eax, 3 ;syscall 3 (read)
  mov ebx, 0 ;file descriptor (stdin)
  lea ecx, [ebp-4] ;pointer to data to save to
  mov edx, 1 ;byte count
  int 0x80 ;issue system call

  ;cleanup
  mov eax, [ebp-4] ;save final value in eax
  pop edx
  pop ecx ; restore ecx
  pop ebx ;restore ebx
  add esp, 4 ;free local variables
  leave ;restore ebp and stack
  ret ;return to caller


exit:
  mov ebx, 0
  mov eax, 1
  int 80h
