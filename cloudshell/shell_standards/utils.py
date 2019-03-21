import functools


def attr_length_validator(max_length):
    def decorator_func(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):

            nargs = []
            for arg in args:
                if isinstance(arg, basestring):
                    nargs.append(arg[:max_length])
                else:
                    nargs.append(arg)

            for key, value in kwargs.iteritems():
                if isinstance(value, basestring):
                    kwargs[key] = value[:max_length]

            return func(*nargs, **kwargs)

        return inner

    return decorator_func


class cached_property(property):
    def __init__(self, func, name=None, doc=None):
        self.__name__ = name or func.__name__
        self.__module__ = func.__module__
        self.__doc__ = doc or func.__doc__
        self.func = func

    def __set__(self, obj, value):
        obj.__dict__[self.__name__] = value

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        value = obj.__dict__.get(self.__name__, None)
        if value is None:
            value = self.func(obj)
            obj.__dict__[self.__name__] = value
        return value
