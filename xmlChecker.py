# pylama:ignore=W605,E221,C901
"""
        __ ______     __     _   _
        /    /      /    )   /  /|              /       /   ,
-------/----/-------\-------/| /-|----__----__-/----__-/--------__----__-
      /    /         \     / |/  |  /   ) /   /   /   /   /   /   ) /   )
_(___/____/______(____/___/__/___|_(___/_(___/___(___/___/___/___/_(___/_
                                                                      /
    xmlChecker.py - v1.0.3                                        (_ /

Version History:
 v1.0.0 - Initial Release
 v1.0.1 - Check local files, and path case, and l10n entries.
"""

import argparse
import os
import sys
import urllib.request
import glob
import xml.etree.ElementTree as ET
from pathlib import Path

hasLXML = True

try:
    from lxml import etree
except ImportError:
    hasLXML = False

GIANTS_WEBSITE = "https://validation.gdn.giants-software.com/xml/fs22/"

FILE_ERRORS = {
    "FILE_NOT_FOUND": "    FILE NOT FOUND: {0}",
    "FILE_NOT_FOUND_NEW": "    FILE NOT FOUND: {0}  (new name: {1})",
    "ABSOLUTE_PATH": "    PATH ERROR: {0} appears to be an absolute path, this is wrong",
    "CASE_MISMATCH": "    FILE CASE MISMATCH: {0} vs detected {1}",
    "CAN_NOT_CHECK": "    FILE IS PART OF A MOD AND CAN'T BE CHECKED: {0}",
    "FILE_LOCKED": "    FILE IS PART OF LOCKED DATA AND CAN'T BE CHECKED: {0}"
}

MOD_DIR_PREFIX = "$moddir$"

XSD_MAP = {
    "bale": "bale.xsd",
    "beaconLight": "beaconLight.xsd",
    "connectionHoses": "connectionHoses.xsd",
    "crawler": "crawler.xsd",
    "feedingRobot": "feedingRobot.xsd",
    "greenhousePlant": "greenhousePlant.xsd",
    "handTool": "handtool.xsd",
    "inlineBale": "inlineBale.xsd",
    "licensePlates": "mapLicensePlates.xsd",
    "motionPathEffects": "mapMotionPathEffects.xsd",
    "placeable": "placeable.xsd",
    "powerTakeOff": "powerTakeOff.xsd",
    "sound": "ambientSounds.xsd",
    "sounds": "vehicle_sounds.xsd",
    "vehicle": "vehicle.xsd",
    "vehicles": "savegame_vehicles.xsd",
    "wheel": "wheel.xsd",
}

DATA_DOLLAR_PATH_MAP = [
    "bale", "beaconLight", "connectionHoses", "crawler", "feedingRobot", "greenhousePlant",
    "handTool", "inlineBale", "licensePlates", "motionPathEffects", "placeable", "sound",
    "sounds", "vehicle", "wheel"
]

UNKNOWN_NO_DATA_DOLLAR = ["placeables"]

FILENAME_ATTRIBUTES = [
    "filename",
    "textureFilename",
    "densityMaskFilename",
    "xmlFilename",
    "i3dFilename",
]

