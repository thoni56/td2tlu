#! /usr/bin/env python3

import xml.sax
import argparse


class TimereportHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""
        self.type = ""
        self.format = ""
        self.year = ""
        self.rating = ""
        self.stars = ""
        self.description = ""

    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "movie":
            print("*****Movie*****")
            title = attributes["title"]
            print("Title:", title)


if (__name__ == "__main__"):

    argparser = argparse.ArgumentParser(
        description='Convert XML output from Timeduty to TLU format XML.')
    argparser.add_argument('file', help='the name of the XML export file')

    args = argparser.parse_args()

    xmlparser = xml.sax.make_parser()
    Handler = TimereportHandler()
    xmlparser.setContentHandler(Handler)
    xmlparser.parse("simple.xml")
