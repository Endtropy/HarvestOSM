#!/usr/bin/env python

from harvestosm.utils import get_name, BASE_PATH
from collections import OrderedDict
from shapely.ops import transform
from harvestosm.decorators import wra2plist
from shapely.geometry.base import BaseGeometry
from shapely.geometry import shape
from harvestosm.base import BaseMeta, ConfigMeta
from harvestosm.overpass import Overpass

# shared name iterator
gen_name = get_name().__iter__()

# TODO:
# dodelat geometrii podel linie a bod, zatim to hazi typeerror


class Area(metaclass=BaseMeta):

    def __init__(self, geom):
        if isinstance(geom, BaseGeometry) and geom.type in ['Polygon', 'MultiPolygon']:
            self.geom = geom
        elif hasattr(geom, '__geo_interface__'):
            try:
                self.geom = shape(geom.__geo_interface__)
            except ValueError:
                self.geom = shape(geom.__geo_interface__.get('features')[0].get('geometry'))
        else:
            raise TypeError('Input geometry have to by shapely object')

    @property
    def overpass_poly(self):
        """Return Overpass polygon representation of AOI """
        if not self.lonlat:
            return '(poly: "{}")'.format(' '.join([str(p) for xy in self.coords.__iter__() for p in xy]))
        return '(poly: "{}")'.format(' '.join([str(p) for xy in Area(self.reverse()).coords.__iter__() for p in xy]))

    def reverse(self):
        return transform(lambda x, y: (y, x), self.geom)

    @property
    @wra2plist
    def coords(self):
        if hasattr(self.geom, 'exterior'):
            return self.geom.exterior.coords
        elif self.geom.type == 'MultiPolygon':
            return self.geom[0].exterior.coords
        else:
            return self.geom.coords


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
        if hasattr(self.area, 'overpass_poly'):
            return f'{self.element}{self.area.overpass_poly}->.{self.name};'
        else:
            return f'{self.element}{self.area}->.{self.name};'


class TagSet(Set):

    def __init__(self, element, area, name, tag):
        self.tag = Tag(tag)
        super().__init__(element, area, name)

    def __str__(self):
        if hasattr(self.area, 'overpass_poly'):
            return f'{self.element}.{self.area.overpass_poly}{self.tag}->.{self.name};'
        else:
            return f'{self.element}.{self.area}{self.tag}->.{self.name};'


class SetContainer(OrderedDict):

    @property
    def last(self):
        return [k for k in self.keys()][self.__len__()-1]


class Statement(metaclass=BaseMeta):
    """
    Base class for generation of overpass statement

    Parameters:
        lonlat - (bool, defoult: True) Parameter specify order of coordinates in input geometry. If true, order of
                                       coordinates is changed into order required by overpass i.e lat lon
        overpass_timeout (int, default = 360) specify overpass timeout header i.e. [timeout:360]
        overpass_out_format (str, default = 'json') specify overpass output format i.e. [out:json]
        overpass_maxsize (int, default = 1073741824)  specify overpass max output size i.e. [maxsize:1073741824]
        overpass_out (str, default ='out body geom') specify overpass output
        overpass_endpoint "https://overpass-api.de/api/interpreter"
    """
    def __init__(self, element, area, tag=None):

        area_name = next(gen_name)
        self.container = SetContainer({area_name: Set(element, Area(area), area_name)})

        if tag is not None:
            tag_name = next(gen_name)
            self.container.update({tag_name: TagSet(element, area_name, tag_name, tag)})

        self.overpass = Overpass()

    def __str__(self):
        return ' '.join(val.__str__() for _, val in self.container.items())

    def union(self, other):
        """Union of two OSM sets i.e. (.A; .B;)->.C; """
        return self._math(other, '')

    def difference(self, other):
        """Difference of two OSM sets i.e. (.A; - .B;)->.C; """
        return self._math(other, '-')

    def _math(self, other, operator):
        name = next(gen_name)
        operation = {name: f'(.{self.container.last}; {operator} .{other.container.last};)->.{name};'}
        self.container.update(other.container)
        self.container.update(operation)
        return self

    def intersection(self, other, element='node'):
        name = next(gen_name)
        operation = {name: f'{element}.{self.container.last}.{other.container.last};->.{name};'}
        self.container.update(other.container)
        self.container.update(operation)
        return self

    def recurse(self, recurse):
        if recurse in ['<', '<<', '>>', '>']:
            name = next(gen_name)
            operation = {name: f'(.{self.container.last}; {recurse} ;)->.{name};'}
            self.container.update(operation)
            return self
        else:
            raise ValueError(f'Valid recurse symbols are <, <<, >>, >, Not {recurse}')

    @property
    def query(self):
        return ' '.join([f'[timeout:{self.overpass_timeout}][out:{self.overpass_out_format}][maxsize:'
                          f'{self.overpass_maxsize}];', self.__str__(),f'.{self.container.last} {self.overpass_out};'])

    def to_osm_json(self):
        self.overpass.query = self.query
        return self.overpass._osm_json

    def to_geojson(self):
        self.overpass.query = self.query
        return self.overpass.geojson

    def to_geopandas(self):
        self.overpass.query = self.query
        return self.overpass.gpd


class Node(Statement):
    def __init__(self, area, tag=None):
        super().__init__('node', area, tag)


class Way(Statement):
    def __init__(self, area, tag=None):
        super().__init__('way', area, tag)
