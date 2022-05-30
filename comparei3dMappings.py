"""
  _____ _______ _______ _______  _____  ______  ______  _____ __   _  ______
    |      |    |______ |  |  | |     | |     \ |     \   |   | \  | |  ____
  __|      |    ______| |  |  | |_____| |_____/ |_____/ __|__ |  \_| |_____|
    comparei3dMappings.py

Version History:
 v0.0.9 - Initial Release
"""
import argparse
import os
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description='Compare i3d Mapping in xml files.')

parser.add_argument('files', metavar='files', nargs='*', type=argparse.FileType('r', encoding='utf-8'))
args = parser.parse_args()


if ( args.files is None  or len(args.files) < 2 ) :
	print("No files given.")
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

	for texts in thisXML.findall('i3dMappings'):
		for child in texts:
			thisMapID   = child.attrib["id"]
			thisMapNode = child.attrib["node"]
			if thisMapID in nameList.keys():
				nameList[thisMapID].append({thisName: thisMapNode})
			else :
				nameList[thisMapID] = [{thisName: thisMapNode}]

foundMismatch = False
for thisText in nameList:
	if ( len(nameList[thisText]) != fileCount ):
		foundMismatch = True

		foundFiles    = [list(shortFileName.keys())[0] for shortFileName in nameList[thisText] ]

		notFoundFiles = [ testFile for testFile in fileListShort if testFile not in foundFiles ]

		print("Mismatch Found (missing):")
		print("  Text Name : " + thisText)
		print("   Found In      : " + str(foundFiles))
		print("   Not Found In  : " + str(notFoundFiles))
	else :
		foundMismatch = True
		lastNodeID    = False
		stopNow       = False
		for i3dMapping in nameList[thisText] :
			if not stopNow :
				thisNodeID = list(i3dMapping.values())[0]

				if lastNodeID == False :
					lastNodeID = thisNodeID

				if lastNodeID != thisNodeID :
					stopNow = True
					print("Mismatch Found (different):")
					print("  ID Name : " + thisText)
					print("   Mappings : " + str(nameList[thisText]))

if not foundMismatch:
	print("All files share the same I3D Mapping")
else :
	print("\nThere are mismatched I3D Mappings")
