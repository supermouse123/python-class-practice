# @Time    : 2020/1/18
# @Author  : sunyingqiang
# @Email   : 344670075@qq.com

print('<[100]> evalsupport start')

def deco_alpha(cls):
    print('<[200]> deco_alpha')
    def inner_1(self):
        print('<[300]> deco_alpha:inner_1')

    cls.method_y = inner_1
    return cls

class MetaAleph(type):
    print('<[400]> MetaAleph body')

    def __init__(cls, name, bases, dic):
        print('<[500]> MetaAleph init')

        def inner_2(self):
            print('<[600]> MetaAleph init:inner_2')
        cls.method_z = inner_2
print('<[700]> MetaAleph end')