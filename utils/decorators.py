import functools

def wra2plist(func):
    @functools.wraps(func)
    def wraper(*args, **kwargs):
        return list(func(*args, **kwargs))
    return wraper

def option(*args,**kwargs):
    def class_wrap(cls):
        @functools.wraps(cls)
        def wrapper_atribures(**kwargs):
            for key, val in kwargs.items():
                setattr(cls, key, val)
            return cls
        return wrapper_atribures(**kwargs)
    return class_wrap
