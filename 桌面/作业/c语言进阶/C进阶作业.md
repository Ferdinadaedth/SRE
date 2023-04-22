作业完成后将**程序源码**，**运行实例**，**作业过程记录（写成md）**，**打包后**发送至：**hhan@redrock.team**

格式为**学号+名字**（2021212735黄子迅）

# C进阶作业

#### Level1:

编写c程序，利用不同类型指针的特性，实现下面这个函数:

```c
void bitSwap(unsigned int x);
//它的作用是交换一个int数据的高位和低位。
//在注释解释input和output这么交换的原因。
//示例：
-->input  :0x1234ABCD
-->output :0xCDAB3412
```

#### Level2:

编写c程序，将一个n×n矩阵转置。

**只能用指针操作，禁止使用数组**

```c
//示例：
-->input   :
1 2 3
4 5 6
7 8 9
-->output  :
1 4 7 
2 5 8 
3 6 9
```

#### Level3:

写一个makefile文件，编译下方给出的链接中的所有文件

> 请尽可能的编写出最简洁的makefile文件

链接：https://pan.baidu.com/s/1feRvH68dsckyJBUekOufxw?pwd=j91t 
提取码：j91t 
--来自百度网盘超级会员V5的分享

#### Level4:

实现十进制数字到任意进制的转换函数:

```c++
void baseConverter(int dec,int base);
//其中base为转换的基数
//示例：
-->input   :250, 16
-->output  :FA
```

#### Level5（选做（对二进制感兴趣推荐做））:

尝试从下列伪代码中恢复结构体：

```c
_DWORD *ptr;
char *v3 = (char *)0xdeadbeef;
char *v4 = (char *)0x11223344;
int size = 0x40;
int number = 0xfa;
void *v10 = 0x7fff123000;

ptr = malloc(0x28uLL);
*(_QWORD *)ptr = v3;
ptr[1] = size;
*((_QWORD *)ptr + 2) = v4;
ptr[6] = number;
*((_QWORD *)ptr + 4) = v10;
```

```c
_DWORD 4字节
_QWORD 8字节
```

恢复后的结构体格式为:

*结构体中的命名与伪代码中定义的变量名保持一致*

```c
struct ptr
{
	double v3;
    int v4;
    char *v5;
    ...
    ...
}ptr;
```



