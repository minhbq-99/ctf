flow của chương trình

```
 v12 = *MK_FP(__GS__, 20);
  v10 = 0;
  memset(numbers, 0, 0x400u);
  point = 0;
  memcpy(s, "123456789ABCDEFabcdef", 22u);
  alarm(30u);
  v3 = time(0);
  srand(v3);
  setvbuf(stdout, 0, 2, 0);
  v4 = READFILE("/home/winner/intro.txt");
  puts(v4);
  choose((int **)numbers);
  printf("Thank you! Let's see the winning numbers...\n");
  sleep(3u);
  puts(".");
  for ( i = 0; i < 4; ++i )
  {
    v5 = rand();
    point += numbers[s[v5 % strlen(s)]] << 10;
  }
  printf("You won: $%d\n", point);
  result = v10;
  if ( *MK_FP(__GS__, 20) == v12 )
    result = v10;
  return result;
  ```
  
  pseudocode của ida thiếu một đoạn này
  ```
  lea     eax, aYouWonD
  mov     ecx, [ebp+point]
  mov     [esp], eax      ; format
  mov     [esp+4], ecx
  call    _printf
  cmp     [ebp+point], 0
  mov     [ebp+var_484], eax
  jnb     loc_8048B5A
  lea     eax, aHomeWinnerFlag ; "/home/winner/flag"
  mov     [esp], eax      ; filename
  call    READFILE
  mov     [esp], eax      ; s
  call    _puts
  mov     [ebp+var_488], eax
  ```
  
  hàm choose  
  ```
  void __cdecl choose(int **n)
{
  char c; // [sp+Fh] [bp-9h]@3
  int i; // [sp+10h] [bp-8h]@1

  i = 0;
  printf("Please choose winning numbers [1-9a-f] (type 0 if you're done)\n");
  while ( i < 256 )
  {
    c = getchar();
    if ( c == '0' )
      break;
    n[c] = (int *)((char *)n[c] + 1);
    ++i;
  }
}
```
  
  - Thời gian bắt đầu : 7h30 ngày 17/9  
  - Các bước thực hiện:  
    + Coi các string trong binary => thấy có chỗ đọc flag   
    + Checksec:
  ```
  Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
  ```
  => Không thể dùng shellcode, có thể overwrite GOT  
    + Kiểm tra giả thiết và viết exploit code  
  
  - Các giả thiết ban đầu 
    + buffer overflow  
    + index không được kiểm tra  
      * sửa biến point để get flag  
      * overwrite GOT  
      * overwrite ret addr của main  
      * overwrite ret addr của choose  
  
  - Sau khi debug, xem kỹ binary:    
    + không thấy buffer overflow  
    + sửa biến point cũng không thể get được flag vì lúc nào nó cũng jump tới loc_8048B5A dù point là bao nhiêu, cái bẫy làm tốn nhiều thời gian  
       ```
         cmp     [ebp+point], 0
         jnb     loc_8048B5A
       ```
    + không thể overwrite GOT vì quá xa stack  
    + có thể overwrite ret addr của main nhưng không thể điều khiển để nó chỉ về main + xxx (chỗ get flag)  
    + có thể overwrite ret addr của choose và chỉ nó về chỗ get flag [solve.py](./solve.py)  
   
  - Thời gian kết thúc: 9h30 ngày 17/9

  