LIGHT_MAP = {
    "frontLight_01": "frontLight01",
    "frontLightCone_01": "frontLight02",
    "frontLightOval_01": "frontLight03",
    "frontLightOval_02": "frontLight04",
    "frontLightOval_03": "frontLight05",
    "frontLightRectangle_01": "frontLight06White",
    "frontLightRectangle_01Orange": "frontLight06Orange",
    "frontLightRectangle_02": "frontLight07",
    "rear2ChamberLed_01": "rearLight01",
    "rear2ChamberLight_01": "rearLight36",
    "rear2ChamberLight_02": "rearLight02",
    "rear2ChamberLight_03": "rearLight03",
    "rear2ChamberLight_04": "rearLight04",
    "rear2ChamberLight_05": "rearLight05",
    "rear2ChamberLight_06": "rearLight06",
    "rear2ChamberLight_07": "rearLight07",
    "rear2ChamberTurnLed_01": "turnLight03",
    "rear3ChamberLight_01": "rearLight08",
    "rear3ChamberLight_02": "rearLight09",
    "rear3ChamberLight_03": "rearLight10",
    "rear3ChamberLight_04": "rearLight11",
    "rear3ChamberLight_05": "rearLight12",
    "rear3ChamberLight_06": "rearLight34",
    "rear3ChamberLight_07": "rearLight35",
    "rear4ChamberLight_01": "rearLight13",
    "rear4ChamberLight_02": "rearLight14",
    "rear5ChamberLight_01": "rearLight15",
    "rear5ChamberLight_02": "rearLight16",
    "rearLEDLight_01": "rearLight17",
    "rearLight_01": "rearLight18",
    "rearLightCircle_01Orange": "rearLight19Orange",
    "rearLightCircle_01Red": "rearLight19Red",
    "rearLightCircleLEDRed_01": "rearLight20",
    "rearLightCircleOrange_01": "rearLight21Orange",
    "rearLightCircleOrange_02": "rearLight22Orange",
    "rearLightCircleRed_01": "rearLight21Red",
    "rearLightCircleRed_02": "rearLight22Red",
    "rearLightCircleWhite_02": "rearLight22White",
    "rearLightOvalLEDChromeWhite_01": "rearLight24",
    "rearLightOvalLEDOrange_01": "rearLight23Orange",
    "rearLightOvalLEDRed_01": "rearLight23Red",
    "rearLightOvalLEDRed_02": "rearLight25",
    "rearLightOvalLEDWhite_01": "rearLight22White",
    "rearLightOvalOrange_01": "rearLight26Orange",
    "rearLightOvalRed_01": "rearLight26Red",
    "rearLightOvalWhite_01": "rearLight26White",
    "rearLightSquare_01Orange": "rearLight27Orange",
    "rearMultipointLEDLight_01": "rearLight30",
    "rearMultipointLight_01": "rearLight31",
    "rearMultipointLight_02": "rearLight32",
    "rearMultipointLight_03": "rearLight33",
    "rearMultipointLight_04": "rearLight28",
    "rearMultipointLight_05": "rearLight29",
    "rearPlateNumberLight_01": "plateNumberLight01",
    "sideMarker_01": "sideMarker01",
    "sideMarker_02": "sideMarker02",
    "sideMarker_03": "sideMarker03",
    "sideMarker_04": "sideMarker04",
    "sideMarker_04Orange": "sideMarker05Orange",
    "sideMarker_04Red": "sideMarker05Red",
    "sideMarker_04White": "sideMarker05White",
    "sideMarker_05": "sideMarker05",
    "sideMarker_05Orange": "sideMarker06Orange",
    "sideMarker_05Red": "sideMarker06Red",
    "sideMarker_05White": "sideMarker06White",
    "sideMarker_06": "sideMarker06",
    "sideMarker_06Orange": "sideMarker07Orange",
    "sideMarker_06Red": "sideMarker07Red",
    "sideMarker_06White": "sideMarker07White",
    "sideMarker_07Orange": "sideMarker08Orange",
    "sideMarker_07White": "sideMarker08White",
    "sideMarker_08Orange": "sideMarker09Orange",
    "sideMarker_08White": "sideMarker09White",
    "sideMarker_09Orange_turn": "turnLight02",
    "sideMarker_09Orange": "sideMarker10Orange",
    "sideMarker_09Red": "sideMarker10Red",
    "sideMarker_09White": "sideMarker10White",
    "sideMarker_10Orange": "sideMarker11Orange",
    "sideMarker_10Red": "sideMarker11Red",
    "sideMarker_14White": "sideMarker14White",
    "turnLight_01": "turnLight01",
    "workingLightCircle_01": "workingLight01",
    "workingLightCircle_02": "workingLight02",
    "workingLightOval_01": "workingLight03",
    "workingLightOval_02": "workingLight04",
    "workingLightOval_03": "workingLight05",
    "workingLightOval_04": "workingLight06",
    "workingLightOval_05": "workingLight07",
    "workingLightSquare_01": "workingLight08",
    "workingLightSquare_02": "workingLight09",
    "workingLightSquare_03": "workingLight10",
    "workingLightSquare_04": "workingLight11",
}


def getDataFilesPath(override):
    """ Try and find the data files """
    INSTALL_LOCATIONS = [
        "C:\Program Files (x86)\Farming Simulator 2022\data",
        "C:\Program Files (x86)\Steam\steamapps\common\Farming Simulator 22\data",
        "C:\Program Files\Epic Games\FarmingSimulator22\data",
    ]

    if override is not False:
        if (
            not override.endswith("data/")
            and not override.endswith("data")
            and not override.endswith("data/")
        ):
            print("WARNING: DATA FILES NOT FOUND: supplied path should end with \"data\\\"")
        elif not os.path.isdir(override):
            print("WARNING: DATA FILES NOT FOUND: Invalid Path Supplied")
        else:
            return override
    else:
        editPath = findInstalledEditor()
        if editPath:
            return editPath
        else:
            for testPath in INSTALL_LOCATIONS:
                if os.path.isdir(testPath):
                    return testPath

    print("WARNING: DATA FILES NOT FOUND: checking linked $data entries disabled.")
    return ""


