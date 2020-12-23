# @Time    : 2020/12/23
# @Author  : sunyingqiang
# @Email   : 344670075@qq.com

class LookingGlass:
    """自定义上下文管理器"""
    def __enter__(self):
        import sys
        self.original_write = sys.stdout.write   #执行print函数会调用sys.stdout.write然后把print里的参数传给sys.stdout.write
        sys.stdout.write = self.reverse_write
        return 'JABBERWOCKY'

    def reverse_write(self, text):
        self.original_write(text[::-1])

    def __exit__(self, exc_type, exc_val, exc_tb):
        import sys
        sys.stdout.write = self.original_write
        if exc_type is ZeroDivisionError:
            print('Please DO NOT divide by zero')
            return True

with LookingGlass() as what:
    print("Alice, kitty and Snowdrop")
    print(what)

print(what)

manager = LookingGlass()
print(manager)
monster = manager.__enter__()
print(monster)

print(monster == 'JABBERWOCKY')
print(monster)
manager.__exit__(None, None, None)
print(monster)

import contextlib

@contextlib.contextmanager            #装饰器自动实现enter方法和exit方法只需要写自己的逻辑即可
def looking_glass():
    import sys
    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])

    sys.stdout.write = reverse_write
    yield 'JABBERWOCKY'
    sys.stdout.write = original_write        #如果程序报错这句永远不执行

with looking_glass() as what:
    print("Alice, kitty and Snowdrop")
    print(what)

print(what)


@contextlib.contextmanager
def looking_glass():
    """加入错误处理的上下文管理器"""
    import sys
    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])

    sys.stdout.write = reverse_write
    try:
        yield 'JABBERWOCKY'
    except ZeroDivisionError:
        msg = 'Please DO NOT divide by zero'
    finally:
        sys.stdout.write = original_write
        if msg:
            print(msg)