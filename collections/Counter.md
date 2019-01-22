# Python步步飞升之collections.Counter

## 1. 前言
Python内置四种基本container：list, dict, set, tuple，collections模块为其补充。Counter为collections中一个容器。一言以蔽之，是为计数器.

## 2. 从一个简单例子说起
有一个list
```
l = ['red', 'blue', 'red', 'green', 'blue', 'blue']
```
现在需要统计下各个颜色出现的次数，用一个循环实现
```
from collections import defaultdict

l = ['red', 'blue', 'red', 'green', 'blue', 'blue']
counter = defaultdict(int)
for i in l:
    counter[i] += 1
print(counter)
```
运行结果
```
defaultdict(<class 'int'>, {'red': 2, 'blue': 3, 'green': 1})
```
这里用到了以前讲述到的(defaultdict)[https://github.com/Kianhit/python-bbfeisheng/blob/master/collections/defaultdict.md]。

## 3. Life is short, you need Python
现在有了collections.Counter工具，我们可以更加便利的实现这点
```
from collections import Counter

l = ['red', 'blue', 'red', 'green', 'blue', 'blue']
counter = Counter(l)
print(counter)
```
运行结果
```
Counter({'blue': 3, 'red': 2, 'green': 1})
```

## 4. Counter简单介绍
```
class collections.Counter([iterable-or-mapping])
```
Counter是dict的一个子类，构造函数接受iterable或者mapping，用以计数。
例举创建Counter的方法
```
c = Counter() # 空Counter
c = Counter('gallahad') # 从iterable创建
c = Counter({'red': 4, 'blue': 2}) # 从mapping创建
c = Counter(cats=4, dogs=8) # 以关键字参数创建
```

## 5. Mark一些该类常用方法和特点

### 5.1 Counter不会遇到*KeyError*异常
```
>>> c = Counter()
>>> print(c['a'])
0
```

### 5.2 Counter值可为零和负数
```
>>> c = Counter({'a': 1, 'b': -1, 'c': 0})
>>> c['b']
-1
>>> c['c']
0
```

### 5.3 Counter支持“加减或与”运算
```
>>> c = Counter(a=3, b=1)
>>> d = Counter(a=1, b=2)
>>> c + d                       # 两个counter对应值相加:  c[x] + d[x]
Counter({'a': 4, 'b': 3})
>>> c - d                       # 两个counter对应值相减 (只保留正数值)
Counter({'a': 2})
>>> c & d                       # 与运算，取最小值:  min(c[x], d[x]) 
Counter({'a': 1, 'b': 1})
>>> c | d                       # 或运算，取最大值:  max(c[x], d[x])
Counter({'a': 3, 'b': 2})
```
其中一元加减操作表示被加减一个空Counter
```
>>> c = Counter(a=2, b=-4)
>>> +c
Counter({'a': 2})
>>> c = Counter(a=2, b=-4)
>>> -c
Counter({'b': 4})
```
所以刚好可以使用*+c*用来去除Counter中非正数值

### 5.4 elements()
以任意顺序返回Counter中key，个数为value值的迭代器。
```
>>> c = Counter('askdlsajpdsadlsa')
>>> print(c)
Counter({'a': 4, 's': 4, 'd': 3, 'l': 2, 'k': 1, 'j': 1, 'p': 1})
>>> list(c.elements())
['a', 'a', 'a', 'a', 's', 's', 's', 's', 'k', 'd', 'd', 'd', 'l', 'l', 'j', 'p']
>>> list(sorted(c.elements()))
['a', 'a', 'a', 'a', 'd', 'd', 'd', 'j', 'k', 'l', 'l', 'p', 's', 's', 's', 's']
```

### 5.5 most_common([n])
返回次数最高的N个mapping组成的list
```
>>> Counter('askdlsajpdsadlsa').most_common(3)
[('a', 4), ('s', 4), ('d', 3)]
```
当n未输入时返回所有，按照次数高低排序
```
>>> Counter('askdlsajpdsadlsa').most_common()
[('a', 4), ('s', 4), ('d', 3), ('l', 2), ('k', 1), ('j', 1), ('p', 1)]
```
那么可以简单的获得次数最低的的3个mapping组成的list
```
>>> Counter('askdlsajpdsadlsa').most_common()[:-4:-1]
[('p', 1), ('j', 1), ('k', 1)]
```

## 6. 结语
如有疑问，欢迎留言共同探讨。