def findInstalledEditor():
    """ Find a locally installed Giants Editor"""
    localAppData  = os.getenv('localappdata')
    editorFolders = glob.glob(localAppData + "/GIANTS Editor*")
    editorVersion = 0
    editorFolder  = False

    try:
        if len(editorFolders):
            for thisFolder in editorFolders:
                versionInt = int(thisFolder[-5:].replace(".", ""))
                if editorVersion < versionInt:
                    editorFolder  = thisFolder
                    editorVersion = versionInt

        if editorFolder is not False:
            if os.path.isfile(editorFolder + "/editor.xml"):
                editorTree = ET.parse(editorFolder + '/editor.xml')
                editorRoot = editorTree.getroot()
                for thisTag in editorRoot.findall(".//gameinstallationpath"):
                    return thisTag.text + "data/"
    except BaseException:
        return False
    return False


def check_new_light(filename):
    filename = filename[5:]

    lightname = os.path.splitext(os.path.basename(filename))[0]

    if lightname in LIGHT_MAP.keys():
        return LIGHT_MAP[lightname]
    else:
        return False


def clean_path(baseFolder, filename):
    baseFolderTuple = os.path.splitdrive(baseFolder)
    return os.path.normpath(os.path.join(baseFolderTuple[0], baseFolderTuple[1], filename))


def check_local_file_cache(filename, baseFolder):
    """ check if a local file exists, cache results to lessen IO """
    global dataFilesPath, cachedLocalFiles

    if filename in cachedLocalFiles:
        return (True, None, None)

    if os.path.isabs(filename):
        return(False, FILE_ERRORS["ABSOLUTE_PATH"], [filename])

    absFile   = clean_path(baseFolder, filename)
    absFolder = os.path.normpath(baseFolder)

    if not os.path.exists(absFile):
        return(False, FILE_ERRORS["FILE_NOT_FOUND"], [filename])

    casedFile = str(Path(absFile).resolve())

    if casedFile != absFile:
        return(False, FILE_ERRORS["CASE_MISMATCH"], [
            absFile.replace(absFolder, ''),
            casedFile.replace(absFolder, '')
        ])

    return (True, None, None)


def check_data_file_cache(filename):
    """ check if a data file exists, cache results to lessen IO """
    global dataFilesPath, cachedDataFiles

    filename = filename[6:]

    if filename in cachedDataFiles or dataFilesPath == "":
        return (True, None, None)

    absFile   = clean_path(dataFilesPath, filename)
    absFolder = os.path.normpath(dataFilesPath)

    if not os.path.isfile(absFile):
        if check_new_light(absFile):
            return(
                False,
                FILE_ERRORS["FILE_NOT_FOUND_NEW"],
                ["DATA::" + filename, check_new_light(filename)]
            )
        return(False, FILE_ERRORS["FILE_NOT_FOUND"], ["DATA::" + filename])
    else:
        casedFile = str(Path(absFile).resolve())

        if casedFile != absFile:
            return(False, FILE_ERRORS["CASE_MISMATCH"], [
                absFile.replace(absFolder, ''),
                casedFile.replace(absFolder, '')
            ])

    return (True, None, None)


def enter_key_exit():
    """ Exit when enter key pressed """
    print("Press ENTER to close terminal.")
    try:
        input()
    except BaseException:
        pass
    exit()


def check_links(xmlTree, useDataDollar):
    textList      = ["  PROCESSING: checking file links"]
    badCache      = []

    for file_key in FILENAME_ATTRIBUTES:
        for thisTag in thisXML.findall(".//*[@" + file_key + "]"):
            thisKeyValue   = thisTag.attrib[file_key]
            thisFileStatus = None
            if thisKeyValue not in badCache:
                if thisKeyValue.startswith("{0}data/".format(["", "$"][useDataDollar])):
                    thisFileStatus = check_data_file_cache("{0}{1}".format(
                        ["", "$"][not useDataDollar],
                        thisKeyValue
                    ))
                elif thisKeyValue.startswith(MOD_DIR_PREFIX):
                    thisFileStatus = (False, FILE_ERRORS["CAN_NOT_CHECK"], [thisKeyValue])
                elif thisKeyValue.startswith("$dataS/"):
                    thisFileStatus = (False, FILE_ERRORS["FILE_LOCKED"], [thisKeyValue])
                else:
                    thisFileStatus = check_local_file_cache(thisKeyValue, thisFolder)

                if not thisFileStatus[0]:
                    badCache.append(thisKeyValue)
                    textList.append(thisFileStatus[1].format(thisFileStatus[2]))

    if (len(textList) == 1):
        textList.append("    NOTICE: no missing linked file(s) detected.")

    return textList


