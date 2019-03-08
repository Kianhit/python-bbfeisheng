# Python步步飞升之变量和常量

文章比较杂乱，想起相关的就记录一下。

## 变量
这个和数学中变量定义没啥区别，只是能为任意类型。借百度百科的话:
> 变量来源于数学，是计算机语言中能储存计算结果或能表示值抽象概念。变量可以通过变量名访问。

## 变量建立
Python中变量定义
```
变量名 = 值
```
因为Python为动态语言，变量类型是不固定的，不用指定变量类型。
```
>>> a = 1
>>> type(a)
<class 'int'>
>>> a = 'x'
>>> type(a)
<class 'str'>
```
**type()**函数返回变量的类型
与动态语言对应的就是静态语言，比如Java，新建变量时需要指定变量类型且不能更改。
```
int a = 3;
```

## 变量在内存中
比如
```
x = 'abc'
```
这里Python解释器在内存中创建了'abc'字符串和一个名为x的变量，然后将'abc'地址指向x。
```
>>> x = 'abc'
>>> id(x)
10281600
>>> y = x
>>> id(y)
10281600
```
**id()**函数查看变量内容地址，可以看到变量x和变量y是指向同一个地址。

## is和==
这里python中有两个操作符
- is: 比较值是否相等
- ==: 比较引用是否相等
比如
```
>>> x = 'abcd'
>>> y = 'abcd'
>>> x is y
True
```
字符串变量存储的其实是内存地址，所以“x is y”为真。
```
>>> x = 1000
>>> id(x)
2544224
>>> y = 1000
>>> id(y)
2547168
>>> x == y
True
>>> x is y
False
```
可以看到虽然x和y值均为1000，但是他们却指向不同的地址，所以“x is y”为假。
但是，
```
>>> x = 256
>>> y = 256
>>> x is y
True
>>> x = 257
>>> y = 257
>>> x is y
False
```
这是因为Python实现的时候缓存了-5到256的整数，详情见[“is” operator behaves unexpectedly with integers](https://stackoverflow.com/questions/306313/is-operator-behaves-unexpectedly-with-integers)。
> The current implementation keeps an array of integer objects for all integers between -5 and 256, when you create an int in that range you actually just get back a reference to the existing object. So it should be possible to change the value of 1. I suspect the behaviour of Python in this case is undefined. :-)

## 常量
常量就是不变的变量，Python中通常用全部大写的变量名表示常量，但这只是一个习惯上的用法，其实也是可以修改的。

## 命名规则
数字，字母，下划线，任意组合，数字不能开头，python 的关键字不能用，变量名尽量有意义。

Python语言编码没有具体的风格，常见两种风格规范：
- [官方PEP风格](https://www.python.org/dev/peps/)
- [Google Python 风格指南](https://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/contents/)

摘抄一些命名约定

- 所谓”内部(Internal)”表示仅模块内可用, 或者, 在类内是保护或私有的.
- 用单下划线(_)开头表示模块变量或函数是protected的(使用from module import *时不会包含).
- 用双下划线(__)开头的实例变量或方法表示类内私有.
- 将相关的类和顶级函数放在同一个模块里. 不像Java, 没必要限制一个类一个模块.
- 对类名使用大写字母开头的单词(如CapWords, 即Pascal风格), 但是模块名应该用小写加下划线的方式(如lower_with_under.py). 尽管已经有很多现存模块使用类似于CapWords.py这样的命名, 但现在已经不鼓励这样做, 因为如果模块名碰巧和类名一致, 这会让人困扰.

Python之父Guido推荐的规范
Type|    Public | Internal
---|:--:|---:
Modules| lower_with_under |   _lower_with_under
Packages|    lower_with_under     
Classes| CapWords  |  _CapWords
Exceptions|  CapWords   |  
Functions|   lower_with_under()  |_lower_with_under()
Global/Class Constants  |CAPS_WITH_UNDER |_CAPS_WITH_UNDER
Global/Class Variables  |lower_with_under  |  _lower_with_under
Instance Variables  |lower_with_under  |  _lower_with_under (protected) or __lower_with_under (private)
Method Names   | lower_with_under() | _lower_with_under() (protected) or __lower_with_under() (private)
Function/Method Parameters | lower_with_under     
Local Variables |lower_with_under    

## Python除法
- "/"除法计算结果是浮点数，是精确的除法
```
>>> 5/2
2.5
>>> 4/2
2.0
>>> 10/3
3.3333333333333335
```
- "//"除法，又叫做“地板除”，两个整数的除法仍然是整数，只取结果的整数部分
```
>>> 5//2
2
>>> 4//2
2
>>> 10//3
3
```