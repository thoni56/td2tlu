#/usr/bin/env python3

import sys
import shutil
from openpyxl import load_workbook
import datetime
import calendar
import lxml.etree as ET
import tdreader



def usage():
    print("Usage:   td2cambio <year>-<month> <xml-file>")
    print("Example: td2cambio 2020-02 Export.xml")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        usage()
        exit(1)
    
    # Year and month from argv
    year, month = sys.argv[1].split("-")
    year = int(year)
    month = int(month)
    month_name = calendar.month_name[month]

    # TBD check that year and month are integers

    # Create new file with correct name
    file_name = "Konsulttidrapport-"+sys.argv[1]+".xlsx"
    shutil.copyfile("Konsulttidrapport.xlsx", file_name)

    # Open workbook
    workbook = load_workbook(filename = file_name)
    sheet = workbook.active

    # The name of the activity in Timeduty should be the team followed by the
    # project number in parenthesis so that we can extract them automatically
    activity_name = "Java SDK Teamet (1234-1)"
    team = activity_name.split("(")[0].strip()
    projno = activity_name.split("(")[1].strip()[:-1]

    # Write month info and team
    sheet.cell(column=2, row=4, value=month_name+" "+str(year))
    sheet.cell(column=2, row=5, value=team)

    # Update rows for dates
    date = datetime.datetime(year, month, 1)
    for row in range(8, 39):
        sheet.cell(column=1, row=row, value=date)
        date = date + datetime.timedelta(days=1)

    # Fill project number
    sheet.cell(column=2, row=7, value=projno)

    # and hours from the xml-file
    indata = ET.parse(sys.argv[2])

    from_date, to_date, time_rows, expense_rows = tdreader.extract_data_from_xml(indata)

    # TODO check that from_date & to_date matches the month given as argument

    # Get all cambio project activities
    tdreader.filter_registrations_for_client(time_rows, "Cambio")
    

    # Close and exit
    workbook.save(file_name)
