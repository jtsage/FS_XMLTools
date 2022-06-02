# pylama:ignore=W605,E221,C901
"""
        __ ______     __     _   _
        /    /      /    )   /  /|              /       /   ,
-------/----/-------\-------/| /-|----__----__-/----__-/--------__----__-
      /    /         \     / |/  |  /   ) /   /   /   /   /   /   ) /   )
_(___/____/______(____/___/__/___|_(___/_(___/___(___/___/___/___/_(___/_
                                                                      /
    i3dChecker.py - v1.0.0                                        (_ /

Version History:
 v1.0.0 - Initial Release
"""

import argparse
import os
import sys
import math
import glob
import xml.etree.ElementTree as ET
from pathlib import Path

installLocations = [
    "C:\Program Files (x86)\Farming Simulator 2022\data",
    "C:\Program Files (x86)\Steam\steamapps\common\Farming Simulator 22\data",
    "C:\Program Files\Epic Games\FarmingSimulator22\data",
]

commonMasks = [
    "0", "223", "8194", "262367", "524288", "1048576", "2097152", "2105410", "2109442", "3145728",
    "16777216", "16781314", "16781578", "16791586", "18874368", "134217728", "134225920",
    "134225922", "1073741824"
]
unusualMasks = [
    "1024", "2048", "8196", "8212", "8450", "12290", "14591", "28704", "30736", "131072", "262399",
    "524255", "2109440", "2109464", "2121728", "3170304", "16777224", "16779264", "16781312",
    "16789506", "19922944", "33554432", "1075838976", "1088421888", "1090521088", "2147483648",
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


def getDataFilesPath(override):
    """ Try and find the data files """
    installLocations = [
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
            for testPath in installLocations:
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


def enter_key_exit():
    """ Exit when enter key pressed """
    print("Press ENTER to close terminal.")
    try:
        input()
    except BaseException:
        pass
    exit()


def check_local_file_cache(filename, baseFolder):
    """ check if a local file exists, cache results to lessen IO """
    global dataFilesPath, cachedLocalFiles

    if filename in cachedLocalFiles:
        return False

    if os.path.isabs(filename):
        return(
            "    FILE ERROR: " + filename +
            " appears to be an absolute path.  This is probably wrong."
        )

    baseDrive = os.path.splitdrive(baseFolder)
    absFile   = os.path.normpath(os.path.join(baseDrive[0], baseDrive[1], filename))
    absFolder = os.path.normpath(baseFolder)

    if not os.path.exists(absFile):
        if absFile.endswith(".png"):
            absFile = absFile[:-3] + "dds"
            if not os.path.exists(absFile):
                return("    FILE NOT FOUND: " + filename)
        else:
            return("    FILE NOT FOUND: " + filename)

    casedFile = str(Path(absFile).resolve())

    if casedFile != absFile:
        return(
            "    FILE CASE MISMATCH: " + absFile.replace(absFolder, '') +
            " vs detected:" + casedFile.replace(absFolder, '')
        )

    return False


def check_data_file_cache(filename):
    """ check if a data file exists, cache results to lessen IO """
    global dataFilesPath, cachedDataFiles

    origName = filename
    filename = filename[6:]

    if filename in cachedDataFiles:
        return False

    if dataFilesPath == "":
        """ Data files not found, don't do this."""
        cachedDataFiles.append(filename)
        return False

    baseDrive = os.path.splitdrive(dataFilesPath)
    absFile   = os.path.normpath(os.path.join(baseDrive[0], baseDrive[1], filename))
    absFolder = os.path.normpath(dataFilesPath)

    if not os.path.isfile(absFile):
        if absFile.endswith(".png"):
            absFile = absFile[:-3] + "dds"
            if not os.path.exists(absFile):
                return("    FILE NOT FOUND: " + origName)
        else:
            return("    FILE NOT FOUND: " + origName)
    else:
        casedFile = str(Path(absFile).resolve())

        if casedFile == absFile:
            cachedDataFiles.append(filename)
            return False
        else:
            return(
                "    FILE CASE MISMATCH: " + absFile.replace(absFolder, '') +
                " vs detected:" + casedFile.replace(absFolder, '')
            )


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


def mask_uses_old_bits(mask):
    """ See if any of the old bits are set."""
    oldBits = [2, 6, 7, 22, 23, 26]

    binMaskReversed = format(int(mask), '032b')[::-1]

    for testBit in oldBits:
        if binMaskReversed[testBit] == "1":
            return True

    return False


def mask_string_to_hex(mask):
    """ Turn collision mask into a HEX number"""
    return "0x" + '%X' % int(mask)


def sRGB_string_to_hex(color):
    """ Convert space delimited sRGB color to HEX string"""
    if color is None:
        return "#FFFFFF"
    return "#" + "".join(['%02X' % int(math.floor(float(part) * 255)) for part in color.split()])


parser = argparse.ArgumentParser(description='Sanity check an i3d file.')
parser.add_argument(
    'files', metavar='files', nargs='+', type=argparse.FileType('r', encoding='utf-8')
)
parser.add_argument(
    '--no-shadow-check',
    help="Disable checking visible shapes for shadow maps",
    dest="noShadow",
    action='store_true'
)
parser.add_argument(
    '--no-link-check',
    help="Disable checking linked files for existence",
    dest="noLinks",
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


file_list        = args.files
cachedDataFiles  = []
cachedLocalFiles = []
dataFilesPath    = getDataFilesPath(args.installPath)

print("Files Found: " + str(len(file_list)))

for file in file_list:
    thisName   = os.path.basename(file.name)
    thisFolder = os.path.dirname(os.path.abspath(file.name))
    lightsInfo = ["\nRealLights Information:"]
    colInfo    = ["\nUnknown, uncommon, or depreciated collisionMasks:"]
    linkLight  = ["\nLinks to old lights in i3d:"]
    linkPath   = ["\nCheck path of linked files:"]
    shadows    = ["\nhasShadowMap | castsShadowMap on renderable shapes:"]

    print("\nTesting: " + thisName)
    try:
        thisXML    = ET.fromstring(file.read())
    except BaseException:
        print("ERROR: Unable to read / parse file '" + thisName + "'")
        enter_key_exit()

    foundBadLink = False
    badCache     = []
    for thisTag in thisXML.findall(".//File"):
        thisFileName = none_attrib(thisTag, "filename")
        if thisFileName is not None and thisFileName not in badCache:
            if thisFileName.startswith("$data/"):
                fileStatus = check_data_file_cache(thisFileName)
            else:
                fileStatus = check_local_file_cache(thisFileName, thisFolder)

            if fileStatus is not False:
                foundBadLink = True
                linkPath.append(fileStatus)
                badCache.append(thisFileName)

    if not foundBadLink:
        linkPath.append("  all good.")

    foundLights = False
    for thisTag in thisXML.findall(".//Light"):
        foundLights = True
        lightsInfo.append("  Node Name: " + na_attrib(thisTag, "name"))
        thisLine  = "   Type: " + na_attrib(thisTag, "type")
        thisLine += ", Color: " + sRGB_string_to_hex(none_attrib(thisTag, "color"))
        thisLine += ", Shadows: " + yn_attrib(thisTag, "castShadowMap")
        thisLine += ", Range: " + na_attrib(thisTag, "range") + " m"
        thisLine += ", Cone Angle: " + na_attrib(thisTag, "coneAngle") + " °"
        thisLine += ", Drop Off: " + na_attrib(thisTag, "dropOff") + " m"
        lightsInfo.append(thisLine)

    if not foundLights:
        lightsInfo.append("  no lights found.")

    foundBadShadows = False
    for thisTag in thisXML.findall(".//Shape"):
        thisTagNonRender = none_attrib(thisTag, "nonRenderable")
        thisTagCasts     = none_attrib(thisTag, "castsShadows")
        thisTagReceives  = none_attrib(thisTag, "receiveShadows")

        if (not is_xml_true(thisTagReceives) or not is_xml_true(thisTagCasts)):
            # Either missing cast or receive, check visible...
            if (not is_xml_true(thisTagNonRender)):
                foundBadShadows = True
                shadows.append("  Node Name: " + na_attrib(thisTag, "name"))
                shadows.append(
                    "   Casts Shadow Map: " + yn_attrib(thisTag, "castsShadows") +
                    " | Receives Shadow Map: " + yn_attrib(thisTag, "receiveShadows")
                )

    if not foundBadShadows:
        shadows.append("  none found.")

    foundBadLight = False
    for thisTag in thisXML.findall(".//File"):
        thisFileName = none_attrib(thisTag, "filename")
        if thisFileName is not None:
            for thisTestName in lightMap.keys():
                if thisTestName + "." in thisFileName:
                    foundBadLight = True
                    linkLight.append(
                        "  Linked Light with fileId '" + na_attrib(thisTag, "fileId") +
                        "' is '" + thisTestName + "', should be '" +
                        lightMap[thisTestName] + "'"
                    )
    if not foundBadLight:
        linkLight.append("  none found.")

    foundBadCol = False

    for thisTag in thisXML.findall(".//*[@collisionMask]"):
        thisColMaskDec = none_attrib(thisTag, "collisionMask")
        thisColMaskHex = mask_string_to_hex(thisColMaskDec)
        thisName       = na_attrib(thisTag, "name")
        if thisColMaskDec not in commonMasks:
            foundBadCol = True
            if thisColMaskDec in unusualMasks:
                colInfo.append(
                    "  collisionMask for '" + thisName + "' (" + thisColMaskDec + ")/(" +
                    thisColMaskHex + ") is unusual, but does exist in some giants files"
                )
            else:
                if mask_uses_old_bits(thisColMaskDec):
                    colInfo.append(
                        "  collisionMask for '" + thisName + "' (" + thisColMaskDec + ")/(" +
                        thisColMaskHex + ") uses depreciated bits and needs corrected"
                    )
                else:
                    colInfo.append(
                        "  collisionMask for '" + thisName + "' (" + thisColMaskDec + ")/(" +
                        thisColMaskHex + ") is unknown, and should be checked"
                    )

    if not foundBadCol:
        colInfo.append("  none found.")

    if not args.noLightInfo:
        print("\n".join(lightsInfo))
    if not args.noLights:
        print("\n".join(linkLight))
    if not args.noShadow:
        print("\n".join(shadows))
    if not args.noColInfo:
        print("\n".join(colInfo))
    if not args.noLinks:
        print("\n".join(linkPath))

print('\ndone.')

if sys.stdout.isatty():
    # Don't pause on finish if we re-directed to a file.
    enter_key_exit()
