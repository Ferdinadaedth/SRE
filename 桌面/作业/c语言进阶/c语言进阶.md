# Level1 

```  c
#include<stdio.h>
int i;
void bitSwap(unsigned int x)
{
	char* p = (char*)&i;//将int型指针转换成char型指针
	char t = p[0];
	p[0] = p[3];
	p[3] = t;
	t = p[1];
	p[1] = p[2];
	p[2] = t;//通过中间变量将int类型高低字节位交换
}
int main()
{
	scanf("%X", &i);
	bitSwap(i);
	printf("0x%X\n", i);
	return 0;

}
```

![](D:\Edc\OneDrive\桌面\作业\c语言进阶\level1.png)

 # Level2  

```  c
#include <stdio.h>
#include <stdlib.h>
void a(int* p, int n)
{
    int i, j;

    for (i = 0;i < n;i++)
    {
        for (j = 0;j < n;j++)
        {
            scanf("%d", p + n * i + j);
        }
    }
}

void b(int* p, int* q,int n)
{
    int i, j;
    for (i = 0;i < n;i++)
    {
        for (j = 0;j < n;j++)
        {
            *(q + n* i + j) = *(p + n* j + i);
        }
    }

}
void c(int* q,int n)
{
    int i, j;
    for (i = 0;i < n;i++)
    {
        for (j = 0;j < n;j++)
        {
            printf("%d ", *(q + n * i + j));
        }
        printf("\n");
    }
}

int main()
{
    int n;
    int* p = NULL;
    int* q = NULL;
    scanf("%d", &n);
    p = (int*)malloc(n * n * sizeof(int));
    q = (int*)malloc(n * n * sizeof(int));
    if (p != NULL)
    {
        a(p, n);
        if (q != NULL)
        {
            b(p, q, n);
         c(q, n);
        }
    }
    return 0;
}
```

![](D:\Edc\OneDrive\桌面\作业\c语言进阶\level2.png)

# Level3

```  shell
.PHONY:main 
objects=main.o pre.o lcm.o gcd.o talk.o
main:$(objects)
        gcc -o main $(objects) 
main.o: pre.h gcd.h lcm.h talk.h
lcm.O:lcm.h talk.h gcd.h 
gcd.o:gcd.h talk.h
talk.o:talk.h
pre.o:pre.h
    
clean: 
        rm *.o

```

![](D:\Edc\OneDrive\桌面\作业\c语言进阶\level3.png)

# Level4

```  c
#include<stdio.h>
#include<string.h>
int x, y;
void change(int dev, int base)
{
    if (dev)
    {
        change(dev / base, base);
        if ((dev%base) <= 9)
        {
            printf("%d", dev % base);
        }
        else
        {
            printf("%c", (dev % base) - 10 + 'A');
        }
    }
}
int main()
{
    while (scanf("%d%d", &x, &y) != EOF)
    {
        if (x < 0)
        {
            printf("-");
            x = -x;
        }
        change(x, y);
    }
    return 0;
}
```

![](D:\Edc\OneDrive\桌面\作业\c语言进阶\Level4.png)
