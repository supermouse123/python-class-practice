# @Time    : 2021/1/11
# @Author  : sunyingqiang
# @Email   : 344670075@qq.com


import abc


class AutoStorage:
    """描述符类：主要作用存储对象，对象在赋值的时候进行字段验证等操作"""
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(prefix, index)   #防止递归取值和赋值所以起一个别名
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)


class Validated(abc.ABC, AutoStorage):
    """字段验证抽象类"""
    def __set__(self, instance, value):
        value = self.validate(instance, value)
        super(Validated, self).__set__(instance, value)

    @abc.abstractmethod
    def validate(self, instance, value):
        """return validated value or raise ValueError"""
        pass


class Quantity(Validated):
    """a number greater than zero"""

    def validate(self, instance, value):
        if value <= 0:
            raise ValueError('value must be > 0')
        return value


class NonBlank(Validated):
    """a string with at leastone non-space character"""

    def validate(self, instance, value):
        value = value.strip()
        if len(value) == 0:
            raise ValueError('value cannot be empty or blank')
        return value


class LineItem:
    description = NonBlank()  #用来验证description字段不能为空
    weight = Quantity()       #用来验证字段不能为负数
    price = Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price