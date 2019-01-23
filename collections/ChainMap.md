# Python步步飞升之collections.ChainMap

## 1. 前言
Python内置四种基本container：list, dict, set, tuple，collections模块为其补充。[ChainMap](https://docs.python.org/3.5/library/collections.html?highlight=collections#collections.ChainMap)为collections中一个容器, Python 3才添加的。一言以蔽之，是为可以把很多dict链接起来.
## 2.  ChainMap定义
```
class collections.ChainMap(*maps)
```
ChainMap接收map关系建立新的object。
假设我们有2个dict
```
a = {'a': 1, 'b': 2}
b = {'c': 3}
```
我们想要合并生成新的字典, 可能会这样做
```
>>> for x in b:
...     a[x] = b[x]
...
>>> a
{'a': 1, 'b': 2, 'c': 3}
```
我们有个更快的方法就是使用ChainMap，避免update
```
>>> c = ChainMap(a, b)
>>> c
ChainMap({'a': 1, 'b': 2}, {'c': 3})
```
## 3. ChainMap读取和更新
ChainMap内部存储了一个名为maps的list用以维护mapping关系, 这个list可以直接查看和修改，修改之后相应ChainMap值也就修改了
```
>>> c.maps
[{'a': 1, 'b': 1}, {'b': 2}]
>>> c.maps[0]['a'] = 2
>>> c
ChainMap({'a': 2, 'b': 1}, {'b': 2})
>>> c.maps[1]['b'] = 3
>>> c
ChainMap({'a': 2, 'b': 1}, {'b': 3})
```
如果不是修改这个list，我们对ChainMap的修改只会影响第一个map，读取的时候会从第一个map开始读，直到遇到指定的key
```
>>> c
ChainMap({'a': 2, 'b': 1}, {'b': 3})
>>> c['b'] = 4
>>> c
ChainMap({'a': 2, 'b': 4}, {'b': 3})
>>> c['b']
4
```

## 4. Mark一些该类方法和属性

### 4.1 new_child(m=None)
生成一个新的ChainMap, m指定mappings作为第一个mapping，后面跟着原先的mappings
```
>>> c
ChainMap({'a': 1, 'b': 1}, {'b': 2})
>>> c.new_child()
ChainMap({}, {'a': 1, 'b': 1}, {'b': 2})
>>> c.new_child({'d': 0})
ChainMap({'d': 0}, {'a': 1, 'b': 1}, {'b': 2})
```

### 4.2 parents属性
返回父ChainMap，由除了第一个map之后的其它mappings组成
```
>>> d
ChainMap({'d': 0}, {'a': 1, 'b': 1}, {'b': 2})
>>> d.parents
ChainMap({'a': 1, 'b': 1}, {'b': 2})
```

### 4.3 maps属性
上面提到过的用以存储mappings的可更新list
```
>>> d.maps
[{'d': 0}, {'a': 1, 'b': 1}, {'b': 2}]
```

## 5. 简单应用
一个Python命令中，如果在命令行中输入参数则使用该参数，没有则从OS环境变量中获取，如果还没有再取自定义默认值
```
import os
import argparse
from collections import ChainMap


defaults = {'color': 'red', 'user': 'guest'}

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--user')
parser.add_argument('-c', '--color')
namespace = parser.parse_args()
command_line_args = {k: v for k, v in vars(namespace).items() if v}

combined = ChainMap(command_line_args, os.environ, defaults)

print(combined['color'])
print(combined['user'])
```
运行测试
```
PS C:\Users\kigao\Documents\code\python-bbfeisheng> python .\collections\note_ChainMap.py -c Black -u Kian
Black
Kian
PS C:\Users\kigao\Documents\code\python-bbfeisheng> python .\collections\note_ChainMap.py
red
guest
```
## 6. 结语
如有疑问，欢迎留言共同探讨。