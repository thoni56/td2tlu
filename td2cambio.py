#/usr/bin/env python3

import sys
import shutil
from openpyxl import load_workbook
import datetime
import calendar


def usage():
    print("Usage:   td2cambio <year>-<month>")
    print("Example: td2cambio 2020-02")

if __name__ == "__main__":
    if len(sys.argv) < 2:
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

    # The name of the activity should be the team followed by the project number in parenthesis
    # activity_name = "Java SDK Teamet (1234-1)"
    activity_name = "Java SDK Teamet (1234-1)"
    team = activity_name.split("(")[0].strip()
    projno = activity_name.split("(")[1].strip()[:-1]


    sheet.cell(column=2, row=4, value=month_name+" "+str(year))
    sheet.cell(column=2, row=5, value=team)

    # Update date list for rows
    date = datetime.datetime(year, month, 1)
    for row in range(8, 39):
        sheet.cell(column=1, row=row, value=date)
        date = date + datetime.timedelta(days=1)

    # Fill project number
    sheet.cell(column=2, row=7, value=projno)

    # and hours

    # Close and exit
    workbook.save(file_name)
