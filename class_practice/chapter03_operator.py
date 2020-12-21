# @Time    : 2020/12/21
# @Author  : sunyingqiang
# @Email   : 344670075@qq.com

import math
import itertools
import numbers


class Test:

    def __init__(self, list_num):
        self.list_num = list_num

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))

    def __iter__(self):
        return iter(self.list_num)

    def __neg__(self):
        return Test(-x for x in self)

    def __pos__(self):
        return Test(self)

    def __add__(self, other):
        """让类可以使用加法"""
        try:
            pairs = itertools.zip_longest(self, other, fillvalue=0.0)
            return Test(a + b for a, b in pairs)
        except TypeError:
            return NotImplemented

    def __radd__(self, other):
        """让类被动使用加法"""
        return self + other

    def __mul__(self, other):
        if isinstance(other, numbers.Real):
            return Test(n * other for n in self)
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self * other

    def __str__(self):
        return str(list(self))

    def __iadd__(self, other):
        """用于加等于在原对象上执行"""
        return self + other


t = Test([4, 2])
print(t)
print(abs(t))
print(-t)
print(+t)
t2 = Test([1, 2])
a = t+t2
print(t+(1, 3))
print((1, 3)+t)  #test不是tuple类型不能彼此相加, tuple的__add__方法不支持然后检查test有没有__radd__方法
print(t * 10)
print(10 * t)

print(id(t))
t += [1, 2]
print(t)
print(id(t))
