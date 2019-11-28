import sys


class TailRecourseException(BaseException):
    """
    自定义异常
    """

    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs


def tail_call_optimized(g):
    """
    自定义装饰器，尾递归优化，当这个函数是其本身的祖父时，使它等于它自己，防止栈溢出。
    但是效率约为之前的1/5左右。（不完全统计）
    """
    def func(*args, **kwargs):
        f = sys._getframe()
        if f.f_back and f.f_back.f_back and f.f_back.f_back.f_code == f.f_code:
            raise TailRecourseException(args, kwargs)
        else:
            while True:
                try:
                    return g(*args, **kwargs)
                except TailRecourseException as e:
                    args = e.args
                    kwargs = e.kwargs
    func.__doc__ = g.__doc__
    return func
