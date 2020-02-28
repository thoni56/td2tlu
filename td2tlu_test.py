#! /usr/bin/env python3
import unittest
import lxml.etree as ET
from td2tlu import TimereportConverter, User, convert_time_to_decimal


class TD2TLUTest(unittest.TestCase):

    timecode_table = {
        'Sjukdom':'1',
        'VAB':'2',
        'Semester':'3'
    }

    def convert_and_compare(self, case_name):
        converter = TimereportConverter(users=[User('anders.bodelius@responsive.se', '1', 'Anders', 'Bodelius')],
            timecodes=self.timecode_table)
        output = converter.convert_to_tlu(case_name+'.xml', creation_date="2018-04-01")
        output_file = open(case_name+'.output', 'w+')
        print(output, file=output_file)
        with open(case_name+'.tlu') as f:
            expected = f.read()
        self.assertEqual(output.strip(), expected.strip())
            
    def test_converts_a_minimal_input_to_tlu(self):
        self.convert_and_compare('minimal')

    def test_1_employee_1_registration(self):
        self.convert_and_compare('1_anstalld_1_registrering_franvaro')
        
    def test_1_employee_2_registrations(self):
        self.convert_and_compare('1_anstalld_2_registrering_franvaro')
    
    def test_1_employee_2_mixed_registrations(self):
        self.convert_and_compare('1_anstalld_2_blandade_registreringar')
        
    def test_convert_time_to_decimal_handles_whole_hours(self):
        self.assertEqual(convert_time_to_decimal('8'), '8')

    def test_convert_time_to_decimal_handles_hours_zero_minutes(self):
        self.assertEqual(convert_time_to_decimal('8:00'), '8')

    def test_convert_time_to_decimal_handles_hours_with_6_minutes(self):
        self.assertEqual(convert_time_to_decimal('8:06'), '8.1')

    def test_convert_time_to_decimal_handles_hours_with_13_minutes(self):
        self.assertEqual(convert_time_to_decimal('8:13'), '8.22')
