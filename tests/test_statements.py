import unittest
from harvestosm.statement import Statement, Node, Way
# from harvestosm.statement import Tag
from shapely import geometry


class TestStatement(unittest.TestCase):

    def setUp(self):
        self.element = 'element'
        self.tag = 'tag'
        self.area = 'area'
        self.tag_dict = {'key1': 'value1', 'key2': 'value2'}
        self.tag_list = ['value1','value2' ]

    def test_statement_costruct(self):
        # general constructor
        s = Statement(self.element, self.area,  self.tag)
        self.assertEqual(s.__str__(), f'{self.element}{self.area}->.A;\n{self.element}.A["{self.tag}"]->.B;')

        # Node child
        n = Node(self.area, self.tag)
        self.assertEqual(n.__str__(), f'node{self.area}->.C;\nnode.C["{self.tag}"]->.D;')

        # Way child
        w = Way(self.area, self.tag)
        self.assertEqual(w.__str__(), f'way{self.area}->.E;\nway.E["{self.tag}"]->.F;')

        # Without tag
        t = Way(self.area)
        self.assertEqual(t.__str__(), f'way{self.area}->.G;')
#
    def test_tags(self):
        # set tag se dict
        t = Node(self.area, tag={'key1':'value1', 'key2':'value2' })
        self.assertEqual(t.__str__(), f'node{self.area}->.H;\nnode.H["key1"="value1"]["key2"="value2"]->.I;')

        # set tag as list
        t = Node(self.area, tag=['value1', 'value2'])
        self.assertEqual(t.__str__(), f'node{self.area}->.J;\nnode.J["value1"]["value2"]->.K;')
# #
# #
#     def setUp(self):
#         self.tag_string = 'string'
#         self.tag_string_repr = '["string"]'
#         self.tag_dict = {'key1': 'val1', 'key2': 'val2', 'key3': None}
#         self.tag_dict_repr = '["key1"="val1"]["key2"="val2"]["key3"]'
#         self.tag_mix_list = [{'key1': 'val1', 'key2': 'val2'}, 'key3']
#
#
#     def test_tag_instance_repr(self):
#         tag = Tag(self.tag_string)
#         self.assertEqual(tag.__repr__(), self.tag_string_repr)
#         tag = Tag(self.tag_dict)
#         self.assertEqual(tag.__repr__(), self.tag_dict_repr)
#         tag = Tag(self.tag_mix_list)
#         self.assertEqual(tag.__repr__(), self.tag_dict_repr)
#         tag = Tag()
#         self.assertEqual(tag.__repr__(), '')



if __name__ == '__main__':
    unittest.main()