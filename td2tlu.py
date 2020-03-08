#! /usr/bin/env python3

# A converter between the XML format from Timeduty (https://timeduty.com) and
# the TLU format used by Visma Lön 600. The format for a TLU file is described
# at https://www.vismaspcs.se/visma-support/visma-lon-600/content/online-help/filformat-tidsredovisningsfil.htm
#
# This hack was programmed specifically for handling absence @ Responsive Development Technologies by Thomas Nilefalk

import lxml.etree as ET
import argparse
import datetime
import sys
import tdreader


class User():
    def __init__(self, id, number, first, last):
        self.id = id
        self.number = number
        self.first = first
        self.last = last


class Timeduty2TluConverter():

    timecode_table = {
        'Semester': '040',
        'Sjuk': '050',
        'Sjukdom': '050',
        'VAB': '060',
        'Föräldraledig': '070',
        'Föräldraledighet': '070',
        'Tjänstledig': '090',
        'Tjänstledighet': '090',
    }

    user_table = [
        User('thomas.nilefalk@responsive.se', '102', 'Thomas', 'Nilefalk'),
        User('roger.magnesved@responsive.se', '105', 'Roger', 'Magnesved'),
        User('anders.bodelius@responsive.se', '107', 'Anders', 'Bodelius'),
        User('joakim.sarehag@responsive.se', '112', 'Joakim', 'Särehag'),
    ]

    def generate_timecodes(self):
        timecodes = ET.Element('TimeCodes')
        last_timecode = ''
        for name, code in self.timecode_table.items():
            if not code == last_timecode:
                ET.SubElement(timecodes, 'TimeCode', {
                    'Code': code, 'TimeCodeName': name})
                last_timecode = code
        return timecodes

    def timecode_lookup(self, activity_name):
        return self.timecode_table[activity_name]

    def __init__(self, timecodes=None, users=None):
        if timecodes is not None:
            self.timecode_table = timecodes
        if users is not None:
            self.user_table = users

    def convert_to_tlu(self, file, creation_date=datetime.date.today().strftime("%Y-%m-%d")):
        if not file:
            return None

        indata = ET.parse(file)

        from_date, to_date, time_rows, expense_rows = tdreader.extract_data_from_xml(
            indata)

        salary_data = ET.Element('SalaryData')
        salary_data.set('ProgramName', 'td2tlu.py')
        salary_data.set('Created', creation_date)
        salary_data.set('CompanyName', 'Responsive AB')
        salary_data.set('OrgNo', '556565-8472')

        timecodes = self.generate_timecodes()
        salary_data.append(timecodes)
        salary_data_employee = ET.SubElement(salary_data, 'SalaryDataEmployee', {
            'FromDate': from_date, 'ToDate': to_date})

        for user in self.user_table:

            time_registrations = tdreader.filter_registrations_for_user(
                user.id, time_rows)

            expense_registrations = tdreader.filter_registrations_for_user(
                user.id, expense_rows)

            if len(time_registrations) > 0 or len(expense_registrations):
                employee = ET.SubElement(salary_data_employee, 'Employee', {
                    'EmploymentNo': user.number, 'FirstName': user.first, 'Name': user.last,
                    'FromDate': from_date, 'ToDate': to_date})

                # No data for normal working times but node is required
                ET.SubElement(employee, 'NormalWorkingTimes')

                # Time registrations
                times = ET.Element('Times')
                for time_registration in time_registrations:
                    registration = self.time_from_registration(
                        time_registration)
                    if registration is not None:
                        times.append(registration)
                employee.append(times)

                # No time adjustments(?) or balances
                ET.SubElement(employee, 'TimeAdjustments')
                ET.SubElement(employee, 'TimeBalances')

                # Expense registrations
                expenses = ET.Element('RegOutlays')
                for expense_registration in expense_registrations:
                    expense = self.expense_from_registration(
                        expense_registration)
                    expenses.append(expense)
                employee.append(expenses)

        return ET.tostring(salary_data, pretty_print=True, encoding="iso-8859-1")

    def expense_from_registration(self, registration):
        expense_element = ET.Element('RegOutlay')
        expense_element.set('DateOfReport', tdreader.get_date(registration))
        expense_element.set('OutlayCodeName', '')
        expense_element.set('OutlayType', '')
        expense_element.set('NoOfPrivate', '')
        expense_element.set('Unit', '')
        expense_element.set('SumOfPrivate', registration.find('amount').text)
        expense_element.set(
            'OutlayCodeName', registration.find('description').text)
        return expense_element

    def time_from_registration(self, registration):
        activity_name = registration.find(
            'activityname').text
        try:
            timecode = self.timecode_lookup(activity_name)
            time_element = ET.Element('Time')
            time_element.set('DateOfReport', tdreader.get_date(registration))
            time_element.set('TimeCode', timecode)
            time_element.set('SumOfHours', tdreader.get_time(registration))
        except:
            # Did not find that activity, print a warning
            print(
                "WARNING! Unknown activity '{}' - ignored".format(activity_name), file=sys.stderr)
            time_element = None
        return time_element


if (__name__ == "__main__"):

    argparser = argparse.ArgumentParser(
        description='Convert XML output from Timeduty to TLU format XML.')
    argparser.add_argument(
        'inputfile', help='name of the XML file from TimeDuty')
    argparser.add_argument(
        'outputfile', help='name of the TLU file to create')

    args = argparser.parse_args()

    converter = Timeduty2TluConverter()
    output = converter.convert_to_tlu(args.inputfile)

    with open(args.outputfile, 'wb') as file:
        file.write(output)
