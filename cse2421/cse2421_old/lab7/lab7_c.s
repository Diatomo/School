	.file	"lab7_c.c"
	.local	some_static_int
	.comm	some_static_int,4,4
	.text
	.globl	complex_function
	.type	complex_function, @function
complex_function:
.LFB0:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movl	%edi, -20(%rbp)
	movl	%esi, -24(%rbp)
	movl	-20(%rbp), %eax
	subl	$7, %eax
	movl	%eax, -12(%rbp)
	movl	-24(%rbp), %eax
	movl	%eax, -8(%rbp)
	movl	-20(%rbp), %eax
	imull	-24(%rbp), %eax
	movl	%eax, -4(%rbp)
	movl	-12(%rbp), %eax
	movl	%eax, -16(%rbp)
	cmpl	$0, -8(%rbp)
	jns	.L2
	addl	$17, -16(%rbp)
	jmp	.L3
.L2:
	subl	$13, -16(%rbp)
.L3:
	movl	-20(%rbp), %eax
	cmpl	$1, %eax
	je	.L5
	cmpl	$1, %eax
	jg	.L6
	testl	%eax, %eax
	je	.L7
	jmp	.L4
.L6:
	cmpl	$2, %eax
	je	.L8
	cmpl	$3, %eax
	je	.L9
	jmp	.L4
.L7:
	movl	-8(%rbp), %eax
	movl	-16(%rbp), %edx
	addl	%eax, %edx
	movl	some_static_int(%rip), %eax
	addl	%edx, %eax
	addl	$4, %eax
	movl	%eax, -16(%rbp)
.L5:
	movl	-8(%rbp), %eax
	movl	-16(%rbp), %edx
	subl	%eax, %edx
	movl	%edx, %eax
	addl	$5, %eax
	movl	%eax, -16(%rbp)
	jmp	.L10
.L8:
	movl	-16(%rbp), %eax
	leal	-13(%rax), %edx
	movl	some_static_int(%rip), %eax
	subl	%eax, %edx
	movl	%edx, %eax
	movl	%eax, -16(%rbp)
	jmp	.L10
.L9:
	movl	-4(%rbp), %edx
	movl	%edx, %eax
	sall	$3, %eax
	subl	%edx, %eax
	movl	%eax, %edx
	movl	-16(%rbp), %eax
	addl	%edx, %eax
	subl	-8(%rbp), %eax
	movl	%eax, -16(%rbp)
.L4:
	addl	$1, -16(%rbp)
	nop
.L10:
	movl	some_static_int(%rip), %eax
	subl	-20(%rbp), %eax
	movl	%eax, %edx
	movl	-16(%rbp), %eax
	addl	%edx, %eax
	movl	%eax, some_static_int(%rip)
	movl	-16(%rbp), %eax
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.size	complex_function, .-complex_function
	.section	.rodata
.LC0:
	.string	"(%d, %d): %d\n"
	.text
	.globl	main
	.type	main, @function
main:
.LFB1:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$32, %rsp
	movl	%edi, -20(%rbp)
	movq	%rsi, -32(%rbp)
	movq	-32(%rbp), %rax
	addq	$8, %rax
	movq	(%rax), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	atoi
	movl	%eax, -8(%rbp)
	movq	-32(%rbp), %rax
	addq	$16, %rax
	movq	(%rax), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	atoi
	movl	%eax, -4(%rbp)
	movl	$0, -16(%rbp)
	jmp	.L13
.L16:
	movl	$2, -12(%rbp)
	jmp	.L14
.L15:
	movl	-12(%rbp), %edx
	movl	-16(%rbp), %eax
	movl	%edx, %esi
	movl	%eax, %edi
	call	complex_function
	movl	%eax, %ecx
	movl	-12(%rbp), %edx
	movl	-16(%rbp), %eax
	movl	%eax, %esi
	movl	$.LC0, %edi
	movl	$0, %eax
	call	printf
	subl	$1, -12(%rbp)
.L14:
	movl	-12(%rbp), %eax
	cmpl	-4(%rbp), %eax
	jg	.L15
	addl	$1, -16(%rbp)
.L13:
	movl	-16(%rbp), %eax
	cmpl	-8(%rbp), %eax
	jl	.L16
	movl	$0, %eax
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1:
	.size	main, .-main
	.ident	"GCC: (Ubuntu 4.8.4-2ubuntu1~14.04.1) 4.8.4"
	.section	.note.GNU-stack,"",@progbits
