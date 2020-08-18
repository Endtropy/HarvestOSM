import unittest
from harvestosm.statement import Statement, Node, Way, Area
from harvestosm.utils import open_json, save2json
from shapely.geometry import Polygon, MultiPolygon


class TesHarvest(unittest.TestCase):

    def setUp(self):
        self.element = 'element'
        self.tag = 'tag'
        self.area = Polygon([(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)])
        self.area_overpass = '(poly: "0.0 0.0 0.0 1.0 1.0 1.0 1.0 0.0 0.0 0.0")'
        self.tag_dict = {'key1': 'value1', 'key2': 'value2'}
        self.tag_list = ['value1', 'value2']
        self.tag_list2 = ['key1=value1']
        self.poly_shape = Polygon([(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)])
        self.mpoly_shape = MultiPolygon(polygons=[self.poly_shape])
        save2json('config.json', **{'lonlat': True})


    def test_statement_costruct(self):
        # general constructor
        s = Statement(self.element, self.area,  self.tag)
        res = ''.join(ch for ch in s.__str__() if not ch.isupper())
        self.assertEqual(res, f'{self.element}{self.area_overpass}->.; {self.element}.["{self.tag}"]->.;')

        # Node child
        n = Node(self.area, self.tag)
        res = ''.join(ch for ch in n.__str__() if not ch.isupper())
        self.assertEqual(res, f'node{self.area_overpass}->.; node.["{self.tag}"]->.;')

        # Way child
        w = Way(self.area, self.tag)
        res = ''.join(ch for ch in w.__str__() if not ch.isupper())
        self.assertEqual(res, f'way{self.area_overpass}->.; way.["{self.tag}"]->.;')

        # Without tag
        t = Way(self.area)
        res = ''.join(ch for ch in t.__str__() if not ch.isupper())
        self.assertEqual(res, f'way{self.area_overpass}->.;')

    def test_tags(self):
        # set tag se dict
        t = Node(self.area, tag={'key1': 'value1', 'key2': 'value2'})
        res = ''.join(ch for ch in t.__str__() if not ch.isupper())
        self.assertEqual(res, f'node{self.area_overpass}->.; node.["key1"="value1"]["key2"="value2"]->.;')

        # set tag as list
        t = Node(self.area, tag=['value1', 'value2'])
        res = ''.join(ch for ch in t.__str__() if not ch.isupper())
        self.assertEqual(res, f'node{self.area_overpass}->.; node.["value1"]["value2"]->.;')

        t = Node(self.area, tag=self.tag_list2)
        res = ''.join(ch for ch in t.__str__() if not ch.isupper())
        self.assertEqual(res, f'node{self.area_overpass}->.; node.["key1=value1"]->.;')

    def test_math(self):
        # union
        n = Node(self.area, self.tag)
        w = Way(self.area)
        res = ''.join(ch for ch in n.union(w).__str__() if not ch.isupper())
        self.assertEqual(res, f'node{self.area_overpass}->.; node.["{self.tag}"]->.;'
                              f' way{self.area_overpass}->.; (.;  .;)->.;')
        # intersect
        n = Node(self.area)
        w = Way(self.area)
        res = ''.join(ch for ch in n.intersection(w).__str__() if not ch.isupper())
        self.assertEqual(res, f'node{self.area_overpass}->.; way{self.area_overpass}->.; node..;->.;')

        # recurse
        n = Node(self.area)
        res = ''.join(ch for ch in n.recurse('<').__str__() if not ch.isupper())
        self.assertEqual(res, f'node{self.area_overpass}->.; (.; < ;)->.;')

    def test_area_constructor(self):
        # rest type error
        self.assertRaises(TypeError, Area, '' )

        #test creation
        self.assertIsInstance(Area(self.poly_shape),Area)

        #sets polygon coords
        a=Area(self.poly_shape)
        self.assertEqual(a.coords, [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0), (0.0, 0.0)])

        #sets polygon coords
        a=Area(self.mpoly_shape)
        self.assertEqual(a.coords, [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0), (0.0, 0.0)])

        # TODO
        #sets point coords
        # a=Area(self.point_shape)
        # self.assertEqual(a.coords, [(1.0, 0.0)])

        #sets linestring
        # a=Area(self.line_shape)
        # self.assertEqual(a.coords, [(0, 0), (1, 1)])

    def test_BaseMeta(self):
        # test of access to config attribute
        s = Statement(self.element, self.area,  self.tag)
        self.assertEqual(s.lonlat, open_json('config.json').get('lonlat'))
        s.lonlat = True

        # test of changing of attribute
        n = Node(self.area, tag=self.tag)
        n.lonlat = False
        self.assertEqual(s.lonlat, n.lonlat)
        s.lonlat = True


if __name__ == '__main__':
    unittest.main()
