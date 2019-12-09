#! /usr/bin/env python3
import unittest
import lxml.etree as ET
from td2tlu import TimereportConverter


class TD2TLUTest(unittest.TestCase):

    def test_converts_no_file_to_None(self):
        converter = TimereportConverter()
        tree = converter.convert(None)
        self.assertEqual(tree, None)

    def convert_and_compare(self, case_name):
        converter = TimereportConverter()
        output = converter.convert(case_name+'.xml', creation_date="2018-04-01")
        output_file = open(case_name+'.output', 'w+')
        print(output, file=output_file)
        with open(case_name+'.tlu') as f:
            expected = f.read()
        self.assertEqual(output, expected)
            
    def test_converts_a_minimal_input_to_tlu_with_all_required_elements(self):
        self.convert_and_compare('minimal')

    def test_1_employee_1_registration(self):
        self.convert_and_compare('1_anstalld_1_registrering_franvaro')
        

