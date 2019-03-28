import functools


def attr_length_validator(max_length):
    def decorator_func(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):

            nargs = []
            for arg in args:
                if isinstance(arg, str):
                    nargs.append(arg[:max_length])
                else:
                    nargs.append(arg)

            for key, value in kwargs.items():
                if isinstance(value, str):
                    kwargs[key] = value[:max_length]

            return func(*nargs, **kwargs)

        return inner

    return decorator_func


class cached_property(property):
    @functools.lru_cache()
    def __get__(self, obj, type=None):
        return super(cached_property, self).__get__(obj, type)
