# Python步步飞升之高级特征

## 1. 前言
Python有句著名的话，叫做"Life is short, you need Python"，人生苦短啊，代码越少，效率越高，这也是我喜欢Python的原因。这篇文章学习一下Python语言的高级特征: Slicing(切片)，Iterable(迭代)，List Comprehensions(列表生成式)，Generator(生成器)和Iterator(迭代器)。 

## 2. Slicing(切片)
Python切片的功能主要用于方便地获取List/Tuple/String等object中元素。
### 2.1 循环生成新list
比如有个List如下，需要获取前3个元素
```
l = ['a','b','c','d','e','f','g']
```
我们可能会有笨方法，用循环来取
```
newL = []
n = 3
for i in range(n):
    newL.append(l[i])
```
### 2.2 List切片
用切片就可以这样简单的获取
```
>>> l[0:3]
['a', 'b', 'c']
>>> l[:3]
['a', 'b', 'c']
>>> l[3:]
['d', 'e', 'f', 'g']
```
l[0:3]的意思是从索引0开始到索引3，不包括索引3。如果第一个索引是0，则可省略；省略第二个索引，代表取到最后一个索引。
### 2.3 Tuple, String切片
对tuple，string同样效果，因为这俩也可以看做一个list
```
>>> t=('a', 'b', 'c')
>>> t[1:3]
('b', 'c')
>>> s='abcdefg'
>>> s[1:3]
'bc'
```
### 2.4 负数索引
索引为负数时，代表倒着取。比如说-1代表最后一个index。
```
>>> l[-1]
'g'
>>> l[-2:-1]
['f']
>>> l[:-2]
['a', 'b', 'c', 'd', 'e']
```
### 2.5 slice类 
Python提供了一个slice类
```
>>> abcObj = slice(0,3)
>>> l[abcObj]
['a', 'b', 'c']
```
### 2.6 简单应用
截取字符串，python中没有类似substring,substr的函数或方法，切片功能可以胜任。
获取s中字符e之后的字符串
```
>>> s
'abcdefg'
>>> s[s.index('e')+1:]
'fg'
```
反转字符串
```
>>> s[::-1]
'gfedcba'
```

## 3. Iterable(迭代)
### 3.1 定义
能够用for来循环的对象，叫做可迭代对象。
比如list,tuple,string
```
>>> s='123'
>>> for i in s:
...     print(i)
...
1
2
3
```
### 3.2 迭代dict
```
>>> d = {'a': 1, 'b': 2}
>>> for k in d:
...     print(k)
...
a
b
>>> for v in d.values():
...     print(v)
...
1
2
>>> for i in d.items():
...     print(i)
...
('a', 1)
('b', 2)
```
### 3.3 判断
可以用collections.Iterable判断是否为可迭代对象
```
>>> from collections import Iterable
>>> isinstance(d, Iterable)
True
>>> isinstance(5, Iterable)
False
```
## 4. List Comprehensions(列表生成式)
### 4.1 定义
Python内置用以创建list的表达式
### 4.2 例子1
比如说有个list
```
l = ['a','b','c']
```
我们要两两有序交互生成一个新的list
```
newL = ['ab', 'ac', 'ba', 'bc', 'ca', 'cb']
```
使用以下方式实现
```
>>> newL = []
>>> for x in l:
...     for y in l:
...         if x!= y:
...             newL.append(x+y)
...
>>> newL
['ab', 'ac', 'ba', 'bc', 'ca', 'cb']
```
使用列表生成式简化
```
>>> newL = [x+y for x in l for y in l if x != y]
>>> newL
['ab', 'ac', 'ba', 'bc', 'ca', 'cb']
```
可以说简单一行，人生苦短啊。
### 4.3 例子2
再比如说，有一个到10的自然数数列，想要计算一个平方的数列
```
>>> l = list(range(10))
>>> l
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> [x*x for x in l]
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
>>> [x*x for x in l if x%2 == 0]
[0, 4, 16, 36, 64]
```

## 5. Generator(生成器)
### 5.1 定义
生成器和list类似，但只有在需要返回下一个数据时它才会计算，而不用如list一样有容量限制，节省空间。
有常见两种方法创建一个生成器：把一个列表生成式的[]改成()和通过用yield替换函数中return实现
### 5.2 把一个列表生成式的[]改成()
例如
```
>>> l = ['a','b','c']
>>> newL = [x+y for x in l for y in l if x != y]
>>> newL
['ab', 'ac', 'ba', 'bc', 'ca', 'cb']
>>> g = (x+y for x in l for y in l if x != y)
>>> g
<generator object <genexpr> at 0x03134130>
```
生成器通过next()函数返回元素
```
>>> next(g)
'ab'
>>> next(g)
'ac'
```
生成器是Iterable，可以用for来循环元素
```
>>> for x in g:
...     print(x)
...
ba
bc
ca
cb
```
### 5.3 通过用yield替换函数中return实现
变成generator的函数，在每次调用next()的时候执行，遇到yield语句返回，再次执行时从上次返回的yield语句处继续执行。
```
>>> def odd():
...     yield 1
...     yield 3
...     yield 5
>>> o = odd()
>>> next(o)
1
>>> next(o)
3
>>> next(o)
5
```

## 6. Iterator(迭代器)
### 6.1 定义
可以被next()函数调用并不断返回下一个值的对象称为迭代器：Iterator。
Iterator的计算是惰性的，只有在需要返回下一个数据时它才会计算。
### 6.2 转变Iterable为Iterator
生成器是迭代器，list是Iterable但不是Iterator。
可以使用iter()函数将Iterable修改为Iterator。
```
>>> from collections import Iterator
>>> l = [1,2,3]
>>> next(l)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'list' object is not an iterator
>>> g = iter(l)
>>> next(g)
1
```
### 6.3 判断对象是否为Iterator
```
>>> isinstance(l, Iterator)
False
>>> isinstance(g, Iterator)
True
```

## 7. 结语
如有疑问，欢迎留言共同探讨。