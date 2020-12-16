# @Time    : 2020/12/16
# @Author  : sunyingqiang
# @Email   : 344670075@qq.com

import abc
import random


class Tombola(abc.ABC):
    """定义一个抽象基类"""

    @abc.abstractmethod
    def load(self, iterable):
        """从可迭代对象中添加元素"""

    @abc.abstractmethod
    def pick(self):
        """随机删除元素，然后将其返回"""

    def loaded(self):
        """如果至少有一个元素，返回True, 否则返回False"""
        return bool(self.inspect())

    def inspect(self):
        """返回一个有序元组，由当前元素构成"""
        items = []
        while True:
            try:
              items.append(self.pick())
            except LookupError:
                break
        self.load(items)
        return tuple(sorted(items))


class BingoCage(Tombola):

    def __init__(self, items):
        self._randomizer = random.SystemRandom()
        self._items = []
        self.load(items)

    def load(self, iterable):
        self._items.extend(iterable)
        self._randomizer.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')

    def __call__(self, *args, **kwargs):
        self.pick()

b = BingoCage(['a', 'b', 'c', 'd'])
print(b())
print(b.pick())
print(b.pick())
print(b.pick())


class LotteryBlower(Tombola):

    def __init__(self, iterable):
        self._balls = list(iterable)

    def load(self, iterable):
        self._balls.extend(iterable)

    def pick(self):
        try:
           position = random.randrange(len(self._balls))
        except ValueError:
            raise LookupError('pick from empty LotterBlower')
        return self._balls.pop(position)

    def loaded(self):
        return bool(self._balls)

    def inspect(self):
        return tuple(sorted(self._balls))


@Tombola.register
class TomboList(list):
    """不采用继承的方式，采用装饰器的方式实现抽象基类"""
    def pick(self):
        if self:
            position = random.randrange(len(self))
            return self.pop(position)
        else:
            raise LookupError('pop from empty TomboList')

    load = list.extend

    def loaded(self):
        return bool(self)

    def inspect(self):
        return tuple(sorted(self))

print(issubclass(TomboList, Tombola))  #判断TomboList是不是Tombola的子类
t = TomboList(range(100))
print(t.inspect())
print(isinstance(t, Tombola))
print(list(Tombola._abc_registry))


import doctest

TEST_FILE = 'tombola_test.rst'
TEST_MSG = '{0:16} {1.attempted:2} tests, {1.failed:2} failed - {2}'

def main(argv):
    verbose = '-v' in argv
    real_subclasses = Tombola.__subclasses__()
    virtual_subclasses = list(Tombola._abc_registry)

    for cls in real_subclasses + virtual_subclasses:
        test(cls, verbose)

def test(cls, verbose=False):
    res = doctest.testfile(TEST_FILE,
                           globs={'ConcreteTombola': cls},
                           verbose=verbose,
                           optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)
    tag = 'FAIL' if res.failed else 'ok'
    print(TEST_MSG.format(cls.__name__, res, tag))


if __name__ == '__main__':
    import sys
    main(sys.argv)


