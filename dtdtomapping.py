#!/usr/bin/python3
import sys, time
import json
from lxml import etree


NON_IMPORTANT_ELEMENTS = ["dblp","author", "editor", "title", "booktitle", "pages", "year", "address", "journal", "volume", "number", "month", "url", "ee", "cdrom", "cite", "publisher", "note", "crossref", "isbn", "series", "school", "chapter", "publnr", "ref", "sup", "sub", "i", "tt"]
text_type = {"type":"text", "fields":{"keyword":{"type":"keyword", "ignore_above":256}}}
date_type = {"type":"date"}

def try_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


def dtdtodict(dtd_in):
    '''Read the .dtd file and create a dictionary to dump with json.dumps'''
    mapping = {'properties':{}}
    elements = {}

    with open(dtd_in, 'r') as dtd_file:
        dtd = etree.DTD(dtd_file)
        #Gestione Elementi
        for element in dtd.iterelements():
            elements[element.name] = {"attributes":[], "fields":[]}
            # Gestione dei campi
            if element.content is not None:
                fields = []
                content = element.content
                while content.right is not None:
                    if content.left.name is None:
                        fields.append("#text")
                    else:
                        fields.append(content.left.name)
                    content = content.right
                if content.name is None:
                    fields.append("#text")
                else:
                    fields.append(content.name)
                elements[element.name]["fields"] = fields
            # Gestione Attributi
            attributes = []
            for attribute in element.iterattributes():
                attributes.append(attribute.name)
            elements[element.name]["attributes"] = attributes

    print("Scanning element:", end=" ")
    for element in elements:
        # print(element)
        # print("\tAttributes: ", elements[element]["attributes"])
        # print("\tFields: ", elements[element]["fields"])
        mapping["properties"][element] = {"properties":{}}
        for attribute in elements[element]["attributes"]:
            if "date" in attribute:
                mapping["properties"][element]["properties"]["@"+str(attribute)] = date_type
            else:
                mapping["properties"][element]["properties"]["@"+str(attribute)] = text_type

        for field in elements[element]["fields"]:
            if field in elements.keys():
                mapping["properties"][element]["properties"][str(field)] = {}
            else:
                mapping["properties"][element]["properties"][str(field)] = text_type
    print("OK")
    print("Updating main element with subelement:", end=" ")
    for element in elements:
        for subelement in elements[element]["fields"]:
            if "#text" not in str(subelement):
                mapping["properties"][element]["properties"][str(subelement)] = mapping["properties"][subelement]
    print("OK")
    return mapping

def dicttojson(mapping_out, mapping_json):
    '''Write the .json file that contain the mapping for elasticsearch'''
    with open(mapping_out, 'w') as mapping_file:
        mapping_file.write(mapping_json)

def delsubelement(mapping, ):
    for element in NON_IMPORTANT_ELEMENTS:
        del mapping["properties"][element]
    return mapping

def dtdtomapping(dtd_in, mapping_out="mapping.json"):
    '''dtdtomapping get a .dtd file and construct the JSON mapping for Elasticsearch'''
    mapping = dtdtodict(dtd_in)

    print("Deleting non-main elements:", end=" ")
    mapping = delsubelement(mapping)
    print("OK")

    print("Creating json mapping:", end=" ")
    mapping_json = json.dumps(mapping, indent=4)
    print("OK")
    #print(mapping_json)

    print("Writing ", mapping_out, end=": ")
    dicttojson(mapping_out, mapping_json)
    print("OK")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        dtdtomapping(sys.argv[1])
    elif len(sys.argv) == 3:
        dtdtomapping(sys.argv[1], sys.argv[2])
