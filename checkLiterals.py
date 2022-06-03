# pylama:ignore=W605,E221,C901
"""
        __ ______     __     _   _
        /    /      /    )   /  /|              /       /   ,
-------/----/-------\-------/| /-|----__----__-/----__-/--------__----__-
      /    /         \     / |/  |  /   ) /   /   /   /   /   /   ) /   )
_(___/____/______(____/___/__/___|_(___/_(___/___(___/___/___/___/_(___/_
                                                                      /
    checkLiterals.py - v1.0.2                                     (_ /

Version History:
 v0.0.9 - Initial Release
 v1.0.0 - Polished up Release
"""

import argparse
import os
import sys
import xml.etree.ElementTree as ET

ATTRIBUTES_TO_CHECK = [
    "abortUnloading", "activateText", "baleDoNotAllowFillTypeMixing", "baleNotSupported",
    "changeText", "clutchCrackingGearWarning", "clutchCrackingGroupWarning",
    "clutchNoEngagedWarning", "consumersEmptyWarning", "consumersEmptyWarning", "deactivateText",
    "detachWarning", "disableText", "enableText", "infoText", "lowering", "lowerPlatform",
    "middleNegDirectionText", "middlePosDirectionText", "minUnloadingFillLevelWarning",
    "negDirectionText", "noCutter", "objectText", "onlyOneBaleTypeWarning", "operatingPosition",
    "posDirectionText", "textNeg", "textPos", "tilting", "title", "transportPosition",
    "turnOffText", "turnOnNotAllowedWarning", "turnOnStateWarning", "turnOnText", "typeDesc",
    "unfoldWarning", "unload", "unloadBaleText", "unloadHere"
]
TAG_TO_CHECK_NAME_ATTRIB = [
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
]
TAG_TO_CHECK_TEXT = ["function", "typeDesc", "name"]


def enter_key_exit():
    """ Exit when enter key pressed """
    print("Press ENTER to close terminal.")
    try:
        input()
    except BaseException:
        pass
    exit()


def print_bad(tag, value):
    """ Print tag and value to output device """
    print("  Possible missed translation in tag: " + tag + ", current value is: " + value)


def is_l10n(value):
    return value.startswith("$l10n")


print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
print("  checkLiterals v1.0.2")
print("    by JTSModding")
print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")

parser = argparse.ArgumentParser(
    description='Check vehicle/placable xml(s) for untranslated strings.'
)
parser.add_argument(
    'files', metavar='files.xml', nargs="+", type=argparse.FileType('r', encoding='utf-8')
)

try:
    args = parser.parse_args()
except BaseException:
    enter_key_exit()

print("Files Found: " + str(len(args.files)))

for file in args.files:
    cleanFile  = True
    thisName   = os.path.basename(file.name)

    try:
        if not file.name.endswith("xml"):
            raise BaseException
        thisXML    = ET.fromstring(file.read())
    except BaseException:
        print("ERROR: Unable to read / parse file '" + thisName + "'")
        enter_key_exit()

    print("\nChecking: " + thisName + "...\n")

    for attrib_key in ATTRIBUTES_TO_CHECK:
        for thisTag in thisXML.findall(".//*[@" + attrib_key + "]"):
            if not is_l10n(thisTag.attrib[attrib_key]):
                cleanFile = False
                print_bad(thisTag.tag, thisTag.attrib[attrib_key])

    for tag_name in TAG_TO_CHECK_TEXT:
        for thisTag in thisXML.findall(".//" + tag_name):
            if tag_name == "name":
                if len(thisTag):
                    cleanFile = False
                    print_bad(thisTag.tag, 'translated with the "old" method')
            if thisTag.text is not None and not thisTag.text.isspace():
                if not is_l10n(thisTag.text):
                    cleanFile = False
                    print_bad(thisTag.tag, thisTag.text)

    for tag_name in TAG_TO_CHECK_NAME_ATTRIB:
        for thisTag in thisXML.findall(".//" + tag_name):
            if "name" in thisTag.attrib:
                if not is_l10n(thisTag.attrib["name"]):
                    cleanFile = False
                    print_bad(thisTag.tag, thisTag.attrib["name"])

    print(
        "\nFile: " + thisName + (" HAS", " has no")[cleanFile] + " probable missing translations\n"
    )


print("done.")

if sys.stdout.isatty():
    # Don't pause on finish if we re-directed to a file.
    enter_key_exit()
