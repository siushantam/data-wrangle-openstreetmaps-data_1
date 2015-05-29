#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This program is to transform the OSM file to json file for MongoDB import
# Data cleaning is also done here

import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json

# REGEX check declaration
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# XML keys to be put under the created sub-document
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

# Street types to be ignored, found from audit.py
IGNORED_ST = [ "61-63", "Amizade", "Barbosa", "Cinatti", "Coimbra", "Dadao",
           "District", "Felicidade", "Gaio", "Glenealy", "Guimarães",
           "Industrial", "It", "Keng", "Lacerda", "Load", "Lu", "Mau",
           "Mesquita", "Negra", "Oceano", "Olímpica", "On", "Patane",
           "Patos", "Pereira", "Pinto", "Prosperidade", "Ranch",
           "Regedor", "República", "S.", "Seca", "Sen", "Silva", "Sul",
           "Tranquilidade", "Twisk", "Verde", "Vitória"]

# City to be ignored, found from audit.py
IGNORED_CI = [ "Zhuhai", "Shenzhen", "guangzhou" ]

# Mapping to clean the data, e.g. changing "St" to "Street"
mapping = { "St": "Street",
            "St.": "Street",
            "Rd.": "Road",
            "Av": "Avenue",
            "Ave": "Avenue"
            }

# Validate if the node is indeed a Hong Kong location
def is_hongkong(node):
    # Filter street type
    if 'address' in node:
        if 'street' in node.get('address', {}):
            try:
                last_word = node['address']['street'].rsplit(' ', 1)[1]
                if last_word in IGNORED_ST:
                    return False
            except:
                pass
        # Filter city
        if 'city' in node.get('address', {}):
            if node["address"]["city"] in IGNORED_CI:
                return False
    # Filter phone
    if 'phone' in node:
        if node["phone"][:3] == "+86":
            return False
        elif node["phone"][:4] == "+853":
            return False
        elif node["phone"][:2] == "86":
            return False
        elif node["phone"][:3] == "075":
            return False
        elif node["phone"][:3] == "020":
            return False
    # Pass all check
    return True

# Validate if the tag stores the street name            
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

# Update the street name according to the mapping above
def update_name(name, mapping):
    try:
        last_word = name.rsplit(' ', 1)[1]
        if last_word in mapping:
            name = name.replace(last_word, mapping[last_word])
    except:
        pass
    return name

# The module to change one XML object to json
def shape_element(element):
    # Declare the base of json
    node = {}
    node['created'] = {}
    latv=1000 # initialize with invalid values
    lonv=1000
    
    # Shape only node and way in the XML
    if element.tag == "node" or element.tag == "way" :
        node['type'] = element.tag
        # Shape position
        for key, value in element.attrib.iteritems():
            if key == 'lat':
                latv = float(value)
            elif key == 'lon':
                lonv = float(value)
            elif key in CREATED:
                node['created'][key] = value
            else:
                node[key] = value
        if latv!=1000 and lonv!=1000: 
            node['pos'] = [latv, lonv]
        # Shape other keys in node
        for tag in element.iter("tag"):
            # Ignore problematic keys
            if problemchars.match(tag.attrib['k']):
                pass
            elif tag.attrib['k'][:5] == "addr:":
                # address field
                if ":" in tag.attrib['k'][5:]:
                    # address field more than one colon, ignore
                    pass
                else:
                    if "address" not in node:
                        # create dict
                        node['address']={}
                    # check if we need to update street name
                    if is_street_name(tag):
                        tag.attrib['v'] = update_name(tag.attrib['v'], mapping)
                    node['address'][tag.attrib['k'][5:]]=tag.attrib['v']
            elif ":" in tag.attrib['k']:
                # other fields with colon
                temp = tag.attrib['k'].split(":")
                node[temp[0]]={}
                node[temp[0]][temp[1]]=tag.attrib['v']
            else:
                # other fields without colon
                node[tag.attrib['k']]=tag.attrib['v']
        # Shape way specific keys
        if element.tag=="way":
            node['node_refs']=[]
        for nd in element.iter("nd"):
            node['node_refs'].append(nd.attrib['ref'])

        return node
    else:
        return None

# Module to iterate all XML objects then write to .json file
def process_map(file_in, pretty = False):
    # Define file name
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        # Iterate XML objects
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                if is_hongkong(el):
                    data.append(el)
                    if pretty:
                        fo.write(json.dumps(el, indent=2)+"\n")
                    else:
                        fo.write(json.dumps(el) + "\n")
    return data

def test():
    data = process_map('hong-kong_china.osm', True)

if __name__ == "__main__":
    test()