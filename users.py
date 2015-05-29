# -*- coding: utf-8 -*-

# This program is to find the users who ever contributed to the area

import xml.etree.ElementTree as ET
import pprint
import re

def get_user(element):
    return

def process_map(filename):
    # Declare the set for users
    users = set()
    # Iterate all XML elements and extract the user name
    for _, element in ET.iterparse(filename):
        if element.tag=="node":
            users.add(element.attrib['user'])
    return users

def test():
    users = process_map('hong-kong_china.osm')
    pprint.pprint(users)

if __name__ == "__main__":
    test()
