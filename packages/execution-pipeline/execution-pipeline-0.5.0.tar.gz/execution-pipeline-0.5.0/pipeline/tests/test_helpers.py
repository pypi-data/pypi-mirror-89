import unittest

from pipeline import execution_pipeline


@execution_pipeline()
def my_func(a, b, caller, *args, kwarg=None, **kwargs):
    assert a == 1, a
    assert b == 2, b
    assert args == (4, 5, 6), args
    assert kwarg == "wow such kwarg", kwarg
    assert kwargs == {"one": 1, "two": 2}, kwargs


class SupportsVariadicArgs(unittest.TestCase):
    @execution_pipeline()
    def my_method(self, a, b, caller, *args, kwarg=None, **kwargs):
        assert self is not None, self
        my_func(a, b, caller, *args, kwarg=kwarg, **kwargs)

    @staticmethod
    def test_construct_valid_function_args_for_function():
        my_func(1, 2, "test_function", 4, 5, 6, kwarg="wow such kwarg", **{"one": 1, "two": 2})

    def test_construct_valid_function_args_for_method(self):
        self.my_method(1, 2, "test_method", 4, 5, 6, kwarg="wow such kwarg", **{"one": 1, "two": 2})

