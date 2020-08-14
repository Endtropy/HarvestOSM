#!/usr/bin/env python

from utils.utils import get_name
from collections import namedtuple, OrderedDict
# from harvestosm.area import Area
from utils.decorators import option
from os import path

gen_name = get_name().__iter__()

class Tag:

    def __init__(self, tag=None):
        if not isinstance(tag, (list, str, dict)) and tag is not None:
            raise ValueError(f'Tag can be string, dictionary or list of string. Not {type(tag)}')
        self.tag = tag

    def __repr__(self):
        if isinstance(self.tag, (str, dict)):
            return self.print_tag(self.tag)
        elif isinstance(self.tag, list) and all(isinstance(val, str) or isinstance(val, dict) for val in self.tag):
            return ''.join(self.print_tag(val) for val in self.tag)
        elif self.tag is None:
            return ''

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def print_tag(tag):
        if isinstance(tag, str):
            return f'["{tag}"]'
        elif isinstance(tag, dict):
            return ''.join(f'["{key}"]' if val is None else f'["{key}"="{val}"]' for key, val in tag.items())



class Set:
    def __init__(self, element, area, name):
        self.element = element
        self.name = name
        self.area = area

    def __str__(self):
        return f'{self.element}{self.area}->.{self.name};'

class TagSet(Set):

    def __init__(self, element, area, name, tag):
        self.tag = Tag(tag)
        super().__init__(element, area, name)

    def __str__(self):
        return f'{self.element}.{self.area}{self.tag}->.{self.name};'


class Statement:

    def __init__(self, element, area, tag=None):

        area_name = next(gen_name)
        self.container = OrderedDict({area_name: Set(element, area, area_name)})

        if tag is not None:
            tag_name = next(gen_name)
            self.container.update({tag_name: TagSet(element, area_name, tag_name, tag)})

    def __str__(self):
        return '\n'.join(val.__str__() for _, val in self.container.items())

    def union(self, other):
        return self.math(other, '')

    def math(self, other, operator):
        name = next(gen_name)

        try:
            self.operation.update(other.operation)
            self.operation.update({name : f'(.{self.last}; {operator} .{other.last};)->.{name };'})
        except StopIteration:
            self.operation.update({name : f'(.{self.last}; {operator} .{other.last};)->.{name};'})

        self.statement.update(other.statement)
        self.last = name
        return self


class Node(Statement):
    def __init__(self, area, tag=None):
        super().__init__('node', area, tag)


class Way(Statement):
    def __init__(self, area, tag=None):
        super().__init__('way', area, tag)


if __name__ == '__main__':
    n=Node('area','tag')




# class Tag:
#
#     def __init__(self, tag=None):
#         if not isinstance(tag, (list, str, dict)) and tag is not None:
#             raise ValueError(f'Tag can be string, dictionary or list of strings or None and'
#                              f' dictionaries. Not {type(tag)}')
#         self.tag = tag
#
#     def __repr__(self):
#         if isinstance(self.tag, (str, dict)):
#             return self.print_tag(self.tag)
#         elif isinstance(self.tag, list) and all(isinstance(val, str) or isinstance(val, dict) for val in self.tag):
#             return ''.join(self.print_tag(val) for val in self.tag)
#         elif self.tag is None:
#             return ''
#
#     def __str__(self):
#         return self.__repr__()
#
#     @staticmethod
#     def print_tag(tag):
#         if isinstance(tag, str):
#             return f'["{tag}"]'
#         elif isinstance(tag, dict):
#             return ''.join(f'["{key}"]' if val is None else f'["{key}"="{val}"]' for key, val in tag.items())
#
#
# class Operation(OrderedDict):
#     def __str__(self):
#         return '\n'.join(v for _, v in self.items())


# class OSMset(OrderedDict):
#
#     def __init__(self):
#         self.name
#
#     def __str__(self):
#         return '\n'.join(f'{val.element}{val.tag}{val.area.overpass_poly}->.{val.name};' for _, val in self.items())







# @option(timeout=360, out='body geom', format_output='json')
# class Statement:
#     OSMSET = namedtuple('STATEMENT', ['element', 'tag', 'area', 'name'])
#
#     def __init__(self, element, tag, area):
#         if not element in ['node', 'way', 'rel', 'area']:
#             raise ValueError(f'OSM element can be node, way, rel or area not {element}')
#
#         elif isinstance(area, Area):
#             pass
#         elif isinstance(area, dict):
#             area = Area.from_geojson(area)
#         elif isinstance(area, (str, list)):
#             area = Area.from_bbox(area)
#         elif isinstance(area, str) and path.isfile(area):
#             area = Area.from_file(area)
#         else:
#             raise TypeError('Unsupported type of area. Area can be defined as bbox, shapely object or geojson')
#
#         name = random_name()
#         self.statement = OSMset({name: self.OSMSET(element, Tag(tag), area, name)})
#         self.operation = Operation()
#         self.last = name
#
#     def __str__(self):
#         code = [f'[out:{self.format_output}][timeout:{self.timeout}];']
#         code += [str(getattr(self, container)) for container in ['statement', 'operation']]
#         try:
#             code += [f'.{self.last} out {self.out};']
#         except StopIteration:
#             code += [f'.{self.last} out {self.out};']
#         return '\n'.join(code)
#
#     def __add__(self, other):
#         return self.math(other, '')
#
#     def __sub__(self, other):
#         return self.math(other, '-')
#
#     def math(self, other, operator):
#         name = random_name()
#
#         try:
#             self.operation.update(other.operation)
#             self.operation.update({name : f'(.{self.last}; {operator} .{other.last};)->.{name };'})
#         except StopIteration:
#             self.operation.update({name : f'(.{self.last}; {operator} .{other.last};)->.{name};'})
#
#         self.statement.update(other.statement)
#         self.last = name
#         return self
#
#     def intersection(self, other, element='node'):
#         name = random_name()
#         self.operation.update({name: f'{element}.{self.last}.{other.last};->.{name};'})
#         self.operation.update(other.operation)
#         self.statement.update(other.statement)
#         self.last = name
#         return self
#
#     def recurse(self, recurse):
#         if recurse in ['<', '<<', '>>', '>']:
#             name = random_name()
#             self.operation.update({name: f'(.{self.last}; {recurse} ;)->.{name};'})
#             self.last = name
#             return self
#         else:
#             raise ValueError(f'Valid recurse symbols are <, <<, >>, >, Not {recurse}')


# if __name__ == '__main__':
#     from shapely.geometry import Polygon
#     p = Polygon([(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)])
#     p2 = Polygon([(1.0, 1.0), (2.0, 1.0), (2.0, 2.0), (1.0, 2.0)])
#     a = Area(p)
#     a2 = Area(p2)
#     t = Tag('a')
#     st1 = Statement('node', t, a)
#     st2 = Statement('way', t, a)
#     st3 = Statement('rel', t, a2)
#
#     s=st1+st2.recurse('<')
#     s=s.intersection(st3)
#     print(s)

