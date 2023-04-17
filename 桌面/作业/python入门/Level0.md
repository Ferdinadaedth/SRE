# Level0  

```  
print("hallo world" )
```

# Level1  

```  python
# -*- coding: gbk -*-
import random
n=1  
a=0  
b=0  
c=0
while n<=5:  
   person = input('石头(0)、剪刀(1)、布(2)：')
   person = int(person)
   computer = random.randint(0, 2)
   if person == computer:

      print('平局')  
      c+=1
   elif person == 0 and computer == 1 or person == 1 and computer == 2 or person == 2 and computer == 0:

      print('你赢了')  
      a+=1  
      if a>=3:  
          print('玩家取得胜利')  
          break
   else:
      print('你输了')  
      b+=1  
      if b>=3:  
          print('电脑取得胜利')  
          break
   n+=1  
   if n==6:  
       n=0  
       a=0  
       b=0  
       print('未分出胜负重新开始')

```

# Level2    

mod.py

```  python
def beautiful(str):
    print(str + " is beautiful")  
```

test.py  

```  python
from mod import beautiful  
beautiful('python')
```

# # Level3

搞不来，靠网上的理解了点

```  python

import requests
import re
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'

class WeatherSpider:


    def getSource(self):
 
        url = 'http://www.weather.com.cn/weather/101040100.shtml'
        resp = requests.get(url,headers=headers)
        # print(resp.content.decode('utf-8'))
        return resp.content.decode('utf-8')

```



