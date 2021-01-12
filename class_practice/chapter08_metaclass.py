# @Time    : 2021/1/12
# @Author  : sunyingqiang
# @Email   : 344670075@qq.com

"""
导入时和运行时的区别
导入时会运行全部顶层代码
对于函数：解释器不会执行函数的定义体，在导入时定义顶层函数，运行时执行函数的定义体
对于类：解释器会执行每个类的定义体，甚至执行嵌套类，结果定义类的属性和方法，并构建类对象
"""
import pickle


def record_factory(cls_name, field_names):
    """类工厂函数(类似于namedtuple类)可详细查看namedtuple源码"""
    try:
        field_names = field_names.replace(',', ' ').split()
    except AttributeError:
        pass
    field_names = tuple(field_names)

    def __init__(self, *args, **kwargs):
        attrs = dict(zip(self.__slots__, args))
        attrs.update(kwargs)
        for name, value in attrs.items():
            setattr(self, name, value)

    def __iter__(self):
        for name in self.__slots__:
            yield getattr(self, name)

    def __repr__(self):
        values = ','.join('{}={!r}'.format(*i) for i in zip(self.__slots__, self))
        return '{}({})'.format(self.__class__.__name__, values)

    cls_attrs = dict(__slots__=field_names,
                     __init__=__init__,
                     __iter__=__iter__,
                     __repr__=__repr__)
    res = type(cls_name, (object,), cls_attrs)
    # res.__module__ = '__main__'   #默认实现__module__方法,不实现这个方法没法被序列化
    return res

Dog = record_factory('Dog', 'name weight owner')
rex = Dog('Rex', 30, 'Bob')
print(pickle.dumps(rex))
# print(rex.name)
# print(rex.weight)
# print(rex)