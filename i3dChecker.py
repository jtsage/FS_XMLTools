# pylama:ignore=W605,E221,C901
"""
        __ ______     __     _   _
        /    /      /    )   /  /|              /       /   ,
-------/----/-------\-------/| /-|----__----__-/----__-/--------__----__-
      /    /         \     / |/  |  /   ) /   /   /   /   /   /   ) /   )
_(___/____/______(____/___/__/___|_(___/_(___/___(___/___/___/___/_(___/_
                                                                      /
    i3dChecker.py - v0.0.9                                        (_ /

Version History:
 v0.0.9 - Initial Release
"""

import argparse
import os
import math
import xml.etree.ElementTree as ET


exit("WIP")


def enter_key_exit():
    """ Exit when enter key pressed """
    print("Press ENTER to close terminal.")
    input()
    exit()


def none_attrib(element, key):
    """ Grab an attribute value by key, null safe"""
    if element.attrib is None:
        return None
    if key not in element.attrib:
        return None
    return element.attrib[key]


def na_attrib(element, key):
    """ Grab an attribute, use n/a instead of None"""
    if none_attrib(element, key) is None:
        return "n/a"
    return none_attrib(element, key)


def yn_attrib(element, key):
    """ Grab an attribute, use yes/no for booleans"""
    tmpVal = none_attrib(element, key)

    if tmpVal is None:
        return "no"
    if tmpVal is True or tmpVal.lower() == 'true':
        return "yes"
    return "no"


def is_xml_true(value):
    """ String convert bool and handle None """
    if value is None:
        return False
    if value is True or value.lower() == 'true':
        return True
    return False


def sRGB_string_to_hex(color):
    """ Convert space delimited sRGB color to HEX string"""
    if color is None:
        return "#FFFFFF"
    return "#" + "".join(['%02X' % int(math.floor(float(part) * 255)) for part in color.split()])


parser = argparse.ArgumentParser(description='Sanity check an i3d file.')
parser.add_argument(
    'files', metavar='files', nargs='*', type=argparse.FileType('r', encoding='utf-8')
)
parser.add_argument(
    '--no-shadow-check',
    help="Disable checking visible shapes for shadow maps",
    dest="noShadow",
    action='store_true'
)
parser.add_argument(
    '--no-light-check',
    help="Disable checking linked lights",
    dest="noLights",
    action='store_true'
)
parser.add_argument(
    '--no-light-info',
    help="Disable output of light info",
    dest="noLightInfo",
    action='store_true'
)
parser.add_argument(
    '--no-col-info',
    help="Disable checking collision info",
    dest="noColInfo",
    action='store_true'
)

try:
    args = parser.parse_args()
except BaseException:
    enter_key_exit()


file_list = args.files

print("Files Found: " + str(len(file_list)))

for file in file_list:
    thisName   = os.path.basename(file.name)
    lightsInfo = ["realLights information:"]
    colInfo    = []
    linkLight  = []
    shadows    = [
        "has/castsShadowMap information:",
        "   (not non-render-able, but either don't cast shadows, or don't receive them, or both)"
    ]

    try:
        thisXML    = ET.fromstring(file.read())
    except BaseException:
        print("ERROR: Unable to read / parse file '" + thisName + "'")
        enter_key_exit()

    for thisTag in thisXML.findall(".//Light"):
        lightsInfo.append("\n  Node Name: " + na_attrib(thisTag, "name"))
        thisLine  = "   Type: " + na_attrib(thisTag, "type")
        thisLine += ", Color: " + sRGB_string_to_hex(none_attrib(thisTag, "color"))
        thisLine += ", Shadows: " + yn_attrib(thisTag, "castShadowMap")
        thisLine += ", Range: " + none_attrib(thisTag, "range") + "m"
        thisLine += ", Cone Angle: " + none_attrib(thisTag, "coneAngle") + "°"
        thisLine += ", Drop Off: " + none_attrib(thisTag, "dropOff") + "m"
        lightsInfo.append(thisLine)

    for thisTag in thisXML.findall(".//Shape"):
        thisTagNonRender = none_attrib(thisTag, "nonRenderable")
        thisTagCasts     = none_attrib(thisTag, "castsShadows")
        thisTagReceives  = none_attrib(thisTag, "receiveShadows")

        if (not is_xml_true(thisTagReceives) or not is_xml_true(thisTagCasts)):
            # Either missing cast or receive, check renderable...
            if (not is_xml_true(thisTagNonRender)):
                shadows.append("\n  Node Name: " + na_attrib(thisTag, "name"))
                shadows.append(
                    "   Casts Shadow Map: " + yn_attrib(thisTag, "castsShadows") +
                    " | Receives Shadow Map: " + yn_attrib(thisTag, "receiveShadows")
                )










    if not args.noLightInfo:
        print("\n".join(lightsInfo))
    if not args.noShadow:
        print("\n".join(shadows))


print('done.')
enter_key_exit()
