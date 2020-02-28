#! /usr/bin/env python3
import unittest
import lxml.etree as ET
from tdreader import convert_hour_and_minute_to_fractional_hour


class TD2TLUTest(unittest.TestCase):

    def test_convert_time_to_decimal_handles_whole_hours(self):
        self.assertEqual(convert_hour_and_minute_to_fractional_hour('8'), '8')

    def test_convert_time_to_decimal_handles_hours_zero_minutes(self):
        self.assertEqual(convert_hour_and_minute_to_fractional_hour('8:00'), '8')

    def test_convert_time_to_decimal_handles_hours_with_6_minutes(self):
        self.assertEqual(convert_hour_and_minute_to_fractional_hour('8:06'), '8.1')

    def test_convert_time_to_decimal_handles_hours_with_13_minutes(self):
        self.assertEqual(convert_hour_and_minute_to_fractional_hour('8:13'), '8.22')
