from harvestosm.utils import open_json, save2json, BASE_PATH


class ConfigMeta(type):
    """config singleton"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(ConfigMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    def __new__(cls, name, bases, clsdict):
        clsobj = super().__new__(cls, name, bases, clsdict)
        for key, value in open_json(clsobj.CONFIG).items():
            setattr(clsobj, key,  value)
        return clsobj


class Config(metaclass=ConfigMeta):
    CONFIG = BASE_PATH / 'config.json' # define together with BaseMeta metaclass config properties

    def get(self, name):
        return self.__getattribute__(name)

    def set(self, name, value):
        self.__setattr__(name, value)
        save2json('config.json', **{name: value})


class Descriptor:
    """Configurate config proprety"""
    def __init__(self, name, *args):
        self.name = name
        self.config = Config()

    def __get__(self, obj, type=None):
        return self.config.get(self.name)

    def __set__(self, obj, value):
        self.config.set(self.name, value)


class BaseMeta(type):

    def __new__(cls, name, bases, clsdict):
        clsobj = super().__new__(cls, name, bases, clsdict)
        for key, _ in open_json(Config.CONFIG).items():
            setattr(clsobj, key, Descriptor(key))
        return clsobj