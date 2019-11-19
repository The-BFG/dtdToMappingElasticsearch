#!/usr/bin/python3
import sys, time
import json
from lxml import etree


def dtdtodict(dtd_in):
    '''Read the .dtd file and create a dictionary to dump with json.dumps'''
    mapping = {'properties':{}}
    keyword =  {'comment': ['<!--', '-->'],
                'element': ['<!ELEMENT', '>'],
                'attlist': ['<!ATTLIST', '>'],
                'entity': ['<!ENTITY', '>'],
                'notation': ['<!NOTATION', '>']}
    entity = {}
    with open(dtd_in, 'r') as dtd_file:
        dtd = etree.DTD(dtd_file)
        for element in dtd.iterelements():
            print(element.content)
            if element.content is not None:
                fields = []
                content = element.content
                while content.right is not None:
                    fields.append(content.left.name)
                    content = content.right
                if()
                fields.append(content.name)
                print(fields)
            for attribute in element.iterattributes():
                print(attribute.elemname,"\t", attribute.name )
                for value in attribute.itervalues():
                    print(element.name,":",dir(value))
            
        # line = dtd_file.readline()
        # while line:
        #     #print(line)
        #     line.strip()
        #     if line.startswith(keyword['comment'][0]):
        #         if line.endswith(keyword['comment'][1]):
        #             line = dtd_file.readline()
        #         elif keyword['comment'][1] in line:
        #             line = line.split(keyword['comment'][1], 1)[1:]
        #         else:
        #             while keyword['comment'][1] not in line:
        #                 line = dtd_file.readline()
        #                 #print(line)
        #                 if line.endswith(keyword['comment'][1]):
        #                     line = dtd_file.readline()
        #                 elif keyword['comment'][1] in line:
        #                     line = line.split(keyword['comment'][1], 1)[1:]
        #                     line = "".join(line)
        #                     time.sleep(.1)
        #                 print(line)
        #     elif line.startswith(keyword['element'][0]):
        #         pass
        #     elif line.startswith(keyword['attlist'][0]):
        #         pass
        #     elif line.startswith(keyword['entity'][0]):
        #         #content = line.partition('"')
        #         #print(line.partition('"'))
        #     elif line.startswith(keyword['notation'][0]):
        #         pass
        #     else:
        #         line = dtd_file.readline()
    return mapping

def dicttojson(mapping_out, mapping_json):
    '''Write the .json file that contain the mapping for elasticsearch'''
    with open(mapping_out, 'w') as mapping_file:
        mapping_file.write(mapping_json)

def dtdtomapping(dtd_in, mapping_out="mapping.json"):
    '''dtdtomapping get a .dtd file and construct the JSON mapping for Elasticsearch'''
    mapping = dtdtodict(dtd_in)
    #mapping_json = json.dumps(mapping, indent=4)
    #dicttojson(mapping_out, mapping_json)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        dtdtomapping(sys.argv[1])
    elif len(sys.argv) == 3:
        dtdtomapping(sys.argv[1], sys.argv[2])
