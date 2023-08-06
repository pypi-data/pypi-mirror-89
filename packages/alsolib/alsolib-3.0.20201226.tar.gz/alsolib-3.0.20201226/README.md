
# alsolib v3.0
alsolib开发者：苦逼者钟宇轩

说明:本库为原创库，火焰工作室精心打造

这是库介绍，大家可以破解看看里面的内容

版权所有，侵权必究

###alsolib库说明介绍：

### alsolib 一个最重要的功能
想知道是谁在看你的学而思作品吗?
他来了~
```python
from alsolib.xes import
a=getnowuser()
print(a) #获取当前观看者 若没登陆则返回 ["Error","None","None"]
```

内置函数 导入方式：

```python
from alsolib import *
```
### 百度百科

```python
a=baidubaike("***")
print(a)
```
### 翻译

```python
a=translate("Hello") 
print(a)
```
### 天气

```python
a=getweather("guangdong","guangzhou")#省，市的英文
print(a)
```

### 内置网页浏览器 title为自定义标题

```python
a=getweather("http://www.asunc.cn/","title")#一定要加http://或https://
print(a)
```

### alsolib 学而思库
导入方式
```python
from alsolib.xes import
a=LoadWork("一个作品的pid")
```


### 学而思获取作品赞

```python
b=a.get_likes()
print(b)
```

### 学而思获取作品作者

```python
b=a.get_user()
print(b)
```

### 学而思获取作品踩的数量

```python
b=a.get_unlikes()
print(b)
```

### 学而思获取作品介绍

```python
b=a.get_description()
print(b)
```

### 学而思获取作者信息

```python
b=a.get_name_as_pid()
print(b)
```

### 学而思获取你对这个作品点赞没有~

```python
while 1:
    b=a.is_like()
    if b==0:
	print("你点赞了")
    if b==-1:
	print("你踩了")
    if b==1:
	print("你没点赞也没踩")
```

剩下还有两个库 alsolib.api 和 alsoqq 自己探索吧~

