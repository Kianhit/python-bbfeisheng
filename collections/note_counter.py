from collections import Counter
from collections import defaultdict

l = ['red', 'blue', 'red', 'green', 'blue', 'blue']
counter = defaultdict(int)
for i in l:
    counter[i] += 1
print(counter)

counter = Counter(l)
print(counter)

c = Counter()
print(c['a'])

c = Counter('gallahad')
c = Counter(a=4, b=2, c=0, d=-2)
print(+c)

c = Counter('askdlsajpdsadlsa')
print(c)
print(list(c.elements()))
print(sorted(c.elements()))
print(c.most_common(3))
print(list(c))
print(c.items())
d = dict(c)
print(set(c))
print(Counter('askdlsajpdsadlsa').most_common(3))
print(c.most_common())
print(c.most_common()[:-4:-1])