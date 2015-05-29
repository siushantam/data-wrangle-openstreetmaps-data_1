# -*- coding: utf-8 -*-

# This program is to get a feel what are the keys in the XML file
# and see if there are abnormal XMLs

import xml.etree.ElementTree as ET
import pprint

# Iterate the XML file and count the tags
def count_tags(filename):
    # Delcare the tags dict
    tags={}
    # Iterate the XML elements
    for event, elem in ET.iterparse(filename):
        if elem.tag in tags:
            tags[elem.tag]+=1
        else:
            tags[elem.tag]=1
    return tags

# Main module
def test():
    tags = count_tags('hong-kong_china.osm')
    pprint.pprint(tags)

if __name__ == "__main__":
    test()
