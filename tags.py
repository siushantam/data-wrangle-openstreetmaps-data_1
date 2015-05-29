# -*- coding: utf-8 -*-

# This program is to audit the "key" in tag and see if they are valid

import xml.etree.ElementTree as ET
import pprint
import re

# REGEX check declaration
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# Count the keys which meet one of the REGEX checks
def key_type(element, keys):
    if element.tag == "tag":
        if lower.match(element.attrib['k']):
            keys['lower']+=1
        elif lower_colon.match(element.attrib['k']):
            keys['lower_colon']+=1
        elif problemchars.match(element.attrib['k']):
            keys['problemchars']+=1
        else:
            keys['other']+=1
    return keys

# Main module to iterate all XML objects to check the keys
def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)
    return keys

def test():
    keys = process_map('hong-kong_china.osm')
    pprint.pprint(keys)

if __name__ == "__main__":
    test()