# Python步步飞升之随机数random

## 1. 概览
[random](https://docs.python.org/3.7/library/random.html)模块是Python的伪随机数([wikipedia伪随机性](https://zh.wikipedia.org/wiki/%E4%BC%AA%E9%9A%8F%E6%9C%BA%E6%80%A7))生成器模块。

## 2. 随机小数
```
>>> random.random()
0.913099783896878
>>> random.uniform(0,10)
0.6890067446514497
```

## 3. 随机整数
```
# 随机一个大于等于0且小于等于10的整数
>>> random.randint(0,10)
5
# 随机一个>=1且<=10之间的奇数，其中2表示递增基数
>>> random.randrange(1,10,2)
5
```

## 4. 随机返回序列元素
```
>>> random.choice('abcde')
'b'
>>> random.choice(['a','b','c','5'])
'5'
>>> random.choice(['a','b','c','5'])
'b'
>>> random.choice(string.ascii_letters)
'Z'
>>> random.choice(string.ascii_letters)
'm'
# 从序列中返回指定个数随机元素的新序列
>>> random.sample(string.ascii_letters,1)
['l']
>>> random.sample(string.ascii_letters,2)
['O', 'c']
>>> random.sample(string.ascii_letters,3)
['M', 'H', 'T']
```

## 5. 随机打乱序列元素顺序
```
>>> l = [1,2,3,4,5]
>>> random.shuffle(l)
>>> l
[1, 4, 3, 5, 2]
```

## 6. 生成指定长度数字和大写字母组成随机数
```
def generate_nonce(n):
    """
    随机获取n位数字和大写字母组合成字符串作为nonce
    """
    return ''.join(random.sample(string.ascii_uppercase + string.digits, n))
>>> generate_nonce(10)
'V87J2WM9AQ'
```

## 7. 结语
如有疑问，欢迎留言共同探讨。