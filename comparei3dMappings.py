# pylama:ignore=W605,E221,C901
"""
        __ ______     __     _   _
        /    /      /    )   /  /|              /       /   ,
-------/----/-------\-------/| /-|----__----__-/----__-/--------__----__-
      /    /         \     / |/  |  /   ) /   /   /   /   /   /   ) /   )
_(___/____/______(____/___/__/___|_(___/_(___/___(___/___/___/___/_(___/_
                                                                      /
    comparei3dMappings.py - v1.0.2                                (_ /

Version History:
 v0.0.9 - Initial Release
 v1.0.0 - Polished up Release
"""

import argparse
import os
import sys
import xml.etree.ElementTree as ET


def enter_key_exit():
    """ Exit when enter key pressed """
    print("Press ENTER to close terminal.")
    try:
        input()
    except BaseException:
        pass
    exit()


print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
print("  comparei3dMappings v1.0.2")
print("    by JTSModding")
print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")

parser = argparse.ArgumentParser(
    description='Compare i3d Mapping in xml files.',
    usage='%(prog)s [-h] file file [file ...]'
)
parser.add_argument(
    'file1',
    nargs=1,
    metavar='file',
    type=argparse.FileType('r', encoding='utf-8')
)
parser.add_argument(
    'file2',
    nargs='+',
    metavar='file',
    type=argparse.FileType('r', encoding='utf-8'),
    help=argparse.SUPPRESS
)

try:
    args = parser.parse_args()
except BaseException:
    enter_key_exit()


file_list = args.file1 + args.file2


print("Files Found: " + str(len(file_list)))

fileCount     = len(file_list)
fileListShort = []
nameList      = {}

for file in file_list:
    foundMap   = False
    thisName   = os.path.basename(file.name)
    fileListShort.append(thisName)

    try:
        thisXML    = ET.fromstring(file.read())
    except BaseException:
        print("ERROR: Unable to read / parse file '" + thisName + "'")
        enter_key_exit()

    for texts in thisXML.findall('i3dMappings'):
        foundMap = True
        for child in texts:
            thisMapID   = child.attrib["id"]
            thisMapNode = child.attrib["node"]
            if thisMapID in nameList.keys():
                nameList[thisMapID].append({thisName: thisMapNode})
            else:
                nameList[thisMapID] = [{thisName: thisMapNode}]

    if not foundMap:
        print("WARNING!: file '" + thisName + "' does not have an i3dMappings section")
        enter_key_exit()

foundMismatch  = False
firstMissing   = False
firstDifferent = False
textMissing    = []
textDiff       = []


for thisText in nameList:
    if (len(nameList[thisText]) != fileCount):
        if not firstMissing:
            textMissing.append("\nMismatch(es) Found (missing):")
            firstMissing  = True
            foundMismatch = True

        foundFiles    = [list(shortFileName.keys())[0] for shortFileName in nameList[thisText]]

        notFoundFiles = [testFile for testFile in fileListShort if testFile not in foundFiles]

        textMissing.append("\n  Text Name : " + thisText)
        textMissing.append("   Found In      : " + str(foundFiles))
        textMissing.append("   Not Found In  : " + str(notFoundFiles))

    # Check if the mapping is the same, even if there was a missing above.
    lastNodeID    = False
    stopNow       = False
    for i3dMapping in nameList[thisText]:
        if not stopNow:
            thisNodeID = list(i3dMapping.values())[0]

            if lastNodeID is False:
                lastNodeID = thisNodeID

            if lastNodeID != thisNodeID:
                stopNow = True
                if not firstDifferent:
                    textDiff.append("\nMismatch(es) Found (different):")
                    firstDifferent = True
                    foundMismatch  = True

                textDiff.append("\n  ID Name : " + thisText)
                textDiff.append("   Mappings : " + str(nameList[thisText]))


if not foundMismatch:
    print("All files share the same I3D Mapping")
else:
    print("\n".join(textMissing))
    print("\n".join(textDiff))
    print("\nThere are mismatched I3D Mappings")

if sys.stdout.isatty():
    # Don't pause on finish if we re-directed to a file.
    enter_key_exit()
