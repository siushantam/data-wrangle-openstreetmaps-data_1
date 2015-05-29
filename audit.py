# -*- coding: utf-8 -*-

# This program is to spot the unexpected street types

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

# Filename and REGEX declaration
OSMFILE = "hong-kong_china.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# Define expected street types
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# Mapping to clean the data, e.g. changing "St" to "Street"
mapping = { "St": "Street",
            "St.": "Street",
            "Rd.": "Road",
            "Ave": "Avenue"
            }

# Define pprint to display utf-8 names
class MyPrettyPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)

# Add unexpected street type
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

# Validate if the tag stores the street name
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

# Main module to audit the XML file
def audit(osmfile):
    osm_file = open(osmfile, "r")
    # Declare the set for unexpected street types
    street_types = defaultdict(set)
    # Iterate all XML elements
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        # Audit only node and way elements
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    return street_types

# Update the street name according to the mapping above
def update_name(name, mapping):
    last_word = name.rsplit(' ', 1)[1]
    if last_word in mapping:
        name = name.replace(last_word, mapping[last_word])
    return name

def test():
    st_types = audit(OSMFILE)
    MyPrettyPrinter().pprint(dict(st_types))

if __name__ == '__main__':
    test()
