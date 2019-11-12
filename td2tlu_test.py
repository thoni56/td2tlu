#! /usr/bin/env python3
import unittest

from td2tlu import TimereportConverter


class TD2TLUTest(unittest.TestCase):

    def test_converts_an_empty_tree_to_an_empty_tree(self):
        converter = TimereportConverter()
        tree = converter.convert(None)
        self.assertEqual(tree.getroot, None)
