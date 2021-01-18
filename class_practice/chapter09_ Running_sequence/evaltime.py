# @Time    : 2020/1/18
# @Author  : sunyingqiang
# @Email   : 344670075@qq.com

from evalsupport import deco_alpha

print('<[1]> evaltime module start')

class ClassOne:
    print('<[2] ClassOne body>')

    def __init__(self):
        print('<[3] ClassOne init>')

    def __del__(self):
        print('<[4] ClassOne del>')         #全部程序运行之后会调用这个方法0

    def method_x(self):
        print('<[5] ClassOne method_x>')

    class ClassTwo:
        print('<[6] classTwo> body')

@deco_alpha
class ClassThree:
    print('<[7] ClassThree body>')

    def method_y(self):
        print('<[8] ClassThree method_y>')


class ClassFour(ClassThree):
    print('<[9] ClassFour body>')

    def method_y(self):
        print('<[10] ClassFour method_y>')

if __name__ == '__main__':
    print('<[11] ClassOne test>', 30 * '.')
    one = ClassOne()
    one.method_x()
    print('<[12] ClassThree test>', 30 * '.')
    three = ClassThree()
    three.method_y()          #被装饰器覆盖的方法
    print('<[12] ClassFour test>', 30 * '.')
    four = ClassFour()
    four.method_y()         #被装饰器不影响子类
print('<[14] evaltime end>')