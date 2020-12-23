# @Time    : 2020/12/23
# @Author  : sunyingqiang
# @Email   : 344670075@qq.com

"""
可迭代对象： 只要实现__iter__方法。或者实现__getitem__方法且__getitem__方法的参数是从0开始的整数，就可认为是可迭代对象
检查方法：用iter(x)函数检查，比isinstance(x, abc,Iterable)方法更可靠，因为iter函数会考虑__getitem__方法
迭代器: 只要实现__next__方法和__iter__方法就是迭代器
检查方法：isinstance(x, abc,Iterable)

迭代对象和迭代器的区别：迭代器实现了__next__方法，迭代对象没有。
生成器：含有yield关键字
所以的生成器全部都是迭代器，所以的迭代器都是可迭代对象

"""
import re
import reprlib

# RE_WORD = re.compile('\w+')
#
#
# class Sentence:
#
#     def __init__(self, text):
#         self.text = text
#         self.words = RE_WORD.findall(text)
#
#     def __getitem__(self, item):
#         """如果序列没有实现iter方法会自动找getitem方法然后从0开始查找元素"""
#         return self.words[item]
#
#     def __len__(self):
#         return len(self.words)
#
#     def __repr__(self):
#         """用于实现简略字符串实现形式"""
#         return 'Sentence(%s)' % reprlib.repr(self.text)
#
# s = Sentence('"The time has come," the Walrus said,')
# print(s)
# for word in s:
#     print(word)
# print(list(s))
# print(s[0])
# print(s[1])
#
# s3 = Sentence('pig and pepper')
# it = iter(s3)
# print(it)
# print(next(it))
# print(next(it))
# print(next(it))
# # print(next(it))
# print(list(it))   #前面已经全部取出，如果需要迭代则需要重新创建迭代器
# print(list(iter(s3)))

class Foo:
    """类实现了iter方法就是可迭代的"""
    def __iter__(self):
        pass

from collections import abc
f = Foo()
print(issubclass(Foo, abc.Iterable))
print(isinstance(f, abc.Iterable))


# RE_WORD = re.compile('\w+')
#
#
# class Sentence:
#     """这个类是可迭代的对象，不是迭代器"""
#     def __init__(self, text):
#         self.text = text
#         self.words = RE_WORD.findall(text)
#
#     def __repr__(self):
#         """用于实现简略字符串实现形式"""
#         return 'Sentence(%s)' % reprlib.repr(self.text)
#
#     def __iter__(self):
#         return SentenceIterator(self.words)
#
#
# class SentenceIterator:
#     """这个类是迭代器同时也是可迭代对象"""
#     def __init__(self, words):
#         self.words = words
#         self.index = 0
#
#     def __next__(self):
#         try:
#             word = self.words[self.index]
#         except IndexError:
#             raise StopIteration()
#         self.index += 1
#         return word
#
#     def __iter__(self):
#         return self


RE_WORD = re.compile('\w+')


class Sentence:
    """用生成器函数实现迭代器"""
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        """用于实现简略字符串实现形式"""
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        for word in self.words:
            yield word
        return

s = Sentence('"The time has come," the Walrus said,')
print(list(s))
# for i in s:
#     print(i)


def gen_AB():
    print('satrt')
    yield 'A'
    print('continue')
    yield 'B'
    print('end')

for c in gen_AB():
    print('---->', c)


class ArithmeticProgression:
    """实现一个等差数列"""
    def __init__(self, begin, step, end=None):
        self.begin = begin
        self.step = step
        self.end = end

    def __iter__(self):
        result = type(self.begin + self.step)(self.begin)   #转成指定类型的数据
        forever = self.end is None
        index = 0
        while forever or result < self.end:
            yield result
            index += 1
            result = self.begin + self.step * index

ap = ArithmeticProgression(0, 1, 3)
print(list(ap))
ap = ArithmeticProgression(1, .5, 3)
print(list(ap))


