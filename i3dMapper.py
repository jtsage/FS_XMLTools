"""
  _____ _______ _______ _______  _____  ______  ______  _____ __   _  ______
    |      |    |______ |  |  | |     | |     \ |     \   |   | \  | |  ____
  __|      |    ______| |  |  | |_____| |_____/ |_____/ __|__ |  \_| |_____|
    i3dMapper.py

Version History:
 v0.0.9 - Initial Release
"""

import argparse
import os
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description='Export i3d Mapping')

parser.add_argument('file', metavar='file', nargs=1, type=argparse.FileType('r', encoding='utf-8'))
parser.add_argument('--no_pretty_print', help="Disable pretty printing", dest="noPretty", default=False, action='store_true' )
args = parser.parse_args()


thisXML     = ET.ElementTree(ET.fromstring(args.file[0].read()))
thisScene   = thisXML.find('Scene')
printNames  = []
maxNameSize = 0
noPretty    = args.noPretty


def nodeMaker(component, depthList = None) :
	thisNode = str(component) + ">"
	if depthList is None :
		return thisNode

	return thisNode +  "|".join([str(i) for i in depthList])


def depth_iter(element, tag=None):
    stack = []
    stack.append(iter([element]))
    while stack:
        e = next(stack[-1], None)
        if e == None:
            stack.pop()
        else:
            stack.append(iter(e))
            if tag == None or e.tag == tag:
                yield (e, len(stack) - 1)

def add_tag(name, node) :
	global maxNameSize
	thisSize = len(name)
	if thisSize > maxNameSize:
		maxNameSize = thisSize

	printNames.append([name, node])

def print_tag(thisMap) :
	global noPretty, maxNameSize

	thisLine = "\t<i3dMapping id=\"" + thisMap[0] + "\""

	if not noPretty :
		for i in range(0, maxNameSize - len(thisMap[0]) ) :
			thisLine += " "

	thisLine += " node=\"" + thisMap[1] + "\" />"

	print(thisLine)
	



uniqueNames      = {}
lastDepth        = 0
countDepth       = []
currentComponent = -1


for xml_entry, depth in depth_iter(thisScene):
	# Name collisions
	if depth > 1 :
		thisNodeName = xml_entry.get('name')
		if thisNodeName in uniqueNames.keys() :
			uniqueNames[thisNodeName] += 1
			thisNodeName = thisNodeName + "_" + '{:0>3}'.format(uniqueNames[thisNodeName])
		else :
			uniqueNames[thisNodeName] = 1

	# Component level objects
	if depth == 2 :
		currentComponent += 1
		countDepth        = []
		lastDepth         = 0
		thisNode          = nodeMaker(currentComponent)
		add_tag(thisNodeName, thisNode)

	# All other objects
	if depth > 2 :
		lastMapIndex = depth - 2

		if lastMapIndex > lastDepth :
			for i in range(0, lastMapIndex - lastDepth) :
				countDepth.append(0)
		else: 
			if lastMapIndex < lastDepth :
				for i in range(0, lastDepth - lastMapIndex) :
					countDepth.pop()

			countDepth[lastMapIndex-1] += 1
		
		lastDepth = lastMapIndex
		
		thisNode = nodeMaker(currentComponent, countDepth)
		add_tag(thisNodeName, thisNode)


print("<i3dMappings>")
for thisMap in printNames :
	print_tag(thisMap)
print("</i3dMappings>")