def check_schema(xmlDocument, fileType, check_l10n):
    textList = ["  PROCESSING: Checking against XSD Schema"]

    try:
        data = urllib.request.urlopen(GIANTS_WEBSITE + XSD_MAP[fileType])
    except BaseException:
        textList.append("    WARNING: Loading XSD from giants validation server failed")
        return textList

    try:
        ns     = ""
        xmlschema_doc = etree.parse(data)

        if check_l10n:
            for thisTag in xmlschema_doc.iter('{*}schema'):
                ns = thisTag.nsmap['xs']

            RESTRICT_TAG = "{{{0}}}restriction".format(ns)
            L10N_PATTERN = etree.Element("{{{0}}}pattern".format(ns), value="$l10n_.+")

            for thisTag in xmlschema_doc.iter("{{{0}}}simpleType".format(ns)):
                if thisTag.attrib["name"] == "g_l10n_string":
                    for child in thisTag:
                        if child.tag == RESTRICT_TAG:
                            child.append(L10N_PATTERN)

                    for thisTag in xmlschema_doc.iter("{{{0}}}attribute".format(ns)):
                        if thisTag.attrib["type"] == "g_l10n_string":
                            thisTag.attrib.pop("default", None)

            xmlschema     = etree.XMLSchema(xmlschema_doc)
            lxml_doc      = etree.fromstring(xmlDocument)
    except BaseException as ecc:
        textList.append("    WARNING: failed to parse XSD or XML")
        for error in ecc.error_log:
            textList.append("    Line {}: {}".format(error.line, error.message))
        return textList

    try:
        xmlschema.assertValid(lxml_doc)
    except BaseException as schema:
        textList.append("    NOTICE: Validation failed:")
        for error in schema.error_log:
            textList.append("    Line {}: {}".format(error.line, error.message))

    if len(textList) == 1:
        textList.append("    NOTICE: XML Passed Validation")

    return textList


print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
print("  xmlChecker v1.0.2")
print("    by JTSModding")
print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")

parser = argparse.ArgumentParser(description='Sanity check an xml shopItem file.')
parser.add_argument(
    'files', metavar='files', nargs='+', type=argparse.FileType('r', encoding='utf-8')
)

parser.add_argument(
    '--check-links',
    help="Check linked files for existence",
    action=argparse.BooleanOptionalAction,
    default=True
)
parser.add_argument(
    '--check-schema',
    help="Check XML against XSD Schema",
    action=argparse.BooleanOptionalAction,
    default=True
)
parser.add_argument(
    '--check-schema-l10n',
    help="Check XML against XSD Schema with $l10n type restriction",
    action=argparse.BooleanOptionalAction,
    default=True
)
parser.add_argument(
    '--install-path',
    help="Installation path to FS data files (.../data/)",
    dest="installPath",
    default=False
)

try:
    args = parser.parse_args()
except BaseException:
    enter_key_exit()

dataFilesPath    = getDataFilesPath(args.installPath)

if not hasLXML and args.check_schema:
    print("WARNING: lxml Module not available, schema checking is disabled.")

file_list = args.files

print("\nFiles Found: " + str(len(file_list)))

for file in file_list:
    cachedDataFiles  = []
    cachedLocalFiles = []
    thisName         = os.path.basename(file.name)
    thisFolder       = os.path.dirname(os.path.abspath(file.name))
    thisFileType     = None

    print("\nTesting: " + thisName)
    print("     in: " + thisFolder)

    try:
        if not file.name.endswith("xml"):
            raise BaseException
        thisFileContents = file.read().encode()
        thisXML          = ET.fromstring(thisFileContents)
    except BaseException as err:
        print(err)
        print("  ERROR: Unable to read / parse file '{0}'".format(thisName))
        enter_key_exit()

    if thisXML.tag in XSD_MAP.keys():
        thisFileType = thisXML.tag
        print("  PROCESSING: xml file is of type '{0}'".format(thisXML.tag))

        if args.check_links:
            print("\n".join(check_links(thisXML, thisFileType in DATA_DOLLAR_PATH_MAP)))

        if args.check_schema and hasLXML:
            print("\n".join(check_schema(thisFileContents, thisFileType, args.check_schema_l10n)))

    else:
        print("  ERROR: xml file is of unknown type {0}".format(thisXML.tag))
        print("  ATTEMPT: just checking links...")

        if args.check_links:
            print("\n".join(check_links(thisXML, thisXML.tag not in UNKNOWN_NO_DATA_DOLLAR)))


print('\ndone.')

if sys.stdout.isatty():
    # Don't pause on finish if we re-directed to a file.
    enter_key_exit()
