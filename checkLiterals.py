# pylama:ignore=W605,E221,C901
"""
        __ ______     __     _   _
        /    /      /    )   /  /|              /       /   ,
-------/----/-------\-------/| /-|----__----__-/----__-/--------__----__-
      /    /         \     / |/  |  /   ) /   /   /   /   /   /   ) /   )
_(___/____/______(____/___/__/___|_(___/_(___/___(___/___/___/___/_(___/_
                                                                      /
    checkLiterals.py - v1.0.0                                     (_ /

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
    input()
    exit()


def print_bad(tag, value):
    """ Print tag and value to output device """
    print("  Possible missed translation in tag: " + tag + ", current value is: " + value)


parser = argparse.ArgumentParser(
    description='Check vehicle/placable xml(s) for untranslated strings.'
)
parser.add_argument(
    'files', metavar='files', nargs="+", type=argparse.FileType('r', encoding='utf-8')
)

try:
    args = parser.parse_args()
except BaseException:
    enter_key_exit()

file_list = args.files


attributes_to_check = {
    "abortUnloading", "activateText", "baleDoNotAllowFillTypeMixing", "baleNotSupported",
    "changeText", "clutchCrackingGearWarning", "clutchCrackingGroupWarning",
    "clutchNoEngagedWarning", "consumersEmptyWarning", "consumersEmptyWarning", "deactivateText",
    "detachWarning", "disableText", "enableText", "infoText", "lowering", "lowerPlatform",
    "middleNegDirectionText", "middlePosDirectionText", "minUnloadingFillLevelWarning",
    "negDirectionText", "noCutter", "objectText", "onlyOneBaleTypeWarning", "operatingPosition",
    "posDirectionText", "textNeg", "textPos", "tilting", "title", "transportPosition",
    "turnOffText", "turnOnNotAllowedWarning", "turnOnStateWarning", "turnOnText", "typeDesc",
    "unfoldWarning", "unload", "unloadBaleText", "unloadHere"
}
tag_to_check_name_attrib = {
    "attacherJointConfiguration", "baseMaterialConfiguration", "configurationSet", "controlGroup",
    "coverConfiguration", "design8Configuration", "design7Configuration", "design6Configuration",
    "design5Configuration", "design4Configuration", "design3Configuration", "design2Configuration",
    "designConfiguration", "designMaterialConfiguration", "designMaterial2Configuration",
    "designMaterial3Configuration", "dischargeableConfiguration", "fillUnitConfiguration",
    "fillVolumeConfiguration", "foldingConfiguration", "frontloaderConfiguration",
    "inputAttacherJointConfiguration", "motorConfiguration", "pipeConfiguration",
    "powerConsumerConfiguration", "rimColorConfiguration", "steeringMode", "tipSide",
    "trailerConfiguration", "transmission", "variableWorkWidthConfiguration",
    "vehicleTypeConfiguration", "wheelConfiguration", "workAreaConfiguration", "workMode",
    "wrappingAnimationConfiguration", "wrappingColorConfiguration",
}
tag_to_check_text = {
    "function", "typeDesc", "name",
}


print("Files Found: " + str(len(file_list)))


for file in file_list:
    cleanFile  = True
    thisName   = os.path.basename(file.name)

    try:
        thisXML    = ET.fromstring(file.read())
    except BaseException:
        print("ERROR: Unable to read / parse file '" + thisName + "'")
        enter_key_exit()

    print("\nChecking: " + thisName + "...\n")

    for attrib_key in attributes_to_check:
        for thisTag in thisXML.findall(".//*[@" + attrib_key + "]"):
            if not thisTag.attrib[attrib_key].startswith('$l10n'):
                cleanFile = False
                print_bad(thisTag.tag, thisTag.attrib[attrib_key])

    for tag_name in tag_to_check_text:
        for thisTag in thisXML.findall(".//" + tag_name):
            if thisTag.text is not None:
                if not thisTag.text.startswith('$l10n'):
                    cleanFile = False
                    print_bad(thisTag.tag, thisTag.text)

    for tag_name in tag_to_check_name_attrib:
        for thisTag in thisXML.findall(".//" + tag_name):
            if "name" in thisTag.attrib:
                if not thisTag.attrib["name"].startswith('$l10n'):
                    cleanFile = False
                    print_bad(thisTag.tag, thisTag.attrib["name"])

    if cleanFile:
        print("\nFile: " + thisName + " had no detected missing translations\n")
    else:
        print("\nFile: " + thisName + " HAS detected missing translations\n")

print("done.")

if sys.stdout.isatty():
    # Don't pause on finish if we re-directed to a file.
    enter_key_exit()
