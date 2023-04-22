# Level 0  

* 第一个程序在第一行打印出111，在第二行打印出222，最后一行为空行    

  > 过程：首先第一个if括号中的表达式为真，执行打印程序并换行，继续第二个if括号中表达式依然为真，继续执行打印程序并换行

* 第二个程序在在第一行打印出111，第二行为空行    

  > 过程：首先第一个if括号中的表达式为真，执行打印程序并换行，然后直接跳过else if语句函数终止执行

  # Level1 

  ~~~c
  ```
   #include <stdio.h>
  int main()
  {
  	int i, j;
  	for (i = 0;i <= 8;i++)
  	{
  		for (j = 1;j <= 9-i;j++)
  		{
  			printf("*");
  		}
  		printf("\n");
  	 }
  }
  
  ~~~

  	# Level2  

  ```  c
  #include<stdio.h>  
  void compare(int a[])
  {
  	int i, t, j;
  	for (i=1; i<=10; i++) 
  	{
  		for (j = 1; j <= 9 - i; j++)  
  		{
  			if (a[j] < a[j + 1])
  			{
  				t = a[j];
  				a[j] = a[j + 1];
  				a[j + 1] = t;
  			}
  		}
  	}
  }
  int main()
  {
  	int a[11];
  	int i;
  	for (i = 1;i <=10;i++)
  	{
  		scanf("%d", &a[i]);
  	}
  	compare(a);
  	for (i = 1;i <= 10;i++)
  	{
  		printf("%d ", a[i]);
  	}
  	return 0;
  }
  
  ```

  

  # Level3  

  ```  c
  #include<stdio.h>  
  int main()
  {
  	int a[4][4], i,j,sum1=0,sum2=0;
  	for (i = 1;i <= 3;i++)
  	{
  		for (j = 1;j <= 3;j++)
  		{
  			scanf("%d", &a[i][j]);
  		}
  	}
  	for (i = 1;i <= 3;i++)
  	{
  		sum1 += a[i][i];
  		sum2 += a[i][4 - i];
  	}
  	printf("主对角线和为%d 副对角线和为%d", sum1,sum2);
  }
  
  ```

  # Level4  

  ```  c
  #include <stdio.h>
  #include <math.h>
  int main()
  {
  	int i,a,c;
  	int sum = 1;
  	scanf("%d", &a);
  	for (i = 1;i <= a;i++)
  	{
  		c = sqrt(2 * i);
  		sum = sum + floor(c);
  		if (i % 3 == 0)
  		{
  			sum = sum -2 ;
  		}
  	}
  	printf("%d", sum);
  	return 0;
  }
  
  
  ```
  
  
