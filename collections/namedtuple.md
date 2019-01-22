# 1. 前言
Python内置四种基本container：list, dict, set, tuple，collections模块为其补充。namedtuple为collections中一个容器。一言以蔽之，是为有属性名字的tuple.

# 2. 简单说明
```
collections.namedtuple(typename, field_names, verbose=False, rename=False)
```
生成一个新的名为typename的tuple子类，属性名称由field_names指定。详细介绍参见[Python官方文档](https://docs.python.org/3.5/library/collections.html#collections.namedtuple)。

# 3.  简单例子
```
from collections import namedtuple

P = namedtuple('Point', ['x', 'y'])
p = P(1,2)
print(p)
print(p.x)
print(p[0])
```
运行结果
```
Point(x=1, y=2)
1
1
```
本身tuple作为一个只读list，只能通过位置进行访问，如p[0]。使用namedtuple之后可以采用属性名称的方式进行访问，增大了可读性，带来了方便。

# 4. Mark一些该类常用方法和属性
-  **_make(iterable)**
  从sequence或iterable中生成一个新的实例
  ```
  P = namedtuple('Point', ['x', 'y'])
  t = [11, 22]
  print(P._make(t))
  ````
  运行结果
  ```
  Point(x=11, y=22)
  ```
- **_asdict()**
按照属性名生成一个OrderedDict实例
```
  P = namedtuple('Point', ['x', 'y'])
  t = [11, 22]
  print(P._make(t)._asdict())
  ````
  运行结果
```
  OrderedDict([('x', 11), ('y', 22)])
```
- **_replace(**kwargs)**
替换相应属性值后生成一个新的namedtuple实例
```
  P = namedtuple('Point', ['x', 'y'])
  t = [11, 22]
  print(P._make(t)._replace(x=22))
````
  运行结果
  ```
  Point(x=22, y=22)
  ```
- **_fields**
以tuple形式返回实例的属性
```
  P = namedtuple('Point', ['x', 'y'])
  t = [11, 22]
  print(P._make(t)._replace(x=22)._fields)
````
  运行结果
```
  ('x', 'y')
```

# 5. 使用场景：从csv文件中读取数据
employee.csv内容如下
```
Kian,18,CEO,R&D Dept
Danna,16,CFO,Finance Dept
```
python读取代码
```
import csv
from collections import namedtuple

EmployeeRecord = namedtuple(
    'EmployeeRecord', 'name, age, title, department')

for emp in map(EmployeeRecord._make, csv.reader(open('C:\\Users\\kian\\Documents\\Python\\employee.csv', 'r'))):
        print(emp.name, emp.title)
```
运行结果
```
Kian CEO
Danna CFO
```
#6. 结语
如有疑问，欢迎留言共同探讨。