# Python步步飞升之collections.defaultdict

## 1. 前言
Python内置四种基本container：list, dict, set, tuple，collections模块为其补充。defaultdict为collections中一个容器。一言以蔽之，是为有默认值的dict.
## 2.  一个官方例子
s为一个list，其中包含了5个tuple，我们的目标是生成d这样的dict统计颜色对应值列表。
```
    s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
    d=[('blue', [2, 4]), ('red', [1]), ('yellow', [1, 3])]
```
一般来说，我们会这样的想法：新建一个dict，循环s写入到d的值(list)中
```
    d = dict()
    for k,v in s:
        d[k].append(v)
    print(d)
```
然后收到以下错误
```
Traceback (most recent call last):
    d[k].append(v)
KeyError: 'yellow'
```
原因是d中没有为'yellow'的key，引用失败。
## 3. 改进一下，先为d赋予默认的key
当k不在d中存在时，赋值一个初始list，值为v
```
s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
d = dict()
for k, v in s:
    if k in d:
        d[k].append(v)
    else:
        d[k] = [v]
print(d)
````
运行结果
```
{'yellow': [1, 3], 'blue': [2, 4], 'red': [1]}
```
## 4. 使用dict的setdefault方法
[setdefault方法](https://www.w3schools.com/python/ref_dictionary_setdefault.asp)可以给指定key设置默认值。
```
s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
d = dict()
for k, v in s:
    if k in d:
        d[k].append(v)
    else:
        d.setdefault(k, [v])
print(d)
```
## 5. Life is short, you need Python
[collections.defaultdict](https://docs.python.org/2/library/collections.html#collections.defaultdict)为dict子类，提供一个拥有默认值的dict。defaultdict参数为一个callable对象，能不接受参数返回一个值，比如list, 比如一个不带参数的function。
```
from collections import defaultdict
s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
d = defaultdict(list)
for k, v in s:
    d[k].append(v)
print(d)
```
或者用一个不带参数的function
```
d = defaultdict(lambda : list())
或者
d = defaultdict(lambda : [])
```
运行结果
```
defaultdict(<class 'list'>, {'yellow': [1, 3], 'blue': [2, 4], 'red': [1]})
```
## 6. 结语
如有疑问，欢迎留言共同探讨。