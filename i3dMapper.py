# pylama:ignore=W605,E221,C901
"""
        __ ______     __     _   _
        /    /      /    )   /  /|              /       /   ,
-------/----/-------\-------/| /-|----__----__-/----__-/--------__----__-
      /    /         \     / |/  |  /   ) /   /   /   /   /   /   ) /   )
_(___/____/______(____/___/__/___|_(___/_(___/___(___/___/___/___/_(___/_
                                                                      /
    i3dMApper.py - v1.0.0                                         (_ /

Version History:
 v0.0.9 - Initial Release
 v1.0.0 - Polished up Release
"""

import argparse
import xml.etree.ElementTree as ET
import os
import sys


def enter_to_exit():
    """ Exit when enter key pressed """
    print("Press ENTER to close terminal.")
    input()
    exit()


def nodeMaker(component, depthList=None):
    """ Make the node string """
    thisNode = str(component) + ">"
    if depthList is None:
        return thisNode

    return thisNode + "|".join([str(i) for i in depthList])


def depth_iter(element, tag=None):
    """ iterate with depth tracking """
    stack = []
    stack.append(iter([element]))
    while stack:
        e = next(stack[-1], None)
        if e is None:
            stack.pop()
        else:
            stack.append(iter(e))
            if tag is None or e.tag == tag:
                yield (e, len(stack) - 1)


def add_tag(name, node):
    """ Add output tag to stack """
    global maxNameSize
    thisSize = len(name)
    if thisSize > maxNameSize:
        maxNameSize = thisSize

    printNames.append([name, node])


def print_tag(thisMap):
    """ output tag """
    global noPretty, maxNameSize

    thisLine = "\t<i3dMapping id=\"" + thisMap[0] + "\""

    if not noPretty:
        for i in range(0, maxNameSize - len(thisMap[0])):
            thisLine += " "

    thisLine += " node=\"" + thisMap[1] + "\" />"

    return thisLine


parser = argparse.ArgumentParser(description='Export i3d Mapping')
parser.add_argument('file', metavar='file', nargs=1, type=argparse.FileType('r', encoding='utf-8'))
parser.add_argument(
    '--no_pretty_print',
    help="Disable pretty printing",
    dest="noPretty",
    default=False,
    action='store_true'
)

try:
    args = parser.parse_args()
except BaseException:
    enter_key_exit()

try:
    thisXML     = ET.ElementTree(ET.fromstring(args.file[0].read()))
except BaseException:
    print("ERROR: Unable to read / parse file '" + os.path.basename(args.file[0].name) + "'")
    enter_key_exit()

thisScene        = thisXML.find('Scene')
printNames       = []
maxNameSize      = 0
noPretty         = args.noPretty
uniqueNames      = {}
lastDepth        = 0
countDepth       = []
currentComponent = -1

for xml_entry, depth in depth_iter(thisScene):
    # Name collisions
    if depth > 1:
        thisNodeName = xml_entry.get('name')
        if thisNodeName in uniqueNames.keys():
            uniqueNames[thisNodeName] += 1
            thisNodeName = thisNodeName + "_" + '{:0>3}'.format(uniqueNames[thisNodeName])
        else:
            uniqueNames[thisNodeName] = 1

    # Component level objects
    if depth == 2:
        currentComponent += 1
        countDepth        = []
        lastDepth         = 0
        thisNode          = nodeMaker(currentComponent)
        add_tag(thisNodeName, thisNode)

    # All other objects
    if depth > 2:
        lastMapIndex = depth - 2

        if lastMapIndex > lastDepth:
            for i in range(0, lastMapIndex - lastDepth):
                countDepth.append(0)
        else:
            if lastMapIndex < lastDepth:
                for i in range(0, lastDepth - lastMapIndex):
                    countDepth.pop()

            countDepth[lastMapIndex - 1] += 1

        lastDepth = lastMapIndex

        thisNode = nodeMaker(currentComponent, countDepth)
        add_tag(thisNodeName, thisNode)

outputQueue = []

outputQueue.append("<i3dMappings>")
for thisMap in printNames:
    outputQueue.append(print_tag(thisMap))
outputQueue.append("</i3dMappings>")


print("\n".join(outputQueue))


if sys.stdout.isatty():
    # Don't pause on finish if we re-directed to a file.
    enter_to_exit()
