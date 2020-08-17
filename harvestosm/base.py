from harvestosm.utils import open_json, save2json


class Descriptor:
    """Configurate config proprety"""
    def __init__(self, name, *args):
        self.name = name

    def __get__(self, obj, type=None):
        return open_json('config.json').get(self.name)

    def __set__(self, obj, value):
        save2json('config.json', **{self.name:value})


class BaseMeta(type):
    def __new__(cls, name, bases, clsdict):
        clsobj = super().__new__(cls, name, bases, clsdict)
        for key, value in open_json(clsobj.CONFIG).items():
            setattr(clsobj, key, Descriptor(key, value))
        return clsobj