import itertools
gen = itertools.count(1, .5)  #一个生成器从一开始每个0.5取一个无上限
print(gen)
print(next(gen))
print(next(gen))

gen = itertools.takewhile(lambda n: n < 3, itertools.count(1, .5))  #返回符合函数结果的数据集
print(list(gen))

str1 = 'abcd'
str2 = 'a'
gen = itertools.compress(str1, str2)  #如果str2为真则输出str1的值
print(next(gen))
# print(next(gen))
# print(next(gen))
# print(next(gen))

list1 = [1, 2, 3, 4]
gen = itertools.dropwhile(lambda n: n < 3, list1)  #输出不符合函数的内容
print(list(gen))


list1 = [1, 2, 3, 4]
gen = itertools.filterfalse(lambda n: n < 3, list1)  #输出不符合函数的内容
print(list(gen))

list1 = [1, 2, 3, 4]
gen = itertools.islice(list1, 3)  #返回切片
print(list(gen))

sample = [5, 4, 2, 8, 7, 6, 3, 0, 9, 1]
print(list(itertools.accumulate(sample)))       #产出累计和
print(list(itertools.accumulate(sample, min)))      #和后面的数挨个比对大小取最小值
print(list(itertools.accumulate(sample, max)))
import operator
print(list(itertools.accumulate(sample, operator.mul)))         #计算乘积
print(list(itertools.accumulate(range(1, 11), operator.mul)))       #1,10的阶乘

print(list(enumerate('avcadsad', 1)))       #迭代出元素的index和元素 index从指定开始默认为0
print(list(map(operator.mul, range(11), range(11))))
print(list(map(operator.mul, range(11), [2, 4, 6])))

print(list(itertools.starmap(operator.mul, enumerate("asdsa", 1))))


print(list(itertools.chain('abc', range(2))))       #把两个迭代元素合并
print(list(itertools.chain(enumerate('avcadsad', 1))))      #只传入一个迭代元素无实际作用

print(list(itertools.chain.from_iterable(enumerate('avcadsad'))))       #取出每个元素顺序连接起来，只能传一个可迭代元素

print(list(zip('abc', range(5))))       #把连个可迭代的元素合并成一个元祖
print(list(zip('abc', range(5), 'dsad')))

print(list(itertools.zip_longest('abd', range(5))))     #和zip相似按最长的对象为标准，不够的补None
print(list(itertools.zip_longest('abd', range(5), fillvalue='?')))      #指定不够长的补什么

print(list(itertools.product('abc', range(2))))     #生成一个笛卡尔积，输出两个元素拼接的最多可能元祖
print(list(itertools.product('abc')))       #传入一个无作用
print(list(itertools.product('abc', repeat=2)))     #重复几次输入各个可迭代对象


cy = itertools.cycle('abc')         #重复的产出各个元素
print(next(cy))
print(next(cy))
print(next(cy))
print(next(cy))

rp = itertools.repeat(7)        #重复的产出这个元素
print(next(rp))
print(next(rp))

print(list(itertools.repeat(7, 3)))   #指定产出多少个

print(list(itertools.combinations('abc', 2)))       #元素的几种组合，不包括相同元素
print(list(itertools.combinations_with_replacement('abc', 2)))      #包括相同元素

print(list(itertools.permutations('abc', 2)))        #元素的几种组合，不包括相同元素,可以有不同顺序的

print(list(itertools.groupby('LLLAAGG')))
for char, group in itertools.groupby('LLLAAGG'):
    print(char, '-->', list(group))


animals = ['aa',  'bb', 'a', 'b']
for char, group in itertools.groupby(animals, len):
    print(char, '-->', list(group))

print(list(itertools.tee('abc')))   #产生多个相同的生成器
g1, g2 = itertools.tee('abc')
# print(next(g1))
# print(next(g2))
print(list(g1))
print(list(g2))