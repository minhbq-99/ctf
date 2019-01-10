flow của chương trình  

```
int __cdecl main()
{
  unsigned int v0; // eax@1
  const char *v1; // eax@1
  ssize_t v2; // eax@10
  char nptr; // [sp+78h] [bp-550h]@2
  unsigned int v5; // [sp+80h] [bp-548h]@1
  unsigned int v6; // [sp+84h] [bp-544h]@1
  unsigned int i; // [sp+88h] [bp-540h]@1
  void *s; // [sp+8Ch] [bp-53Ch]@1
  char v9[1320]; // [sp+90h] [bp-538h]@1
  unsigned int v10; // [sp+5B8h] [bp-10h]@1
  int v11; // [sp+5BCh] [bp-Ch]@1

  v11 = 0;
  v0 = time(0);
  srand(v0);
  alarm(30u);
  v10 = rand() % 6 + 5;
  s = v9;
  i = 0;
  v6 = 0;
  v5 = 0;
  setvbuf(stdout, 0, 2, 0);
  v1 = (const char *)sub_80487B0("/home/c0ffee/intro.txt");
  puts(v1);
  printf("Hi sir! Welcome to 0xC0FFEE SHOP v1.1\n");
  while ( 1 )
  {
    printf("How many cups, sir?\ncups> ");
    __isoc99_scanf("%08s%*c", &nptr);
    v6 = atoi(&nptr);
    if ( v6 <= v10 )
      break;
    printf("No way, sir. There is a long queue, please take %d cups at once. Thank you for your understanding.\n", v10);
  }
  do
  {
    if ( v5 >= v10 )
      break;
    menu();
    printf("what is your name, sir? then I can write it on the cup.\nsize> ");
    __isoc99_scanf("%08s%*c", &nptr);
    v6 = atoi(&nptr);
    if ( !v6 || v6 > 128 )
    {
      puts("Sorry sir, what's wrong with your name?! are you trying to hack us? I'm calling police now.");
      exit(-1);
    }
    memset(s, 0, 128u);
    for ( i = 0; i < v6; i += v2 )
      v2 = read(0, (char *)s + i, v6 - i);
    *((_BYTE *)s + i) = 0;
    printf("Which one, sir?\n>> ");
    __isoc99_scanf("%08s%*c", &nptr);
    v6 = atoi(&nptr);
    *((_DWORD *)s + 32) = v6;
    ++v5;
    s = (char *)s + 132;
    printf("anything else, sir?\n> ");
    __isoc99_scanf("%08s%*c", &nptr);
  }
  while ( !strcmp(&nptr, "yes") );
  puts("Thank you so much, sir!\n...bling bling $$$\n...ching ching $$$\n\nHere is your receipt: ");
  for ( i = 0; i < v5; ++i )
    printf("%16s | %03d\n", &v9[132 * i], *(_DWORD *)&v9[132 * i + 128]);
  return v11;
}
```

Các bước thực hiện:  
   -  xem thử các string trong binary thấy không có chỗ gọi shell hay đọc flag sẵn
   -  checksec:
   ```
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
   ```
      +  Không có stack canary => buffer overflow  
      +  Không thể chèn shellcode  
      +  Có thể overwrite GOT  
      
   -  chạy thử binary, flow chương trình khá khó hiểu, nghi ngờ có overflow chỗ nhập tên => cho chuỗi dài vào nhưng không thấy crash  
   -  bật ida lên đọc binary  
   -  xác định thêm giả thiết debug thử => thất bại  
   -  cảm nhận thấy lỗi off by one từ việc đọc binary ```__isoc99_scanf("%08s%*c", &nptr);``` nhưng không biết để làm gì, rồi bỏ qua  
   -  chạy binary nhập tên với chuỗi dài => không crash như lúc đầu nhưng để ý thấy không in ra receipt => đọc kỹ lại binary => confirm lỗi off by one => dùng nó để overflow  
   
Các giả thiết:  
   -  overflow chỗ nhập tên => không thể được vì có chỗ  
   ```
   if ( v5 >= v10 )
      break;
   ```
   -  chỗ read tên vào có vẻ lạ, dùng ``` read(0, (char *)s, v6); ``` là được rồi mà ??? => search về read, debug thử => bế tắc  
   -  chạy thử binary thấy lạ, nhìn ra off by one có thể dùng để overwrite v5 thành 0 qua đó bypass cái check ở trên => overflow  
   
Timeline:
   -  0:00 - 1:15 : chạy thử binary, đọc binary
   -  1:15 - 1:45 : coi cái chỗ read, debug, chạy binary, quan sát kỹ output
   -  1:45 - 2:00 : thấy chỗ khả nghi ở output kết hợp đọc binary thấy lỗi
   -  2:00 - 2:25 : viết exploit code
   
   
   
