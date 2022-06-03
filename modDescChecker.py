# pylama:ignore=W605,E221,C901
"""
        __ ______     __     _   _
        /    /      /    )   /  /|              /       /   ,
-------/----/-------\-------/| /-|----__----__-/----__-/--------__----__-
      /    /         \     / |/  |  /   ) /   /   /   /   /   /   ) /   )
_(___/____/______(____/___/__/___|_(___/_(___/___(___/___/___/___/_(___/_
                                                                      /
    modDescChecker.py - v1.0.2                                    (_ /

Version History:
 v1.0.2 - Initial Release
"""

import argparse
import os
import sys
import re
import xml.etree.ElementTree as ET

MOD_DESC_VERSION = 66
L10N_REQUIRED = ["en", "de"]
MOD_ICON_NAME = "modIcon.dds"


def check_dup(check_list):
    return len(check_list) == len(set(check_list))


def check_l10n(check_list):
    for requiredBit in L10N_REQUIRED:
        if requiredBit not in check_list:
            return False
    return True


def tag_fail(tag, test):
    prefix_print("Checking of <{0}> for {1} failed".format(tag, test), False, False)


def prefix_print(text, status, noTest=True):
    print("  {1} :: {2}{0}{3}".format(
        text,
        ["   FAIL", "SUCCESS"][status],
        ["", "TEST: "][noTest],
        ["", "?"][noTest]
    ))


def enter_key_exit():
    """ Exit when enter key pressed """
    print("Press ENTER to close terminal.")
    try:
        input()
    except BaseException:
        pass
    exit()


print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
print("  modDescChecker v1.0.2")
print("    by JTSModding")
print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")

parser = argparse.ArgumentParser(description='Sanity check an xml shopItem file.')
parser.add_argument(
    'file', metavar='file', nargs=1, type=argparse.FileType('r', encoding='utf-8')
)

try:
    args = parser.parse_args()
except BaseException:
    enter_key_exit()

try:
    if not args.file[0].name.endswith("xml"):
        raise BaseException
    thisXML = ET.ElementTree(ET.fromstring(args.file[0].read()))
except BaseException:
    print("ERROR: Unable to read / parse file '" + os.path.basename(args.file[0].name) + "'")
    enter_key_exit()

print("CHECKING: {0}".format(args.file[0].name))

try:
    checkTag = thisXML.getroot()

    prefix_print(
        'descVersion is {0} or greater'.format(MOD_DESC_VERSION),
        int(checkTag.attrib["descVersion"]) >= MOD_DESC_VERSION
    )
except BaseException:
    prefix_print('This is not a modDesc file', False)

try:
    prefix_print(
        "Title L10N contains at least {0}".format(str(L10N_REQUIRED)),
        check_l10n([child.tag for child in thisXML.find(".//title")])
    )
except BaseException:
    tag_fail('TITLE', 'Minimum L10N Entries')

try:
    prefix_print(
        "Title {0} are not identical".format(str(L10N_REQUIRED)),
        check_dup([child.text for child in thisXML.find(".//title") if child.tag in L10N_REQUIRED])
    )
except BaseException:
    tag_fail('TITLE', 'Identical L10N Entries')

try:
    prefix_print(
        "Description L10N contains at least {0}".format(str(L10N_REQUIRED)),
        check_l10n([child.tag for child in thisXML.find(".//description")])
    )
except BaseException:
    tag_fail('DESCRIPTION', 'Minimum L10N Entries')

try:
    prefix_print(
        "Description {0} are not identical".format(str(L10N_REQUIRED)),
        check_dup(
            [child.tag for child in thisXML.find(".//description") if child.tag in L10N_REQUIRED]
        )
    )
except BaseException:
    tag_fail('DESCRIPTION', 'Identical L10N Entries')

try:
    prefix_print(
        "iconFilename is '{0}'".format(MOD_ICON_NAME),
        thisXML.find(".//iconFilename").text == MOD_ICON_NAME
    )
except BaseException:
    tag_fail('ICONFILENAME', 'Value is {0}'.format(MOD_ICON_NAME))

try:
    prefix_print(
        "version 1.0.0.0+ contains changelog",
        bool(
            thisXML.find(".//version").text == "1.0.0.0" or
            re.search("changelog", thisXML.find(".//description/en").text, re.IGNORECASE)
        )
    )
except BaseException:
    tag_fail('VERSION', 'Version is 1.0.0.0+ with changelog')

try:
    for thisTag in thisXML.findall(".//l10n/text"):
        prefix_print(
            "'{1}' L10N contains at least {0}".format(str(L10N_REQUIRED), thisTag.attrib["name"]),
            check_l10n([child.tag for child in thisTag])
        )

except BaseException:
    tag_fail('L10N', 'Checking children have minimum set of languages')


print('\ndone.')

if sys.stdout.isatty():
    # Don't pause on finish if we re-directed to a file.
    enter_key_exit()
