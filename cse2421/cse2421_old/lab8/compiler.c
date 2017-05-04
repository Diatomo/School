#include <stdio>

char cellArr[30000] = {0};
char charaArr[30000] = {0};
char *cell = cellArr[0];
char *chara = charaArr[0];

int main(){
	FILE *fp;
	char byChar;
	fp = fopen("hello.by","r");
        if (fp == NULL){
                printf("File didn't open!");
                exit(EXIT_FAILURE);
        }
	switchCase();
	read();
	write();
	compile(fp);
	
}

/*void switchCase(){
printf("switch:\n
        ;extract value from stack\n
        cmp dword [ecx], 43; + ; increment value where data pointer is\n
        je incValue\n
        cmp dword [ecx], 45; - ; decrement value where data pointer is\n
        je decValue\n
        cmp dword [ecx], 62; > ; increment data pointer\n
        je incDataPtr\n
        cmp dword [ecx], 60; < ; decrement data pointer\n
        je decDataPtr\n
        cmp dword [ecx], 46; . ;output\n
        je outputData\n
        cmp dword [ecx], 44; , ;accept one byte of input\n
        je inputData\n
        cmp dword [ecx], 91; [ ;while where point is at has value\n
        je beginLoop\n
        cmp dword [ecx], 93; ] ;jump back to beg loop if something has value.\n
        je endLoop\n
        jmp read_loop\n

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
inputData:; ,           ;get data from current data cell
        jmp read_loop
beginLoop:; [           ;begin loop   ;decrement address
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
        jmp switch\n")


}*/

void read(void){
printf("
read_byte:\n
        ;create stack\n
        push ebp\n
        mov ebp, esp\n
        ;save registers\n
        ;sub esp, 8\n
        ;mov dword[ebp-4],'0'\n
        push ebx \n
        push esi \n
        push ecx \n
        push edx \n
        ;sub esp, 8\n
        ;mov dword [ebp-4], '0'\n
        ;xor ecx, ecx\n");
}

void readLoop(void){
printf("
read_loop:\n;xor eax, eax ;clear eax\n
        xor ecx, ecx\n 
        mov eax, 3 ;std_read\n
        mov ebx, 0 ;file descriptor stdin\n
        mov ecx, esi\n 
        mov edx, 1 ;byte count\n
        int 0x80 ;system call\n
        ;mov esi, ecx\n
        sub dword esi, 4 ;decrement stack pointer\n
        ;mov edx, [ecx]\n
        cmp dword [ecx], 35 ;compare if at the end of the line\n
        jne switch ;if not equal jump to switch \n
        cmp dword [ecx], 35\n
        je exit_read \n
        ;cleanup\n");
}

void skip(void){
printf("
skip:\n
        mov eax, 3 ; read\n
        mov ebx, 0\n
        mov ecx, esi\n 
        mov edx, 1\n
        int 0x80\n
        sub dword esi, 4\n
        cmp dword [ecx], 35 ;if its a terminating character exit_read\n
        je exit_read\n          
        cmp dword [ecx], 93 ;if its a closing ']' then jmp to read_loop for next char\n
        jne skip\n
        jmp read_loop       ;if no\n
exit_read:\n
        pop edx ;restore edx\n
        pop ecx ;restore ecx\n
        pop esi ;restore esi pointer\n
        pop ebx ;restore ebx\n
        ;add esp, 8 ;cleanup local stack\n
        pop ebp ;restore pointer\n
        ;pop ebp\n
        jmp exit  ;return \n");
	
}

void write(void){
printf("
write_byte:\n
        ;create stack\n
        push ebp\n
        mov ebp, esp\n
        ;save registers\n
        push eax\n
        push ebx\n
        push ecx\n
        push edx\n
        ;write\n
        mov eax, 4 ;sys call write\n
        mov ebx, 1 ;file descriptor (stdout)\n
        mov ecx, edi  ;data to load\n
        mov edx, 1 ;byte size\n
        int 0x80   ;system call\n
\n
        ;clean up\n
        pop edx\n
        pop ecx\n
        pop ebx\n
        pop eax\n
        pop ebp\n
        ret\n");
}



void compile(FILE &fp){
	char byChar;
	while(fscanf(fp,"%c",byChar){
		if (byChar == '+'){
			*cell++;
			printf("inc dword [edi] ;add one to the cell\n");
		}
		else if (byChar == '-') {
			*cell--
			printf("dec dword [edi]\n");

		}
		else if (byChar == '>') {
			cell++;
			printf("sub dword edi, 4 ;sub edi's address");

		}
		else if (byChar == '<') {
			cell--;
			printf("add dword edi, 4\n ;add edi's address");
		}
		else if (byChar == '.') {write()}
		else if (byChar == ',') {read()}
		else if (byChar == '['){
			printf("push ecx\nmov ebx, [edi]\ncmp ebx, 0\nsub dword ecx, 4\n");
		}
		else if (byChar == ']'){
			printf("pop edx\nmov ebx, [edi]\ncmp ebx, 0\njle terminateEndLoop\nmov ecx, edx\n");
		}
		printf("sub dword ecx, 4\n");

		
	}

}

