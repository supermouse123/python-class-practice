# @Time    : 2021/1/11
# @Author  : sunyingqiang
# @Email   : 344670075@qq.com

# class Quantity:
#     """属性描述符类"""
#
#     def __init__(self, storage_name):
#         self.storage_name = storage_name
#
#     def __set__(self, instance, value):
#         if value > 0:
#             # setattr(instance, self.storage_name, value)
#             instance.__dict__[self.storage_name] = value    #防止给weight和price赋值出现无限递归的调用__set__方法
#         else:
#             raise ValueError('value must be > 0')
#
# class LineItem:
#     weight = Quantity('weight')
#     price = Quantity('price')
#
#     def __init__(self, description, weight, price):
#         self.description = description   #调用LineItem的set方法
#         self.weight = weight      #会调用Quantity的set方法
#         self.price = price
#
#     def subtotal(self):
#         return self.weight * self.price
#
# truffle = LineItem('wHITE TRUFFLE', 100, 1)

class Quantity:
    _counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls._counter
        self.storage_name = '_{}{}'.format(prefix, index)
        cls._counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        if value > 0:
            # print(self.storage_name)
            setattr(instance, self.storage_name, value)   #把weight和price的变量名称修改防止重复调用__set__方法
        else:
            raise ValueError('value must be > 0')


class LineItem:
    weight = Quantity()        #描述符类似于django的model.CharFiled()
    price = Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

truffle = LineItem('wHITE TRUFFLE', 100, 1)

print(truffle.weight)
# print(truffle._Quantity0)   #防止重复调用__set__方法所以给weight起别名
print(LineItem.weight)
print(truffle.weight)