# Python步步飞升之collections.deque

## 1. 前言
Python内置四种基本container：list, dict, set, tuple，collections模块为其补充。deque为collections中一个容器。一言以蔽之，是为双端队列.

## 2. deque定义
deque发音为“deck”，是“double-ended queue”的缩写，意为“双端队列”，用于生成堆和队列。
deque提供线程安全的，有效利用内存的 **append** 和 **pop** 方法可以从队列前后两个方向操作数据，时间复杂度为O(1)。
list也拥有类似的操作方法 **pop(0)** 和 **insert(0, value)**, 但是效率没有deque高，时间复杂度为O(n)，因为操作之后list的长度和所有元素下标都要做修改。 
```
class collections.deque([iterable[, maxlen]])
```
从iterable中拿去数据，从左到右初始化这些数据，通过自身 **append()** 方法添加数据，最终生成ddeque实例;
当iterable没有提供，即生成一个空deque;
**maxlen** 代表dqeue元素最大长度。
```
>>> d = deque([1,2,3,4]);
>>> d
deque([1, 2, 3, 4])
>>> d = deque([1,2,3,4],3); 
>>> d
deque([2, 3, 4], maxlen=3) # 指定最大长度为3，则append(4)的时候挤掉元素“1”
```

## 3. Mark一些该类常用方法和特点

### 3.1 append(x)和appendleft(x)
后和前添加元素，如果超出maxlen会挤掉相反方向元素
```
>>> d
deque([2, 3, 4], maxlen=3)
>>> d.append(5)
>>> d
deque([3, 4, 5], maxlen=3)
>>> d.appendleft(2)
>>> d
deque([2, 3, 4], maxlen=3)
```

### 3.2 extend(iterable)和extendleft(iterable)
后和前添加iterable中元素
```
>>> d
deque([1, 2])
>>> d.extend([3,4])
>>> d
deque([1, 2, 3, 4])
>>> d.extendleft([-1,0])
>>> d
deque([0, -1, 1, 2, 3, 4]
```

### 3.3 insert(i, x)
在i位置插入x元素，如果超出maxlen，会抛出“IndexError”
```
>>> d
deque([0, -1, 1, 2, 3, 4])
>>> d.insert(0, -2)
>>> d
deque([-2, 0, -1, 1, 2, 3, 4])
>>> d
deque([1, 2, 3], maxlen=3)
>>> d.insert(0, 0)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: deque already at its maximum size
```

### 3.4 pop()和popleft()
后和前删除元素，如果没有元素，会抛出“IndexError”
```
>>> d = deque([1,2,3], 3)
>>> d.pop()
3
>>> d
deque([1, 2], maxlen=3)
>>> d.popleft()
1
>>> d
deque([2], maxlen=3)
>>> d.pop()
2
>>> d
deque([], maxlen=3)
>>> d.pop()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: pop from an empty deque
```

### 3.5 remove(value)
删除指定值的第一个元素，如果没有找到，会抛出“IndexError”
```
>>> d = deque('1223')
>>> d
deque(['1', '2', '2', '3'])
>>> d.remove('2')
>>> d
deque(['1', '2', '3'])
>>> d.remove('5')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: deque.remove(x): x not in deque
```

### 3.6 reverse()
反deque中元素原顺序
```
>>> d
deque(['1', '2', '3'])
>>> d.reverse()
>>> d
deque(['3', '2', '1'])
```

### 3.7 rotate(n)
旋转n个位置，n为负则向左旋转。
```
>>> d
deque(['3', '2', '1'])
>>> d.rotate(1)
>>> d
deque(['1', '3', '2'])
>>> d.rotate(-1)
>>> d
deque(['3', '2', '1'])
```

### 3.8 maxlen属性
返回deque的maxlen属性值
```
>>> d
deque(['3', '2', '1'])
>>> d.maxlen
>>> d = deque([1,2], 3)
>>> d.maxlen
3
```

## 4. 简单应用
从文件中读取最后N行数据，类似于linux的“tail”命令
```
def tail(filename, n=10):
    '文件中读取最后N行数据'
    with open(filename) as f:
        return deque(f, n)
>>> dq = tail('C:\\Users\\kigao\\Documents\\employee.csv', 1);
>>> dq
deque(['Danna,16,CFO,Finance Dept\n'], maxlen=1)
```
其中employee.csv文件内容为
```
Kian,18,CEO,R&D Dept
Danna,16,CFO,Finance Dept
```

## 5. 结语
如有疑问，欢迎留言共同探讨。
