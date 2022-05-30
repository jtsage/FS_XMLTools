"""
  _____ _______ _______ _______  _____  ______  ______  _____ __   _  ______
    |      |    |______ |  |  | |     | |     \ |     \   |   | \  | |  ____
  __|      |    ______| |  |  | |_____| |_____/ |_____/ __|__ |  \_| |_____|
    compareTranslations.py

Version History:
 v0.0.9 - Initial Release
"""
import argparse
import glob
import os
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description='Compare translation files.')

parser.add_argument('files', metavar='files', nargs='*', type=argparse.FileType('r', encoding='utf-8'))
parser.add_argument('--folder', dest='folder', nargs=1, default=False)
parser.add_argument('--giants_ekv', help='Use Giants <e k="" v=""> mode', dest='ekvMode', default=False, action='store_true')
args = parser.parse_args()

ekvMode = args.ekvMode


if ( args.folder != False ) :
	file_list_text = glob.glob(args.folder[0] + "/*.xml")
	file_list      = {open(filename, 'r', encoding='utf-8') for filename in file_list_text}
else :
	if ( args.files is None or len(args.files) < 2 ) :
		print("No folder or files given.")
		parser.print_help()
		exit()
	file_list = args.files

print("Files Found: " +  str(len(file_list)))

fileCount     = 0
fileListShort = []
nameList      = {}

for file in file_list:	
	fileCount += 1
	thisName   = os.path.basename(file.name)
	thisXML    = ET.fromstring(file.read())
	fileListShort.append(thisName)

	if ekvMode :
		for texts in thisXML.findall('elements'):
			for child in texts:
				thisTextName = child.attrib["k"]
				if thisTextName in nameList.keys():
					nameList[thisTextName].append(thisName)
				else :
					nameList[thisTextName] = [thisName]
	else:
		for texts in thisXML.findall('texts'):
			for child in texts:
				thisTextName = child.attrib["name"]
				if thisTextName in nameList.keys():
					nameList[thisTextName].append(thisName)
				else :
					nameList[thisTextName] = [thisName]

foundMismatch = False
for thisText in nameList:
	if ( len(nameList[thisText]) != fileCount ):
		foundMismatch = True

		notFoundFiles = [ testFile for testFile in fileListShort if testFile not in nameList[thisText] ]

		print("Mismatch Found:")
		print("  Text Name : " + thisText)
		print("   Found In      : " + str(nameList[thisText]))
		print("   Not Found In  : " + str(notFoundFiles))


if not foundMismatch:
	print("All files share the same name keys")
else :
	print("\nThere are mismatched translations")
