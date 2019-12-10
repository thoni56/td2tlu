#! /usr/bin/env python3

import lxml.etree as ET
import argparse
import datetime


class User():
    def __init__(self, id, number, first, last):
        self.id = id
        self.number = number
        self.first = first
        self.last = last

class TimereportConverter():

    timecodes = {
        'Sjukdom':'1',
        'VAB':'2',
        'Semester':'3'
    }

    def generate_timecodes(self):
        timecodes = ET.Element('TimeCodes')
        # TODO create from timecode table
        ET.SubElement(timecodes, 'TimeCode', {
            'Code': '1', 'TimeCodeName': 'Sjukdom'})
        ET.SubElement(timecodes, 'TimeCode', {
            'Code': '2', 'TimeCodeName': 'VAB'})
        ET.SubElement(timecodes, 'TimeCode', {
            'Code': '3', 'TimeCodeName': 'Semester'})
        return timecodes

    users = [
        User('thomas.nilefalk@responsive.se', '102', 'Thomas', 'Nilefalk'),
        User('roger.magnesved@responsive.se', '105', 'Roger', 'Magnesved'),
        User('anders.bodelius@responsive.se', '107', 'Anders', 'Bodelius'),
        User('joakim.sarehag@responsive.se', '112', 'Joakim', 'Särehag'),
    ]

    def timecode_lookup(self, activity_name):
        return self.timecodes[activity_name]

    def __init__(self, timecodes=None, users=None):
        if timecodes is not None:
            self.timecodes = timecodes
        if users is not None:
            self.users = users

    def convert(self, file, creation_date=datetime.date.today().strftime("%Y-%m-%d")):
        if not file:
            return None
        indata = ET.parse(file)
        for setting in indata.iter('setting'):
            if 'FilterDateFrom' in setting.attrib.values():
                from_date = setting.attrib['value'].split(' ', 1)[0]
            if 'FilterDateTo' in setting.attrib.values():
                to_date = setting.attrib['value'].split(' ', 1)[0]

        salary_data = ET.Element('SalaryData')
        salary_data.set('ProgramName', 'td2tlu.py')
        salary_data.set('Created', creation_date)
        salary_data.set('CompanyName', 'Responsive AB')
        salary_data.set('OrgNo', '556565-8472')

        timecodes = self.generate_timecodes()
        salary_data.append(timecodes)

        report = indata.find('timereport')
        if report is not None:
            rows = report.findall('reportrow')

            salary_data_employee = ET.SubElement(salary_data, 'SalaryDataEmployee', {
                'FromDate': from_date, 'ToDate': to_date})
            for user in self.users:
                # TODO For now, collect all data for Anders (user[0])
                registrations = filter(lambda r: is_row_for(
                    r, user.id), rows)
                registrations = list(registrations)

                # TODO Filter out only registrations with "interesting" timecodes

                if len(registrations) > 0:
                    employee = ET.SubElement(salary_data_employee, 'Employee', {
                        'EmploymentNo': user.number, 'FirstName': user.first, 'Name': user.last, 
                        'FromDate': from_date, 'ToDate': to_date})
                    ET.SubElement(employee, 'NormalWorkingTimes')
                    times = ET.SubElement(employee, 'Times')
                    for registration in registrations:
                        try:
                            timecode = self.timecode_lookup(registration.find('activityname').text)
                            time = ET.SubElement(times, 'Time')
                            time.set('DateOfReport', registration.find('date').text)
                            time.set('TimeCode', timecode)
                            time.set('SumOfHours', registration.find('reportedtime').text)
                        except:
                            pass # Did not find that activity, so ignore it
                    ET.SubElement(employee, 'TimeAdjustments')
                    ET.SubElement(employee, 'TimeBalances')
                    ET.SubElement(employee, 'RegOutlays')

        return ET.tostring(salary_data, pretty_print=True,
                    doctype='<?xml version="1.0" encoding="ISO-8859-1"?>').decode()


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
    output = converter.convert(args.file)

    print(output)