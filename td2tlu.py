#! /usr/bin/env python3

# A converter between the XML format from Timeduty (https://timeduty.com) and
# the TLU format used by Visma Lön 600. The format for a TLU file is described
# at https://www.vismaspcs.se/visma-support/visma-lon-600/content/online-help/filformat-tidsredovisningsfil.htm
#
# This hack was programmed specifically for Responsive Development Technologies by Thomas Nilefalk

import lxml.etree as ET
import argparse
import datetime
import sys


class User():
    def __init__(self, id, number, first, last):
        self.id = id
        self.number = number
        self.first = first
        self.last = last


class TimereportConverter():

    timecode_table = {
        'Semester': '040',
        'Sjuk': '050',
        'VAB': '060',
        'Föräldraledig': '070',
        'Tjänstledig': '090',
    }

    user_table = [
        User('thomas.nilefalk@responsive.se', '102', 'Thomas', 'Nilefalk'),
        User('roger.magnesved@responsive.se', '105', 'Roger', 'Magnesved'),
        User('anders.bodelius@responsive.se', '107', 'Anders', 'Bodelius'),
        User('joakim.sarehag@responsive.se', '112', 'Joakim', 'Särehag'),
    ]

    def generate_timecodes(self):
        timecodes = ET.Element('TimeCodes')
        for name, code in self.timecode_table.items():
            ET.SubElement(timecodes, 'TimeCode', {
                'Code': code, 'TimeCodeName': name})
        return timecodes

    def timecode_lookup(self, activity_name):
        return self.timecode_table[activity_name]

    def __init__(self, timecodes=None, users=None):
        if timecodes is not None:
            self.timecode_table = timecodes
        if users is not None:
            self.user_table = users

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

        time_report = indata.find('timereport')
        time_rows = time_report.findall(
            'reportrow') if time_report is not None else []

        expense_report = indata.find('expensereport')
        expense_rows = expense_report.findall(
            'reportrow') if expense_report is not None else []

        salary_data_employee = ET.SubElement(salary_data, 'SalaryDataEmployee', {
            'FromDate': from_date, 'ToDate': to_date})
        for user in self.user_table:

            # We will only handle absense, not other types of time registrations
            absence_registrations = self.extract_absence_registrations(user, time_rows)

            expense_registrations = self.extract_expense_registrations(user, expense_rows)

            if len(absence_registrations) > 0 or len(expense_registrations):
                employee = ET.SubElement(salary_data_employee, 'Employee', {
                    'EmploymentNo': user.number, 'FirstName': user.first, 'Name': user.last,
                    'FromDate': from_date, 'ToDate': to_date})

                # No data for normal working times but node is required
                ET.SubElement(employee, 'NormalWorkingTimes')

                # Absence registrations
                times = ET.Element('Times')
                for absence_registration in absence_registrations:
                    absence = self.time_from_registration(absence_registration)
                    times.append(absence)
                employee.append(times)

                # No time adjustments(?) or balances
                ET.SubElement(employee, 'TimeAdjustments')
                ET.SubElement(employee, 'TimeBalances')

                # Expense registrations
                expenses = ET.Element('RegOutlays')
                for expense_registration in expense_registrations:
                    expense = self.expense_from_registration(expense_registration)
                    expenses.append(expense)
                employee.append(expenses)

        return ET.tostring(salary_data, pretty_print=True,
                           doctype='<?xml version="1.0" encoding="ISO-8859-1"?>').decode()

    def expense_from_registration(self, expense_registration):
        reg_outlay = ET.Element('RegOutlay')
        reg_outlay.set('DateOfReport',
                       expense_registration.find('date').text)
        reg_outlay.set('OutlayCodeName', '')
        reg_outlay.set('OutlayType', '')
        reg_outlay.set('NoOfPrivate', '')
        reg_outlay.set('Unit', '')
        reg_outlay.set('SumOfPrivate', expense_registration.find('amount').text)
        reg_outlay.set('OutlayCodeName', expense_registration.find('description').text)
        return reg_outlay

    def time_from_registration(self, absence_registration):
        activity_name = absence_registration.find(
            'activityname').text
        try:
            timecode = self.timecode_lookup(activity_name)
            time = ET.Element('Time')
            time.set('DateOfReport',
                     absence_registration.find('date').text)
            time.set('TimeCode', timecode)
            time_in_fractions = convert_time_to_decimal(
                absence_registration.find('reportedtime').text)
            time.set('SumOfHours', time_in_fractions)
        except:
            # Did not find that activity, print a warning
            print(
                "WARNING! Unknown absence activity - '{}' ignored".format(activity_name), file=sys.stderr)
        return time

    def extract_expense_registrations(self, user, expense_rows):
        expense_registrations = filter(lambda r: is_row_for(
            r, user.id), expense_rows)
        expense_registrations = list(expense_registrations)
        return expense_registrations

    def extract_absence_registrations(self, user, time_rows):
        time_registrations = self.extract_expense_registrations(user, time_rows)
        absence_registrations = list(
            filter(is_absence_registration, time_registrations))
        return absence_registrations


def is_row_for(row, user):
    u = row.find('username')
    return u.text == user


def is_absence_registration(registration):
    return registration.find('project').text == "Frånvaro"


def convert_time_to_decimal(time):
    fields = time.split(":")
    hours = fields[0] if len(fields) > 0 else 0.0
    minutes = fields[1] if len(fields) > 1 else 0.0
    value = float(hours) + (float(minutes) / 60.0)
    return "{0:.2f}".format(value).rstrip('0').rstrip('.')


if (__name__ == "__main__"):

    argparser = argparse.ArgumentParser(
        description='Convert XML output from Timeduty to TLU format XML.')
    argparser.add_argument(
        'file', help='name of the XML file from TimeDuty')

    args = argparser.parse_args()

    converter = TimereportConverter()
    output = converter.convert(args.file)

    print(output)
