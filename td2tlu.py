#! /usr/bin/env python3

import lxml.etree as ET
import argparse
import datetime


class TimereportConverter():
    def __init__(self):
        pass

    def convert(self, tree):
        if not tree:
            return None
        xml = ET.ElementTree()
        return xml


def is_row_for(row, user):
    u = row.find('username')
    return u.text == user


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

    report = indata.find('timereport')
    if report:
        rows = report.findall('reportrow')
    else :
        exit("No data in input file")

    anders = filter(lambda r: is_row_for(
        r, 'anders.bodelius@responsive.se'), rows)
    anders = list(anders)

    print('Writing...')
    tree = ET.Element('SalaryData')
    tree.set('ProgramName', 'td2tlu.py')
    tree.set('Created', datetime.date.today().strftime("%Y-%m-%d"))
    tree.set('CompanyName', 'Responsive AB')
    tree.set('OrgNo', '556565-8472')

    timecodes = ET.SubElement(tree, 'TimeCodes')
    ET.SubElement(timecodes, 'TimeCode', {
        'Code': '1', 'TimeCodeName': 'Sjukdom'})
    ET.SubElement(timecodes, 'TimeCode', {
        'Code': '2', 'TimeCodeName': 'VAB'})
    ET.SubElement(timecodes, 'TimeCode', {
        'Code': '3', 'TimeCodeName': 'Semester'})

    salary_data = ET.SubElement(tree, 'SalaryDataEmployee', {
        'FromDate': from_date, 'ToDate': to_date})
    employee = ET.SubElement(salary_data, 'Employee', {
        'EmploymentNo': '1', 'FirstName': 'Anders', 'LastName': 'Bodelius', 'FromDate': from_date, 'ToDate': to_date})
    ET.SubElement(employee, 'NormalWorkingTimes')

    print(ET.tostring(tree))
