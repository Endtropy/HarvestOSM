from functools import wraps
from harvestosm.utils import open_json


def wra2plist(func):
    @wraps(func)
    def wraper(*args, **kwargs):
        return list(func(*args, **kwargs))
    return wraper


def option(*args, **kwargs):
    def class_wrap(cls):
        @wraps(cls)
        def wrapper_atribures(**kwargs):
            for key, val in open_json(kwargs.get('name')).items():
                setattr(cls, key, val)
            return cls
        return wrapper_atribures(**kwargs)
    return class_wrap


def set_config(*args, **kwargs):
    def class_wrap(cls):
        @wraps(cls)
        def wrapper_config(**kwargs):
            return cls
        return wrapper_config(**kwargs)
    return class_wrap


def debug(func):
    msg = func.__qualname__
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(msg)
        return func(*args, **kwargs)
    return wrapper
