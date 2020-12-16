# @Time    : 2020/12/16
# @Author  : sunyingqiang
# @Email   : 344670075@qq.com

from array import array
import reprlib
import math
import numbers
import operator
import functools
import itertools


class Vector:
    typecode = 'd'
    shortcut_names = 'xyzt'

    def __init__(self, components):
        self._components = array(self.typecode, components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return 'Vector({})'.format(components)

    def __str__(self):
        """返回值必须是字符串"""
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) + bytes(self._components))

    def __eq__(self, other):
        """判断两个对象是否相等"""
        #方式一：
        # return tuple(self) == tuple(other)

        #方式二：
        # if len(self) != len(other):
        #     return False
        # for a, b in zip(self, other):   #把self和other对象封装成一个迭代器相当于(('a', 'a'), ('b', 'f'))
        #     if a != b:                  #元组拆包判断是否相等
        #         return False
        # return True

        #方式三：
        return len(self) == len(other) and all(a == b for a, b in zip(self, other))

    def __hash__(self):
        """相当于给每一位hash异或"""
        hashes = (hash(x) for x in self._components)  #使用迭代器提升效率节省空间，也可使用map函数
        return functools.reduce(operator.xor, hashes, 0)  # 按位异或， 如果序列为空设置初始值为0

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))

    def __bool__(self):
        return bool(abs(self))

    def __len__(self):
        return len(self._components)

    def __getitem__(self, item):
        """把切片完的类型转化成类对象的类型"""
        cls = type(self)  #获取实例所属的类
        # print(cls([1, 2]))  #重新创建类对象
        if isinstance(item, slice):
            return cls(self._components[item])  #转化成类对象
        elif isinstance(item, numbers.Integral):
            return self._components[item]
        else:
            msg = '{cls.__name__} indices must be integers'
            return TypeError(msg.format(cls=cls))
        # return self._components[item]

    def __getattr__(self, item):
        """根据字母所在字符串位置找到列表里指定元素"""
        cls = type(self)
        if len(item) == 1:
            pos = cls.shortcut_names.find(item)
            if 0 <= pos < len(self._components):
                return self._components[pos]
        msg = '{.__name__!r} object has no attribute {!r}'
        raise AttributeError(msg.format(cls, item))

    def __setattr__(self, key, value):
        """设置重新赋值的规定不能和shortcut_names重复防止冲突"""
        cls = type(self)
        if len(key) == 1:
            if key in cls.shortcut_names:
                error = 'readonly attribute {attr_name!r}'
            elif key.islower():
                error = "can't set attributes 'a' to 'z in {cls_name!r}"
            else:
                error = ''
            if error:
                msg = error.format(cls_name=cls.__name__, attr_name=key)
                raise AttributeError(msg)
        super(Vector, self).__setattr__(key, value)   #父类默认实现这个方法调用原来的set方法

    def angle(self, n):
        """计算某个角的坐标"""
        r = math.sqrt(sum(x * x for x in self[n:]))
        a = math.atan2(r, self[n-1])
        if (n == len(self) - 1) and (self[-1] < 0):
            return math.pi * 2 - a
        else:
            return a

    def angles(self):
        """创建生成器按需计算所有角的坐标"""
        return (self.angle(n) for n in range(1, len(self)))

    def __format__(self, format_spec=''):
        if format_spec.endswith('h'):
            format_spec = format_spec[:-1]
            coords = itertools.chain([abs(self)], self.angles())
            outer_fmt = '<{}>'
        else:
            coords = self
            outer_fmt = '({})'
        components = (format(c, format_spec) for c in coords)
        return outer_fmt.format(', '.join(components))


    @classmethod
    def frombytes(cls, octets):
        """把二进制形式转成类对象的形式"""
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)  #把byte类型转成数组
        return cls(memv)


v = Vector([3, 4, 5, 6])
print(v)
# for i in v:
#     print(i)
# print(bytes(v))
# print(v.frombytes(b'd\x00\x00\x00\x00\x00\x00\x08@\x00\x00\x00\x00\x00\x00\x10@\x00\x00\x00\x00\x00\x00\x14@\x00\x00\x00\x00\x00\x00\x18@'))
# print(abs(v))
# print(bool(v), bool(Vector([0, 0])))
# # print(v.b)
# v.B = 10
# print(v.B)
# print(v)
# print(len(v))
# print(v[0])
# print(v[0: 3])
# print(type(v[0: 3]))
# print(format(v, 'h'))
