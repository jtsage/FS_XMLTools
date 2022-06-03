# pylama:ignore=W605,E221,C901
"""
        __ ______     __     _   _
        /    /      /    )   /  /|              /       /   ,
-------/----/-------\-------/| /-|----__----__-/----__-/--------__----__-
      /    /         \     / |/  |  /   ) /   /   /   /   /   /   ) /   )
_(___/____/______(____/___/__/___|_(___/_(___/___(___/___/___/___/_(___/_
                                                                      /
    i3dMapper.py - v1.0.2                                         (_ /

Version History:
 v0.0.9 - Initial Release
 v1.0.0 - Polished up Release
 v1.0.1 - Added clipboard copy batch (and prepped for)
"""

import argparse
import xml.etree.ElementTree as ET
import os
import sys


def enter_key_exit():
    """ Exit when enter key pressed """
    print("Press ENTER to close terminal.")
    try:
        input()
    except BaseException:
        pass
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
    maxNameSize = len(name) if len(name) > maxNameSize else maxNameSize
    printNames.append([name, node])


def print_tag(thisMap):
    """ output tag """
    global pretty_print, maxNameSize

    return "\t<i3dMapping id=\"{0}\" {2}node=\"{1}\" />".format(
        thisMap[0],
        thisMap[1],
        ''.ljust((maxNameSize - len(thisMap[0]) if pretty_print else False))
    )


parser = argparse.ArgumentParser(description='Export i3d Mapping')
parser.add_argument('file', metavar='file', nargs=1, type=argparse.FileType('r', encoding='utf-8'))
parser.add_argument(
    '--pretty-print',
    help="Pretty print output",
    action=argparse.BooleanOptionalAction,
    default=True
)

try:
    args = parser.parse_args()
except BaseException:
    enter_key_exit()

try:
    if not args.file[0].name.endswith("i3d"):
        raise BaseException
    thisXML     = ET.ElementTree(ET.fromstring(args.file[0].read()))
except BaseException:
    print("ERROR: Unable to read / parse file '" + os.path.basename(args.file[0].name) + "'")
    enter_key_exit()

thisScene        = thisXML.find('Scene')
printNames       = []
maxNameSize      = 0
pretty_print     = args.pretty_print
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
            if thisNodeName in uniqueNames.keys():
                raise "Unique Name Error - Unresolved Collision Detected"
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

if sys.stdout.isatty():
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    print("  i3dMapper v1.0.2")
    print("    by JTSModding")
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")
    print("\n".join(outputQueue))
    # Don't pause on finish if we re-directed to a file.
    enter_key_exit()
else:
    print("\n".join(outputQueue))
