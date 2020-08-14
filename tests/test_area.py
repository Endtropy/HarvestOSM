import unittest
from harvestosm.area import Area
from shapely import geometry


class TestStatement(unittest.TestCase):

    def setUp(self):
        self.point_shape = geometry.Point(1.0, 0.0)
        self.point_coords = [(1.0, 0.0)]
        self.line_shape = geometry.LineString([(0, 0), (1, 1)])
        self.line_coords = [(0.0, 0.0), (1.0, 1.0)]
        self.poly_shape = geometry.Polygon([(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)])
        self.poly_coords = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0), (0.0, 0.0)]
        self.bbox_coords = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
        self.area = Area(self.poly_shape)

    def test_from_bbox(self):
        area = Area.from_bbox((0.0, 0.0, 1.0, 1.0))
        self.assertEqual(area.coords, self.poly_coords)

    def test_coords(self):
        area = Area(self.poly_shape)
        self.assertEqual(area.coords, self.poly_coords)
        area = Area(self.line_shape)
        self.assertEqual(area.coords, self.line_coords)

    def test_overpass_poly(self):
        self.assertEqual(self.area.overpass_poly, '(poly: "0.0 0.0 0.0 1.0 1.0 1.0 1.0 0.0 0.0 0.0")')

    # def test_bbox(self):
    #     self.assertEqual(self.area.bbox, '(0.0,0.0,1.0,1.0)')

if __name__ == '__main__':
    unittest.main()