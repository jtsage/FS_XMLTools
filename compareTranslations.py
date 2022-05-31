# pylama:ignore=W605,E221,C901
"""
        __ ______     __     _   _
        /    /      /    )   /  /|              /       /   ,
-------/----/-------\-------/| /-|----__----__-/----__-/--------__----__-
      /    /         \     / |/  |  /   ) /   /   /   /   /   /   ) /   )
_(___/____/______(____/___/__/___|_(___/_(___/___(___/___/___/___/_(___/_
                                                                      /
    compareTranslations.py - v1.0.0                               (_ /

Version History:
 v0.0.9 - Initial Release
 v1.0.0 - Polished up Release
"""
import argparse
import glob
import os
import sys
import xml.etree.ElementTree as ET


def enter_key_exit():
    """ Exit when enter key pressed """
    print("Press ENTER to close terminal.")
    input()
    exit()


def print_dupe(file, key):
    """ Duplicate found"""
    print("WARNING: '" + file + "' contains a duplicate entry for '" + key + "'")


parser = argparse.ArgumentParser(description='Compare translation files.')
parser.add_argument(
    'files', metavar='files', nargs='*', type=argparse.FileType('r', encoding='utf-8')
)
parser.add_argument(
    '--folder',
    help='Process a folder rather than a list of files.',
    dest='folder',
    nargs=1,
    default=False
)
parser.add_argument(
    '--giants_ekv',
    help='Use Giants <e k= v=> mode',
    dest='ekvMode',
    default=False,
    action='store_true'
)

try:
    args = parser.parse_args()
except BaseException:
    enter_key_exit()

ekvMode = args.ekvMode


if (args.folder is not False):
    file_list = {open(fle, 'r', encoding='utf-8') for fle in glob.glob(args.folder[0] + "/*.xml")}
else:
    if (args.files is None or len(args.files) < 2):
        print("ERROR: No folder or files given.")
        parser.print_help()
        enter_key_exit()

    file_list = args.files

print("Files Found: " + str(len(file_list)))

fileCount     = len(file_list)
fileListShort = []
nameList      = {}

xmlContainer = ('texts', 'elements')[ekvMode]
xmlAttrib    = ('name', 'k')[ekvMode]

for file in file_list:
    foundText  = False
    thisName   = os.path.basename(file.name)
    fileListShort.append(thisName)

    try:
        thisXML    = ET.fromstring(file.read())
    except BaseException:
        print("ERROR: Unable to read / parse file '" + thisName + "'")
        enter_key_exit()

    for texts in thisXML.findall(xmlContainer):
        for child in texts:
            foundText = True
            thisTextName = child.attrib[xmlAttrib]
            if thisTextName in nameList.keys():
                if thisName in nameList[thisTextName]:
                    print_dupe(thisName, thisTextName)
                else:
                    nameList[thisTextName].append(thisName)
            else:
                nameList[thisTextName] = [thisName]

    if not foundText:
        print("ERROR: file '" + thisName + "' does not have any detected l10n entries")
        enter_key_exit()

foundMismatch = False

for thisText in nameList:
    if (len(nameList[thisText]) != fileCount):
        if not foundMismatch:
            print("Mismatch(es) Found:")
            foundMismatch = True

        notFoundFiles = [t_file for t_file in fileListShort if t_file not in nameList[thisText]]

        print("\n  Text Name : " + thisText)
        print("   Found In      : " + str(nameList[thisText]))
        print("   Not Found In  : " + str(notFoundFiles))


if not foundMismatch:
    print("All files share the same name keys")
else:
    print("\nThere are mismatched translations")

if sys.stdout.isatty():
    # Don't pause on finish if we re-directed to a file.
    enter_key_exit()
