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
        self.assertEqual(0, 0)

    def test_converts_180301_sample_file_correctly(self):
        converter = TimereportConverter()
        input_tree = ET.parse('test_1_anstalld_1_registrering_franvaro-input.xml')
        output_tree = converter.convert(input_tree)
        output = ET.tostring(output_tree, pretty_print=True).decode()
        with open("test_1_anstalld_1_registrering_franvaro-expected.tlu") as f:
            expected = f.read()
        self.assertEqual(output, expected)
        

