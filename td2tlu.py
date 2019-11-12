#! /usr/bin/env python3

import xml.etree.ElementTree as ET
import argparse


class TimereportConverter():
    def __init__(self):
        pass

    def convert(self, tree):
        if not tree:
            return None
        xml = ET.ElementTree()
        return xml


if (__name__ == "__main__"):

    argparser = argparse.ArgumentParser(
        description='Convert XML output from Timeduty to TLU format XML.')
    argparser.add_argument(
        'file', help='name of the XML file from TimeDuty')

    args = argparser.parse_args()

    print('Reading...')
    indata = ET.parse(args.file)
    for setting in indata.iter('setting'):
        if 'FilterDateFrom' in setting.attrib.values():
            from_date = setting.attrib['value'].split(' ', 1)[0]
        if 'FilterDateTo' in setting.attrib.values():
            to_date = setting.attrib['value'].split(' ', 1)[0]

    print('Writing...')
    tree = ET.Element('SalaryData')
    timecodes = ET.SubElement(tree, 'TimeCodes')
    timecode_sjuk = ET.SubElement(timecodes, 'TimeCode', {
        'Code': '1', 'TimeCodeName': 'Sjukdom'})
    timecode_vab = ET.SubElement(timecodes, 'TimeCode', {
        'Code': '2', 'TimeCodeName': 'VAB'})
    timecode_semester = ET.SubElement(timecodes, 'TimeCode', {
        'Code': '3', 'TimeCodeName': 'Semester'})
    print(ET.tostring(tree))
