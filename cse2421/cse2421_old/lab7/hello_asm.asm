;
; this is hello_asm.asm, a simple hello-world like program to demonstrate some core ideas
;
; export the symbol "main"
global main
; indicate that printf will be an extern that will have to be resolved at link time
extern printf
extern atoi

; the read-only data segment
section .rodata
; note, must place the ascii value of \n (0xa) as a byte after our format string instead of making format string "%d\n"
format_string_1 db "%d",0xa,0

; the read-write data segment
section .data
; initialize the static variable var_s to 30
var_s dd 0x0000001e

; libc (which we linked to) has already established the stack for us, so there
; isn't anything more to do but implement main

; the code (text) segment
section .text
; the 'main' function
main:
  ; set up the main function's stack frame
  push ebp
  mov ebp, esp
  ; set aside space for main's two local variables (int var_x, and int var_y)
  sub esp, 12

  ; implement int var_x = atoi(argv[1])
  ; set aside room for the one parameter on the stack for the first call to atoi
  ;sub esp, 0x4
  ; the array argv will be found in the location of the first argument placed on the stack for this function to consume
  mov ecx, [ebp+0xc]
  ; the first argument to the executable, a pointer to a character assumed to represent a legal integer, can be found 4 bytes offset from where eax points
  ; the second argument to the executable, 
;   a pointer to a character assumed to represent a legal integer, 
;  can be found 8 bytes offset from where eax points
  ; move the first argument onto the stack in preparation for calling atoi
  mov eax, [ecx+4]
  mov [esp], eax
  call atoi
  ; restore the stack to its original state
  add esp, 0x4
  ; eax has our integer value of var_x that we can now store
  mov [ebp-0x4], eax

  ; implement int var_y = atoi(argv[2]) just as above, but adjusted for the other offset
  sub esp, 0x4
  mov ecx, [ebp+0xc]
  mov eax, [ecx+8]
  mov [esp], eax
  call atoi
  add esp, 0x4
  mov [ebp-0x8], eax

  ; set aside room for two parameters on the stack for the first call to printf
  sub esp, 0x8
  ; copy var_x into eax to prepare for the math operation
  mov eax, dword [ebp-0x4]
  ; add the value of var_s to the copy of var_x held in eax
  add eax, [var_s]
  ; place the result of the computation var_x + var_s onto the stack for the first call to printf
  mov [esp+0x4], eax
  ; move the address of the format string into eax and place it onto the proper place on the stack for the second call to printf
  mov eax, format_string_1
  mov [esp], eax
  ; call printf
  call printf
  ; reset the stack to its state before the first call to printf
  add esp, 0x8
  ; set aside room for the two parameters on the stack for the second call to printf
  sub esp, 0x8
  ; copy var_y into eax to prepare for the math operation
  mov eax, dword [ebp-0x8]
  ; add the value of var_s to the copy of var_y held in eax
  add eax, [var_s]
  ; place the result of the computation var_y += var_s onto the stack for the second call to printf
  mov [esp+0x4], eax
  ; move the address of the format string into eax and place it onto the proper place on the stack for the second call to printf
  mov eax, format_string_1
  mov [esp], eax
  ; call printf
  call printf
  ; reset the stack to its state before the second call to printf
  add esp, 0x8
  ; set eax to zero to return success to the caller of main()
  xor eax, eax
  ; we didn't need to do any callee-saves because we only used caller saves registers eax, edx, ecx, so nothing to restore
  ; restore the stack frame for the caller
  leave
  ; and return
  ret
