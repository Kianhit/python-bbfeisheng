# 1. 前言
Python内置四种基本container：list, dict, set, tuple，collections模块为其补充。OrderedDict为collections中一个容器。一言以蔽之，是为记住插入顺序的dict.

# 2. 简单说明
```
class collections.OrderedDict([items])
```
OrderedDict是dict子类，支持dict所有方法，记住了插入key的顺序。如果新条目覆盖现有条目，则原始插入位置保持不变。 删除条目并重新插入它将使其移至最后。详细介绍参见[Python官方文档](https://docs.python.org/3.7/library/collections.html#collections.OrderedDict)。
因为是有序的，所以只有当顺序也相同的时候，两个OrderedDict才相同。但是OrderedDict和普通dict相比较时，会忽略顺序。
```
from collections import OrderedDict

d = {'banana': 3, 'apple': 4}
od1 = OrderedDict({'banana': 3, 'apple': 4})
od2 = OrderedDict({'apple': 4, 'banana': 3})
print(od1 == od2)
print(od1 == d)
```
运行结果
```
False
True
```
# 3. 关键方法
## OrderedDict.popitem(last=True)
  普通dict的该方法不接受参数，只能将最后一个条目删除；OrderedDict比dict更为灵活，接受一个last参数：当last=True时和普通方法一样，符合LIFO顺序；当last=False时候，删除第一个元素，符合FIFO顺序。
```
from collections import OrderedDict

od1 = OrderedDict({'banana': 3, 'apple': 4})
od1.popitem(False)
print(od1)
```
运行结果
```
OrderedDict([('apple', 4)])
```
# 4. 简单增强
OrderedDict只是保持了插入的顺序，当条目被修改时，顺序不会修改。
```
od1 = OrderedDict({'banana': 3, 'apple': 4})
od1['banana'] = 5
print(od1)
```
运行结果
```
OrderedDict([('banana', 5), ('apple', 4)])
```
但是有时候我们需要修改和插入时同样的效果，可以简单的增强一下，重写*\_\_setitem__()*方法当修改时先删除该元素然后再插入。
```
class EnhancedOrderedDict(OrderedDict):

    def __setitem__(self, key, value):
        if key in self:
            del self[key]
        OrderedDict.__setitem__(self, key, value)
```
测试
```
eod = EnhancedOrderedDict({'banana': 3, 'apple': 4})
print(eod)
eod['banana'] = 5
print(eod)
````
运行结果
```
EnhancedOrderedDict([('banana', 3), ('apple', 4)])
EnhancedOrderedDict([('apple', 4), ('banana', 5)])
```
#5. 结语
如有疑问，欢迎留言共同探讨。