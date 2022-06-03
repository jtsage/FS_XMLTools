# pylama:ignore=W605,E221,C901
"""
        __ ______     __     _   _
        /    /      /    )   /  /|              /       /   ,
-------/----/-------\-------/| /-|----__----__-/----__-/--------__----__-
      /    /         \     / |/  |  /   ) /   /   /   /   /   /   ) /   )
_(___/____/______(____/___/__/___|_(___/_(___/___(___/___/___/___/_(___/_
                                                                      /
    i3dMapperReplacer.py - v1.0.2                                 (_ /

Version History:
 v1.0.2 - Initial Release
"""

import argparse
import xml.etree.ElementTree as ET
import os
import subprocess
import sys
import re


def is_numeric_node(value):
    """ See if it's a numeric based node or text"""
    return re.fullmatch("\d>[0-9|]*", value) is not None


def enter_key_exit():
    """ Exit when enter key pressed """
    print("Press ENTER to close terminal.")
    try:
        input()
    except BaseException:
        pass
    exit()


print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
print("  i3dMapperReplacer v1.0.2")
print("    by JTSModding")
print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")

parser = argparse.ArgumentParser(
    description='Change any index based mapping to named mapping in an XML'
)
parser.add_argument('file', metavar='file', nargs=1, type=argparse.FileType('r', encoding='utf-8'))

try:
    args = parser.parse_args()
except BaseException:
    enter_key_exit()

try:
    thisShopItemXML = ET.fromstring(args.file[0].read())
    args.file[0].close()
except BaseException:
    print("ERROR: Unable to read / parse file '" + os.path.basename(args.file[0].name) + "'")
    enter_key_exit()

thisShopItemFile   = os.path.basename(args.file[0].name)
thisShopItemFolder = os.path.dirname(os.path.abspath(args.file[0].name))
baseDrive          = os.path.splitdrive(thisShopItemFolder)
thisShopItemAbs    = os.path.normpath(os.path.join(baseDrive[0], baseDrive[1], thisShopItemFile))
i3dFileAbs         = ""
mapCache           = {}

try:
    ET.tostring(thisShopItemXML, encoding='unicode')
    for thisTag in thisShopItemXML.findall(".//base/filename"):
        if thisTag.text is None:
            raise Exception("NOT FOUND: i3d File Not Found in XML")
        i3dFileAbs = os.path.normpath(os.path.join(baseDrive[0], baseDrive[1], thisTag.text))

    if not os.path.isfile(i3dFileAbs):
        raise Exception("NOT FOUND: i3d File Not Found")

    i3dMap = subprocess.run([
        sys.executable,
        'i3dMapper.py',
        '--no-pretty-print',
        i3dFileAbs
    ], stdout=subprocess.PIPE)

    i3dMapping = ET.fromstring(i3dMap.stdout)

    for thisMap in i3dMapping.findall(".//i3dMapping"):
        mapCache[thisMap.attrib["node"]] = thisMap.attrib["id"]

    for thisType in ["node", "repr", "startNode", "endNode", "linkNode", "jointNode"]:
        for thisTag in thisShopItemXML.findall(".//*[@" + thisType + "]"):
            if thisTag.tag != "i3dMapping":
                myNode = thisTag.attrib[thisType]
                if is_numeric_node(myNode):
                    if myNode in mapCache.keys():
                        thisTag.attrib[thisType] = mapCache[myNode]
                    else:
                        print("WARNING: numeric node " + myNode + " does not exist in i3d file!")

    thisShopItemI3D = thisShopItemXML.find(".//i3dMappings")

    if thisShopItemI3D is not None:
        print("FOUND: i3dMappings Section, re-writing")
        for child in list(thisShopItemI3D):
            thisShopItemI3D.remove(child)

        for thisMap in i3dMapping.findall(".//i3dMapping"):
            thisShopItemI3D.append(thisMap)
    else:
        print("NOT FOUND: i3dMappings Section, creating one instead")
        thisShopItemXML.append(i3dMapping)

    ET.indent(thisShopItemXML, space='    ')
    storeXML_string = ET.tostring(thisShopItemXML, encoding='unicode')
    storeXML_string = storeXML_string.replace("&gt;", ">")
    storeXML_string = "<?xml version='1.0' encoding='utf-8'?>\n" + storeXML_string

    xmlWriter = open(thisShopItemAbs, "w")
    xmlWriter.write(storeXML_string)
    xmlWriter.close()

    print("SUCCESS: re-wrote xml file!")

except AssertionError as err:
    print("UNRECOVERABLE ERROR: " + str(err))

if sys.stdout.isatty():
    # Don't pause on finish if we re-directed to a file.
    enter_key_exit()
