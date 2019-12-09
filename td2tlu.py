#! /usr/bin/env python3

import lxml.etree as ET
import argparse
import datetime


class TimereportConverter():
    def __init__(self):
        pass

    def convert(self, file):
        print('Reading...')
        if not file:
            return None
        indata = ET.parse(file)
        for setting in indata.iter('setting'):
            if 'FilterDateFrom' in setting.attrib.values():
                from_date = setting.attrib['value'].split(' ', 1)[0]
            if 'FilterDateTo' in setting.attrib.values():
                to_date = setting.attrib['value'].split(' ', 1)[0]

        report = indata.find('timereport')
        if report is not None:
            rows = report.findall('reportrow')
            # TODO For now, collect all data for Anders
            anders = filter(lambda r: is_row_for(
                r, 'anders.bodelius@responsive.se'), rows)
            anders = list(anders)
        else :
            anders = None

        print('Writing...')
        salary_data = ET.Element('SalaryData')
        salary_data.set('ProgramName', 'td2tlu.py')
        salary_data.set('Created', datetime.date.today().strftime("%Y-%m-%d"))
        salary_data.set('CompanyName', 'Responsive AB')
        salary_data.set('OrgNo', '556565-8472')

        timecodes = ET.SubElement(salary_data, 'TimeCodes')
        ET.SubElement(timecodes, 'TimeCode', {
            'Code': '1', 'TimeCodeName': 'Sjukdom'})
        ET.SubElement(timecodes, 'TimeCode', {
            'Code': '2', 'TimeCodeName': 'VAB'})
        ET.SubElement(timecodes, 'TimeCode', {
            'Code': '3', 'TimeCodeName': 'Semester'})

        if anders is not None:
            ET.SubElement(salary_data, 'SalaryDataEmployee', {
                'FromDate': from_date, 'ToDate': to_date})
            employee = ET.SubElement(salary_data, 'Employee', {
                'EmploymentNo': '1', 'FirstName': 'Anders', 'LastName': 'Bodelius', 'FromDate': from_date, 'ToDate': to_date})
            ET.SubElement(employee, 'NormalWorkingTimes')
            ET.SubElement(employee, 'TimeAdjustments')
            ET.SubElement(employee, 'TimeBalance')
            ET.SubElement(employee, 'RegOutlays')
        return salary_data


def is_row_for(row, user):
    u = row.find('username')
    return u.text == user


if (__name__ == "__main__"):

    argparser = argparse.ArgumentParser(
        description='Convert XML output from Timeduty to TLU format XML.')
    argparser.add_argument(
        'file', help='name of the XML file from TimeDuty')

    args = argparser.parse_args()

    converter = TimereportConverter()
    tree = converter.convert(args.file)

    print(ET.tostring(tree, pretty_print=True).decode())