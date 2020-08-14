from utils import utils, decorators
from shapely.geometry.base import BaseGeometry
from shapely.geometry import shape, Polygon
from shapely.ops import transform
import fiona




# class Geometry:
#     """Base geometry object based on shapely"""
#     def __init__(self, geom):
#         if isinstance(geom, BaseGeometry):
#             self.geom = geom
#         else:
#             raise TypeError('Input geometry can be defined as shapely object, bbox, geojson object or geojson path')
#
#     @classmethod
#     def from_geojson(cls, geojson):
#         """construct from geojson"""
#         if geojson.is_valid:
#             if len(geojson['features']) == 1:
#                 return cls(shape(geojson['features'][0].get('geometry')))
#             else:
#                 raise ValueError('AOI have to be defined by one single polygon ')
#         else:
#             raise TypeError('Invalid geojson object')
#
#     @classmethod
#     def from_bbox(cls, bbox):
#         """Bounding region (min_lat, min_lon, max_lat, max_lon) """
#         return cls(Geometry._bbox2shapely(bbox))
#
#     @classmethod
#     def from_file(cls, file):
#         try:
#             with fiona.open(file, 'r') as src:
#                 if len(src) > 0:
#                     print('Version 0.2: Supports only one singlepart area')
#                     return cls(shape(src[0]['geometry']))
#         except TypeError:
#             raise (f'{file} is not path')
#
#     @property
#     @decorators.wra2plist
#     def coords(self):
#         if hasattr(self.geom, 'exterior'):
#             return self.geom.exterior.coords
#         elif self.geom.type == 'MultiPolygon':
#             return self.geom[0].exterior.coords
#         else:
#             return self.geom.coords
#
#     @property
#     def bbox(self):
#         return self.geom.bounds
#
#     def reverse(self):
#         return transform(lambda x, y: (y, x), self.geom)
#
#     @staticmethod
#     def _bbox2shapely(bbox):
#         """ Converts the input coordination representation (see the constructor docstring for a list of valid
#         representations) into a flat tuple
#
#         :param bbox: A bbox in one of several forms listed in the class description.
#         :return: shapely.geometry.polygon
#         :raises: TypeError
#         """
#         if isinstance(bbox, (list, tuple)):
#             if len(bbox) == 4:
#                 points = tuple(map(float, bbox))
#                 return Polygon(Geometry._bbox2poly(points))
#             if len(bbox) == 2 and all([isinstance(point, (list, tuple)) for point in bbox]):
#                 points = [coor for coors in bbox for coor in coors]
#                 return Polygon(Geometry._bbox2poly(points))
#             raise TypeError('Expected a valid list or tuple representation of a bbox')
#         elif isinstance(bbox, str):
#             try:
#                 points = tuple([float(s) for s in bbox.replace(',', ' ').split() if s])
#                 return Polygon(list(zip(points[::2], points[1::2])))
#             except ValueError:
#                 raise ValueError('Invalid bbox representation')
#         else:
#             raise TypeError('Invalid bbox representation')
#
#     @staticmethod
#     def _bbox2poly(bbox):
#         """From tuple (minx, miny, maxx, maxy) calculate remaining corners"""
#         minx, miny, maxx, maxy = bbox
#         return (minx, miny), (maxx, miny), (maxx, maxy), (minx, maxy)
#
#
# class Area(Geometry):
#     """Class for overpass area statements"""
#     def __init__(self, geom):
#         self.name = utils.random_name()
#         super(Area, self).__init__(geom)
#
#     @property
#     def overpass_poly(self):
#         return '(poly: "{}")'.format(' '.join([str(p) for xy in
#                                                Area(self.reverse()).coords.__iter__() for p in xy]))
