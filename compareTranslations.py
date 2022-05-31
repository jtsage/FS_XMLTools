"""
  _____ _______ _______ _______  _____  ______  ______  _____ __   _  ______
    |      |    |______ |  |  | |     | |     \ |     \   |   | \  | |  ____
  __|      |    ______| |  |  | |_____| |_____/ |_____/ __|__ |  \_| |_____|
    compareTranslations.py v1.0.0

Version History:
 v0.0.9 - Initial Release
 v1.0.0 - Polished up Release
"""
import argparse
import glob
import os
import xml.etree.ElementTree as ET

def enter_key_exit() :
	print("Press ENTER to close terminal.")
	input()
	exit()

parser = argparse.ArgumentParser(description='Compare translation files.')

parser.add_argument('files', metavar='files', nargs='*', type=argparse.FileType('r', encoding='utf-8'))
parser.add_argument('--folder', dest='folder', nargs=1, default=False)
parser.add_argument('--giants_ekv', help='Use Giants <e k="" v=""> mode', dest='ekvMode', default=False, action='store_true')
args = parser.parse_args()

ekvMode = args.ekvMode

try :
	args = parser.parse_args()
except :
	enter_key_exit()


if ( args.folder != False ) :
	file_list      = {open(filename, 'r', encoding='utf-8') for filename in glob.glob(args.folder[0] + "/*.xml")}
else :
	if ( args.files is None or len(args.files) < 2 ) :
		print("ERROR: No folder or files given.")
		parser.print_help()
		enter_key_exit()

	file_list = args.files

print("Files Found: " +  str(len(file_list)))

fileCount     = len(file_list)
fileListShort = []
nameList      = {}

xmlContainer = ('texts','elements')[ekvMode]
xmlAttrib    = ('name','k')[ekvMode]

for file in file_list:	
	foundText  = False
	thisName   = os.path.basename(file.name)
	thisXML    = ET.fromstring(file.read())
	fileListShort.append(thisName)

	for texts in thisXML.findall(xmlContainer):
		for child in texts:
			foundText = True
			thisTextName = child.attrib[xmlAttrib]
			if thisTextName in nameList.keys():
				if thisName in nameList[thisTextName] :
					print("WARNING: '"+ thisName +"' contains a duplicate entry for '" + thisTextName + "'")
				else : 
					nameList[thisTextName].append(thisName)
			else :
				nameList[thisTextName] = [thisName]


	if not foundText :
		print("ERROR: file '" + thisName + "' does not have any detected l10n entries")
		enter_key_exit()

foundMismatch = False

for thisText in nameList:
	if ( len(nameList[thisText]) != fileCount ):
		if not foundMismatch :
			print("Mismatch(es) Found:")
			foundMismatch = True

		notFoundFiles = [ testFile for testFile in fileListShort if testFile not in nameList[thisText] ]

		print("\n  Text Name : " + thisText)
		print("   Found In      : " + str( nameList[thisText] ))
		print("   Not Found In  : " + str( notFoundFiles ))


if not foundMismatch:
	print("All files share the same name keys")
else :
	print("\nThere are mismatched translations")

enter_key_exit()