# Module to read an XML-file exported from Timeduty time reporting system (https://timeduty.com)
# and return date range and time and expense rows

import lxml.etree as ET

# API: extract data from an XML as it is returned from x xml parsers "parse" function
# Example usage: tdreader.extract_data_from_xml(lxml.etreee.parse(filename))
# Returns a tuple consisting of:
#   from_date : string YYYY-MM-DD
#   to_date : string YYYY-MM-DD
#   time_rows : list of XML-nodes which all are time registrations
#   expense_rows : list of XML-nodes which all are expense registrations
def extract_data_from_xml(indata):

    for setting in indata.iter('setting'):
        if 'FilterDateFrom' in setting.attrib.values():
            from_date = setting.attrib['value'].split(' ', 1)[0]
        if 'FilterDateTo' in setting.attrib.values():
            to_date = setting.attrib['value'].split(' ', 1)[0]

    time_report = indata.find('timereport')
    time_rows = time_report.findall(
        'reportrow') if time_report is not None else []

    expense_report = indata.find('expensereport')
    expense_rows = expense_report.findall(
        'reportrow') if expense_report is not None else []
    return (from_date, to_date, time_rows, expense_rows)

# Filter out registrations for a user (user.id = email as a string)
def filter_registrations_for_user(user, rows):
    registrations = filter(lambda r: is_row_for_user(
        r, user), rows)
    return list(registrations)

# Filter out registrations for a client (name as a string)
def filter_registrations_for_client(client, rows):
    registrations = filter(lambda r: is_row_for_client(
        r, client), rows)
    return list(registrations)

# Filter out registrations for a project (name as a string)
def filter_registrations_for_project(project, rows):
    registrations = filter(lambda r: is_row_for_project(
        r, project), rows)
    return list(registrations)

# Get registered time for a registration
# Most used is as decimal values, so that is the default
def get_time(row):
    return convert_hour_and_minute_as_string_to_fractional_hour(row.find('reportedtime').text)

def get_time_as_string(row):
    return row.find('reportedtime').text

# Internal
def is_row_for_user(row, user):
    return row.find('username').text == user

def is_row_for_client(row, client):
    return row.find('client').text == client

def is_row_for_project(row, project):
    return row.find('project').text == project

def convert_hour_and_minute_as_string_to_fractional_hour(time):
    fields = time.split(":")
    hours = fields[0] if len(fields) > 0 else 0.0
    minutes = fields[1] if len(fields) > 1 else 0.0
    value = float(hours) + (float(minutes) / 60.0)
    return "{0:.2f}".format(value).rstrip('0').rstrip('.')