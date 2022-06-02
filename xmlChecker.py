# pylama:ignore=W605,E221,C901
"""
        __ ______     __     _   _
        /    /      /    )   /  /|              /       /   ,
-------/----/-------\-------/| /-|----__----__-/----__-/--------__----__-
      /    /         \     / |/  |  /   ) /   /   /   /   /   /   ) /   )
_(___/____/______(____/___/__/___|_(___/_(___/___(___/___/___/___/_(___/_
                                                                      /
    xmlChecker.py - v1.0.0                                        (_ /

Version History:
 v1.0.0 - Initial Release
"""

import argparse
import os
import sys
import urllib.request
import posixpath
import json
import re
import glob
import xml.etree.ElementTree as ET

hasLXML = True

try:
    from lxml import etree
except ImportError:
    hasLXML = False

giantsWebsite = "https://validation.gdn.giants-software.com/xml/fs22/"

installLocations = [
    "C:\Program Files (x86)\Farming Simulator 2022\data",
    "C:\Program Files (x86)\Steam\steamapps\common\Farming Simulator 22\data",
    "C:\Program Files\Epic Games\FarmingSimulator22\data",
]

xsdMap = {
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

filename_attributes = [
    "filename",
    "textureFilename",
    "densityMaskFilename",
    "xmlFilename",
    "i3dFilename",
]

lightMap = {
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


def findInstalledEditor():
    localAppData  = os.getenv('localappdata')
    editorFolders = glob.glob(localAppData + "/GIANTS Editor*")
    editorVersion = 0
    editorFolder  = False

    try:
        if len(editorFolders):
            for thisFolder in editorFolders:
                versionInt = int(thisFolder[-5:].replace(".", ""))
                if editorVersion < versionInt:
                    editorFolder = thisFolder
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

    if lightname in lightMap.keys():
        return lightMap[lightname]
    else:
        return False


def check_file_cache(filename):
    """ check if a data file exists, cache results to lessen IO """
    global dataFilesPath, cachedFiles

    filename = filename[5:]

    if filename in cachedFiles:
        return True

    fullpath = dataFilesPath.replace(os.sep, posixpath.sep) + filename

    if os.path.isfile(fullpath):
        cachedFiles.append(filename)
        return True

    return False


def print_dep_notice(current, new):
    if current.startswith("."):
        current = current[1:]
        if new is not False:
            new = new[1:]

    if new is False:
        print("    Depreciated usage found: '" + current + "' has been removed")
    else:
        print("    Depreciated usage found: '" + current + "' is now '" + new + "'")


def giants_to_xpath(type, path):
    """ convert giants xml notation to xpath """
    newPath = path
    if (path.startswith(type)):
        newPath = re.sub("\(0\)", "", newPath)
        newPath = re.sub("\(\?\)", "", newPath)
        newPath = re.sub("\.", "/", newPath)
        newPath = re.sub("^" + type + "/", "./", newPath)
        newPath = re.sub("^(.+)#(.+)$", '\g<1>[@\g<2>]', newPath)
    elif (path.startswith(".")):
        newPath = re.sub("\(0\)", "", newPath)
        newPath = re.sub("\.", "/", newPath)
        newPath = re.sub("^(.+)#(.+)$", '\g<1>[@\g<2>]', newPath)
        newPath = "./" + newPath
    elif (path.startswith("#")):
        newPath = re.sub("^#(.+)$", '[@\g<1>]', newPath)
        newPath = ".//*" + newPath
    else:
        print(path + " was not translated")

    return newPath


def enter_key_exit():
    """ Exit when enter key pressed """
    print("Press ENTER to close terminal.")
    input()
    exit()


parser = argparse.ArgumentParser(description='Sanity check an xml shopItem file.')
parser.add_argument(
    'files', metavar='files', nargs='+', type=argparse.FileType('r', encoding='utf-8')
)
parser.add_argument(
    '--no-depre-check',
    help="Disable checking depreciated xml tags and attributes",
    dest="noDepre",
    action='store_true'
)
parser.add_argument(
    '--no-file-check',
    help="Disable checking linked files",
    dest="noFiles",
    action='store_true'
)
parser.add_argument(
    '--no-schema',
    help="Disable checking schema",
    dest="noSchema",
    action='store_true'
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

try:
    f = open('xmlChecker_data.json')
    depreMap = json.load(f)
except BaseException:
    print("Failed to load data file - make sure you have the json file too!")
    enter_key_exit()

dataFilesPath = ""
cachedFiles   = []

if args.installPath is not False:
    if (
        not args.installPath.endswith("data/")
        and not args.installPath.endswith("data")
        and not args.installPath.endswith("data/")
    ):
        print("WARNING: DATA FILES NOT FOUND: supplied path should end with \"data\\\"")
    elif not os.path.isdir(args.installPath):
        print("WARNING: DATA FILES NOT FOUND: Invalid Path Supplied")
    else:
        dataFilesPath = args.installPath
else:
    editPath = findInstalledEditor()
    if editPath:
        dataFilesPath = editPath
    else:
        for testPath in installLocations:
            if os.path.isdir(testPath) and dataFilesPath == "":
                dataFilesPath = testPath

if dataFilesPath == "":
    print("WARNING: DATA FILES NOT FOUND: checking linked $data entries disabled.")

if not hasLXML:
    print("WARNING: lxml Module not available, schema checking is disabled.")

file_list = args.files

print("\nFiles Found: " + str(len(file_list)))

for file in file_list:
    thisName   = os.path.basename(file.name)
    depreInfo  = ["\nUnknown, uncommon, or depreciated collisionMasks:"]
    linkLight  = ["\nLinks to old lights in i3d:"]
    schema     = ["\nhasShadowMap | castsShadowMap on renderable shapes:"]
    goodFile   = False

    print("\nTesting: " + thisName)

    try:
        thisFileC  = file.read().encode()
        thisXML    = ET.fromstring(thisFileC)
    except BaseException:
        print("ERROR: Unable to read / parse file '" + thisName + "'")
        enter_key_exit()

    for xmlType in xsdMap.keys():
        if thisXML.tag == xmlType:
            goodFile = xmlType
            print("  PROCESSING: xml file is of type '" + xmlType + "'")

    if goodFile is not False:
        if not args.noDepre:
            keepGoing = True
            print("  PROCESSING: depreciated tags / attributes:")
            thisDepTree = depreMap[thisXML.tag]

            if len(thisDepTree):
                for thisDepTest in thisDepTree.keys():
                    thisDepXPath = giants_to_xpath(goodFile, thisDepTest)
                    foundIt = False
                    if thisXML.findall(thisDepXPath):
                        keepGoing = False
                        print_dep_notice(thisDepTest, thisDepTree[thisDepTest])

            if keepGoing:
                print("    NOTICE: no depreciated tags detected.")

        if not args.noFiles:
            keepGoing = True
            print("  PROCESSING: checking file links")

            badCache = []
            for file_key in filename_attributes:
                for thisTag in thisXML.findall(".//*[@" + file_key + "]"):
                    thisKeyValue = thisTag.attrib[file_key]
                    if thisKeyValue.startswith("$data/"):
                        if thisKeyValue not in badCache:
                            if not check_file_cache(thisKeyValue):
                                badCache.append(thisKeyValue)
                                keepGoing = False
                                if check_new_light(thisKeyValue):
                                    print(
                                        "    FILE NOT FOUND: " + thisKeyValue +
                                        " (new name:" + check_new_light(thisKeyValue) + ")"
                                    )
                                else:
                                    print("    FILE NOT FOUND: " + thisKeyValue)
            if keepGoing:
                print("    NOTICE: no missing linked file detected.")

        if not args.noSchema and hasLXML:
            print("  PROCESSING: Checking against XSD Schema")
            keepGoing = True

            try:
                data = urllib.request.urlopen(giantsWebsite + xsdMap[goodFile])
            except BaseException:
                keepGoing = False
                print("    WARNING: Loading XSD from giants validation server failed")

            if keepGoing:
                try:
                    xmlschema_doc = etree.parse(data)
                    xmlschema     = etree.XMLSchema(xmlschema_doc)

                    lxml_doc = etree.fromstring(thisFileC)
                except BaseException as ecc:
                    keepGoing = False
                    print(ecc)
                    print("    WARNING: failed to parse XSD or XML")

            if keepGoing:
                try:
                    xmlschema.assertValid(lxml_doc)
                except BaseException as schema:
                    keepGoing = False
                    print("    NOTICE: Validation failed:")
                    for error in schema.error_log:
                        print("    Line {}: {}".format(error.line, error.message))

            if keepGoing:
                print("    NOTICE: XML Passed Validation")

print('\ndone.')

if sys.stdout.isatty():
    # Don't pause on finish if we re-directed to a file.
    enter_key_exit()
