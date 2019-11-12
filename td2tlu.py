#! /usr/bin/env python3

import xml.etree.ElementTree as ET
import argparse


class TimereportConverter():
    def __init__(self):
        pass


if (__name__ == "__main__"):

    argparser = argparse.ArgumentParser(
        description='Convert XML output from Timeduty to TLU format XML.')
    argparser.add_argument('file', help='the name of the XML export file')

    args = argparser.parse_args()

    indata = ET.parse(args.file)
