#! /usr/bin/env python3
import unittest
import lxml.etree as ET
from td2tlu import TimereportConverter


class TD2TLUTest(unittest.TestCase):

    def test_converts_an_empty_tree_to_an_empty_tree(self):
        converter = TimereportConverter()
        tree = converter.convert(None)
        self.assertEqual(tree, None)

    def test_converts_a_single_xml_node_to_tlu_xml_root(self):
        converter = TimereportConverter()
        input = ET.parse('minimal.xml')

        tree = converter.convert(input)
        self.assertEquals(0, 0)
