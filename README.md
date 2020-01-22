# TD2TLU

This python program takes an XML-file produced by the timereporting application
Timeduty.com (in the reporting section) and converts the absence records to
the TLU format used by Visma Lön.

## Procedure

Create a report in Timeduty using whatever parameters you want. Often the time
period is enough, since `td2tlu` will filter out absence records from the data.

Press the XML icon to produce and download an XML-file.

Bring up a command line and run `td2tlu` on that file:

    td2tlu <export file>

`td2tlu` will present the converted output on the standard output, so best to
save it to a file, e.g.

    td2tlu ExportReport.xml > absence_jan_2020.tlu

The resulting file can be directly imported into Visma Lön.

## Limitations

As this was created specifically for Responsive AB (https://responsive.se) all
conversion data is in the source code. If you want to use `td2tlu` you should change

`timecode_table`: table mapping activity names (for absence) to Visma timecodes

`user_table`: mapping Timeduty userid (email) to Visma employee code and names

Obviously this should be factored out to command line options pointing to files
instead. Merge Requests are welcome.
