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
import math
import xml.etree.ElementTree as ET

hasLXML = True

try:
    from lxml import etree
except ImportError:
    hasLXML = False

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


parser = argparse.ArgumentParser(description='Sanity check an xml shopItem file.')
parser.add_argument(
    'files', metavar='files', nargs='+', type=argparse.FileType('r', encoding='utf-8')
)
parser.add_argument(
    '--no-depre-check',
    help="Disable checking depreciated xml tags and attributes",
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

dataFilesPath = ""

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
    for testPath in installLocations:
        if os.path.isdir(testPath) and dataFilesPath == "" :
            dataFilesPath = testPath

if dataFilesPath == "":
    print("WARNING: DATA FILES NOT FOUND: checking linked $data entries disabled.")

if not hasLXML:
    print("WARNING: lxml Module not available, schema checking is disabled.")

file_list = args.files

print("Files Found: " + str(len(file_list)))

exit()
for file in file_list:
    thisName   = os.path.basename(file.name)
    depreInfo  = ["\nUnknown, uncommon, or depreciated collisionMasks:"]
    linkLight  = ["\nLinks to old lights in i3d:"]
    schema     = ["\nhasShadowMap | castsShadowMap on renderable shapes:"]

    print("\nTesting: " + thisName)
    try:
        thisXML    = ET.fromstring(file.read())
    except BaseException:
        print("ERROR: Unable to read / parse file '" + thisName + "'")
        enter_key_exit()

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

print('\ndone.')

if sys.stdout.isatty():
    # Don't pause on finish if we re-directed to a file.
    enter_key_exit()



    """
AstroGrep Results
-------------------------------------------------------
checkDeprecatedXML was found 525 times in 74 files


Search Options
-------------------------------------------------------
Search Paths: C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5
File Types: *.lua
Regular Expressions: False
Case Sensitive: False
Whole Word: False
Subfolders: True
Show File Names Only: False
Negation: False
Line Numbers: True
Remove Leading White Space: False
Context Lines: 0
Exclusions:
	File -> Extension: .exe 
	File -> Extension: .dll 
	File -> Extension: .pdb 
	File -> Extension: .msi 
	File -> Extension: .sys 
	File -> Extension: .ppt 
	File -> Extension: .gif 
	File -> Extension: .jpg 
	File -> Extension: .jpeg 
	File -> Extension: .png 
	File -> Extension: .bmp 
	File -> Extension: .class 
	File -> Extension: .chm 
	Directory -> Name: .git Equals
	Directory -> Name: .hg Equals
	Directory -> Name: .svn Equals
	Directory -> Name: .cvs Equals
	Directory -> Name: .metadata Equals
	Directory -> Name: .settings Equals


Results
------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\effects\MotionPathEffect.lua
------------------------------------------------------------------------------------
54: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#lengthAndRadius")

--------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\placeables\Placeable.lua
--------------------------------------------------------------------------------
272: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "placeable.filename", "placeable.base.filename")
273: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "placeable.dayNightObjects", "Visiblity Condition-Tab in GIANTS Editor / Exporter")

--------------------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\placeables\specializations\PlaceableLeveling.lua
--------------------------------------------------------------------------------------------------------
63: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "placeable.leveling.rampAreas.rampArea", "placeable.leveling.levelAreas.levelArea")

---------------------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\placeables\specializations\PlaceablePlacement.lua
---------------------------------------------------------------------------------------------------------
60: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "placeable.placement#sizeX")
61: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "placeable.placement#sizeZ")
62: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "placeable.placement#sizeOffsetX")
63: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "placeable.placement#sizeOffsetZ")
64: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "placeable.placement#testSizeX", "placeable.placement.testAreas.testArea")
65: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "placeable.placement#testSizeZ", "placeable.placement.testAreas.testArea")
66: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "placeable.placement#testSizeOffsetX", "placeable.placement.testAreas.testArea")
67: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "placeable.placement#testSizeOffsetZ", "placeable.placement.testAreas.testArea")

-------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\sounds\SoundManager.lua
-------------------------------------------------------------------------------
258: 			XMLUtil.checkDeprecatedXMLElements(xmlFileObject, baseKey .. "#externalSoundFile", "vehicle.base.sounds#filename")

--------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\triggers\LoadTrigger.lua
--------------------------------------------------------------------------------
45: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, xmlNode .. "#scrollerIndex", xmlNode .. "#scrollerNode")

----------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\utils\ObjectChangeUtil.lua
----------------------------------------------------------------------------------
66: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, "", key .. "#collisionActive", key .. "#compoundChildActive or #rigidBodyTypeActive")
67: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, "", key .. "#collisionInactive", key .. "#compoundChildInactive or #rigidBodyTypeInactive")

-------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\utils\XMLUtil.lua
-------------------------------------------------------------------------
67: 	checkDeprecatedXMLElements = function (xmlFile, oldElement, newElement, oldValue, checkForValue)

----------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\Vehicle.lua
----------------------------------------------------------------------------
613: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.filename", "vehicle.base.filename")
625: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.forcedMapHotspotType", "vehicle.base.mapHotspot#type")
626: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.base.forcedMapHotspotType", "vehicle.base.mapHotspot#type")
627: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.speedLimit#value", "vehicle.base.speedLimit#value")
628: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.steeringAxleNode#index", "vehicle.base.steeringAxle#node")
629: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.size#width", "vehicle.base.size#width")
630: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.size#length", "vehicle.base.size#length")
631: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.size#widthOffset", "vehicle.base.size#widthOffset")
632: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.size#lengthOffset", "vehicle.base.size#lengthOffset")
633: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.typeDesc", "vehicle.base.typeDesc")
634: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.components", "vehicle.base.components")
635: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.components.component", "vehicle.base.components.component")
636: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.base.components.component1", "vehicle.base.components.component")
809: 		XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. "#index", key .. "#node")
3106: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. "#indexActor1", key .. "#nodeActor1")
3398: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.schemaOverlay#file")
3399: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.schemaOverlay#width")
3400: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.schemaOverlay#height")
3401: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.schemaOverlay#invisibleBorderRight", "vehicle.base.schemaOverlay#invisibleBorderRight")
3402: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.schemaOverlay#invisibleBorderLeft", "vehicle.base.schemaOverlay#invisibleBorderLeft")
3403: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.schemaOverlay#attacherJointPosition", "vehicle.base.schemaOverlay#attacherJointPosition")
3404: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.schemaOverlay#basePosition", "vehicle.base.schemaOverlay#basePosition")
3405: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.schemaOverlay#fileSelected")
3406: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.schemaOverlay#fileTurnedOn")
3407: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.schemaOverlay#fileSelectedTurnedOn")
3408: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.base.schemaOverlay.default#name", "vehicle.base.schemaOverlay#name")
3409: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.base.schemaOverlay.turnedOn#name")
3410: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.base.schemaOverlay.selected#name")
3411: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.base.schemaOverlay.turnedOnSelected#name")
3414: 		XMLUtil.checkDeprecatedXMLElements(xmlFile, "vehicle.schemaOverlay.attacherJoint", "vehicle.attacherJoints.attacherJoint.schema")

----------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\VehicleCamera.lua
----------------------------------------------------------------------------------
65: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, self.vehicle.configFileName, key .. "#index", "#node")
241: 		XMLUtil.checkDeprecatedXMLElements(xmlFile, self.vehicle.configFileName, raycastKey .. "#index", raycastKey .. "#node")

-------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\VehicleCharacter.lua
-------------------------------------------------------------------------------------
21: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, xmlNode .. "#index", xmlNode .. "#node")

------------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\AIImplement.lua
------------------------------------------------------------------------------------------------
134: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, baseName .. ".areaMarkers#leftIndex", baseName .. ".areaMarkers#leftNode")
135: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, baseName .. ".areaMarkers#rightIndex", baseName .. ".areaMarkers#rightNode")
136: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, baseName .. ".areaMarkers#backIndex", baseName .. ".areaMarkers#backNode")
137: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, baseName .. ".sizeMarkers#leftIndex", baseName .. ".sizeMarkers#leftNode")
138: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, baseName .. ".sizeMarkers#rightIndex", baseName .. ".sizeMarkers#rightNode")
139: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, baseName .. ".sizeMarkers#backIndex", baseName .. ".sizeMarkers#backNode")
140: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, baseName .. ".trafficCollisionTrigger#index", baseName .. ".collisionTrigger#node")
141: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, baseName .. ".trafficCollisionTrigger#node", baseName .. ".collisionTrigger#node")
142: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, baseName .. ".collisionTrigger#index", baseName .. ".collisionTrigger#node")
143: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.aiLookAheadSize#value", baseName .. ".lookAheadSize#value")
144: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, baseName .. ".toolReverserDirectionNode#index", baseName .. ".toolReverserDirectionNode#node")
145: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, baseName .. ".turningRadiusLimiation", baseName .. ".turningRadiusLimitation")
146: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, baseName .. ".forceTurnNoBackward#value", baseName .. ".allowTurnBackward#value (inverted)")
147: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, baseName .. ".needsLowering#lowerIfAnyIsLowerd", baseName .. ".allowTurnBackward#lowerIfAnyIsLowered")

----------------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\ArticulatedAxis.lua
----------------------------------------------------------------------------------------------------
47: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.articulatedAxis.rotatingPart(0)#index", "vehicle.articulatedAxis.rotatingPart(0)#node")

-----------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\Attachable.lua
-----------------------------------------------------------------------------------------------
265: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.attacherJoint", "vehicle.inputAttacherJoints.inputAttacherJoint")
266: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.needsLowering", "vehicle.inputAttacherJoints.inputAttacherJoint#needsLowering")
267: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.allowsLowering", "vehicle.inputAttacherJoints.inputAttacherJoint#allowsLowering")
268: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.isDefaultLowered", "vehicle.inputAttacherJoints.inputAttacherJoint#isDefaultLowered")
269: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.forceSelectionOnAttach#value", "vehicle.inputAttacherJoints.inputAttacherJoint#forceSelectionOnAttach")
270: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.topReferenceNode#index", "vehicle.attacherJoint#topReferenceNode")
271: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.attachRootNode#index", "vehicle.attacherJoint#rootNode")
272: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.inputAttacherJoints", "vehicle.attachable.inputAttacherJoints")
273: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.inputAttacherJointConfigurations", "vehicle.attachable.inputAttacherJointConfigurations")
274: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.brakeForce", "vehicle.attachable.brakeForce#force")
275: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.attachable.brakeForce", "vehicle.attachable.brakeForce#force", nil, true)
276: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.steeringAxleAngleScale", "vehicle.attachable.steeringAxleAngleScale")
277: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.support", "vehicle.attachable.support")
278: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.lowerAnimation", "vehicle.attachable.lowerAnimation")
279: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.toolCameras", "vehicle.attachable.toolCameras")
280: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.attachable.toolCameras#count", "vehicle.attachable.toolCameras")
281: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.attachable.toolCameras.toolCamera1", "vehicle.attachable.toolCamera")
282: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.attachable.toolCameras.toolCamera2", "vehicle.attachable.toolCamera")
283: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.attachable.toolCameras.toolCamera3", "vehicle.attachable.toolCamera")
284: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.foldable.foldingParts#onlyFoldOnDetach", "vehicle.attachable#allowFoldingWhileAttached")
285: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.maximalAirConsumptionPerFullStop", "vehicle.attachable.airConsumer#usage (is now in usage per second at full brake power)")
286: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.attachable.steeringAxleAngleScale#targetNode", "vehicle.attachable.steeringAxleAngleScale.targetNode#node")
703: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#index", key .. "#node")
704: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#indexVisual", key .. "#nodeVisual")
705: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#ptoInputNode", "vehicle.powerTakeOffs.input")
706: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#lowerDistanceToGround", key .. ".distanceToGround#lower")
707: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#upperDistanceToGround", key .. ".distanceToGround#upper")

---------------------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\AttacherJointControl.lua
---------------------------------------------------------------------------------------------------------
59: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.attacherJointControl.control1", "vehicle.attacherJointControl.control with #controlFunction 'controlAttacherJointHeight'")
60: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.attacherJointControl.control2", "vehicle.attacherJointControl.control with #controlFunction 'controlAttacherJointTilt'")
108: 		XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. "#controlAxisIcon", key .. "#iconName")

---------------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\AttacherJoints.lua
---------------------------------------------------------------------------------------------------
2728: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, baseName .. "#index", baseName .. "#node")
2729: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, baseName .. "#indexVisual", baseName .. "#nodeVisual")
2730: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, baseName .. "#ptoOutputNode", "vehicle.powerTakeOffs.output")
2731: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, baseName .. "#lowerDistanceToGround", baseName .. ".distanceToGround#lower")
2732: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, baseName .. "#upperDistanceToGround", baseName .. ".distanceToGround#upper")
2733: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, baseName .. "#rotationNode", baseName .. ".rotationNode#node")
2734: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, baseName .. "#upperRotation", baseName .. ".rotationNode#upperRotation")
2735: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, baseName .. "#lowerRotation", baseName .. ".rotationNode#lowerRotation")
2736: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, baseName .. "#startRotation", baseName .. ".rotationNode#startRotation")
2737: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, baseName .. "#rotationNode2", baseName .. ".rotationNode2#node")
2738: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, baseName .. "#upperRotation2", baseName .. ".rotationNode2#upperRotation")
2739: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, baseName .. "#lowerRotation2", baseName .. ".rotationNode2#lowerRotation")
2740: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, baseName .. "#transNode", baseName .. ".transNode#node")
2741: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, baseName .. "#transNodeMinY", baseName .. ".transNode#minY")
2742: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, baseName .. "#transNodeMaxY", baseName .. ".transNode#maxY")
2743: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, baseName .. "#transNodeHeight", baseName .. ".transNode#height")

-----------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\BaleLoader.lua
-----------------------------------------------------------------------------------------------
261: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleloaderTurnedOnScrollers.baleloaderTurnedOnScroller", "vehicle.baleLoader.animationNodes.animationNode")
262: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleGrabber", "vehicle.baleLoader.grabber")
263: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.balePlaces", "vehicle.baleLoader.balePlaces")
264: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.grabParticleSystem", "vehicle.baleLoader.grabber.grabParticleSystem")
265: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleLoader.grabber.grabParticleSystem", "vehicle.baleLoader.grabber.effectNode")
266: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleLoader#pickupRange", "vehicle.baleLoader.grabber#pickupRange")
267: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleTypes", "vehicle.baleLoader.baleTypes")
268: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleLoader#textTransportPosition", "vehicle.baleLoader.texts#transportPosition")
269: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleLoader#textOperatingPosition", "vehicle.baleLoader.texts#operatingPosition")
270: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleLoader#textUnload", "vehicle.baleLoader.texts#unload")
271: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleLoader#textTilting", "vehicle.baleLoader.texts#tilting")
272: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleLoader#textLowering", "vehicle.baleLoader.texts#lowering")
273: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleLoader#textLowerPlattform", "vehicle.baleLoader.texts#lowerPlattform")
274: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleLoader#textAbortUnloading", "vehicle.baleLoader.texts#abortUnloading")
275: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleLoader#textUnloadHere", "vehicle.baleLoader.texts#unloadHere")
276: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleLoader#rotatePlatformAnimName", "vehicle.baleLoader.animations#rotatePlatform")
277: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleLoader#rotatePlatformBackAnimName", "vehicle.baleLoader.animations#rotatePlatformBack")
278: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleLoader#rotatePlatformEmptyAnimName", "vehicle.baleLoader.animations#rotatePlatformEmpty")
279: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleLoader.animations#grabberDropBaleReverseSpeed", "vehicle.baleLoader.animations.baleGrabber#dropBaleReverseSpeed")
280: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleLoader.animations#grabberDropToWork", "vehicle.baleLoader.animations.baleGrabber#dropToWork")
281: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleLoader.animations#rotatePlatform", "vehicle.baleLoader.animations.platform#rotate")
282: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleLoader.animations#rotatePlatformBack", "vehicle.baleLoader.animations.platform#rotateBack")
283: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleLoader.animations#rotatePlatformEmpty", "vehicle.baleLoader.animations.platform#rotateEmpty")
284: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleLoader#moveBalePlacesAfterRotatePlatform", "vehicle.baleLoader.animations.moveBalePlaces#moveAfterRotatePlatform")
285: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleLoader#moveBalePlacesMaxGrabberTime", "vehicle.baleLoader.animations.moveBalePlaces#maxGrabberTime")
286: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleLoader#alwaysMoveBalePlaces", "vehicle.baleLoader.animations.moveBalePlaces#alwaysMove")
287: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleLoader#resetEmptyRotateAnimation", "vehicle.baleLoader.animations.emptyRotate#reset")

------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\Baler.lua
------------------------------------------------------------------------------------------
185: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.fillScale#value", "vehicle.baler#fillScale")
186: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.turnedOnRotationNodes.turnedOnRotationNode#type", "vehicle.baler.animationNodes.animationNode", "baler")
187: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baler.balingAnimation#name", "vehicle.turnOnVehicle.turnedOnAnimation#name")
188: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baler.fillParticleSystems", "vehicle.baler.fillEffect with effectClass 'ParticleEffect'")
189: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baler.uvScrollParts.uvScrollPart", "vehicle.baler.animationNodes.animationNode")
190: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baler.balerAlarm", "vehicle.fillUnit.fillUnitConfigurations.fillUnitConfiguration.fillUnits.fillUnit.alarmTriggers.alarmTrigger.alarmSound")
191: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baler.baleAnimation#node", "vehicle.baler.baleTypes.baleType#baleNode")
192: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baler.baleAnimation#baleNode", "vehicle.baler.baleTypes.baleType#baleNode")
193: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baler.baleAnimation#scaleNode", "vehicle.baler.baleTypes.baleType#scaleNode")
194: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baler.baleAnimation#baleScaleComponent", "vehicle.baler.baleTypes.baleType#scaleComponents")
195: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baler.baleAnimation#unloadAnimationName", "vehicle.baler.baleTypes.baleType#unloadAnimation")
196: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baler.baleAnimation#unloadAnimationSpeed", "vehicle.baler.baleTypes.baleType#unloadAnimationSpeed")
197: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baler.baleAnimation#baleDropAnimTime", "vehicle.baler.baleTypes.baleType#dropAnimationTime")
198: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baler#toggleAutomaticDropTextPos", "vehicle.baler.automaticDrop#textPos")
199: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baler#toggleAutomaticDropTextNeg", "vehicle.baler.automaticDrop#textNeg")
200: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baler.baleAnimation#firstBaleMarker", "Please adjust bale nodes to match the default balers")
212: 			XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. "#time")

------------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\BaleWrapper.lua
------------------------------------------------------------------------------------------------
197: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.wrapper", "vehicle.baleWrapper")
198: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleGrabber", "vehicle.baleWrapper.grabber")
199: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleWrapper.grabber#index", "vehicle.baleWrapper.grabber#node")
200: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleWrapper.grabber#index", "vehicle.baleWrapper.grabber#node")
201: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleWrapper.roundBaleWrapper#baleIndex", "vehicle.baleWrapper.roundBaleWrapper#baleNode")
202: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleWrapper.roundBaleWrapper#wrapperIndex", "vehicle.baleWrapper.roundBaleWrapper#wrapperNode")
203: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleWrapper.squareBaleWrapper#baleIndex", "vehicle.baleWrapper.squareBaleWrapper#baleNode")
204: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.baleWrapper.squareBaleWrapper#wrapperIndex", "vehicle.baleWrapper.squareBaleWrapper#wrapperNode")
317: 		XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. "#fillType")
318: 		XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. "#wrapperBaleFilename")
319: 		XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. "#minBaleDiameter", key .. "#diameter")
320: 		XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. "#maxBaleDiameter", key .. "#diameter")
321: 		XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. "#minBaleWidth", key .. "#width")
322: 		XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. "#maxBaleWidth", key .. "#width")
323: 		XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. "#minBaleHeight", key .. "#height")
324: 		XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. "#maxBaleHeight", key .. "#height")
325: 		XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. "#minBaleLength", key .. "#length")
326: 		XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. "#maxBaleLength", key .. "#length")
377: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, baseKey .. "#skipWrappingFillTypes", baseKey .. "#skipUnsupportedBales")
455: 		XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. "#index", key .. "#node")
524: 		XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. "#index", key .. "#node")

--------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\Combine.lua
--------------------------------------------------------------------------------------------
159: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.combine.chopperSwitch", "vehicle.combine.swath and vehicle.combine.chopper")
160: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.turnedOnRotationNodes.turnedOnRotationNode#type", "vehicle.combine.rotationNodes.rotationNode", "combine")
161: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.indoorHud.workedHectars", "vehicle.combine.dashboards.dashboard with valueType 'workedHectars'")
162: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.combine.folding#fillLevelThreshold", "vehicle.combine.folding#fillLevelThresholdPct")
751: 		XMLUtil.checkDeprecatedXMLElements(xmlFile, baseKey .. ".chopperParticleSystems", baseKey .. ".chopperEffect")
752: 		XMLUtil.checkDeprecatedXMLElements(xmlFile, baseKey .. ".strawParticleSystems", baseKey .. ".strawEffect")
753: 		XMLUtil.checkDeprecatedXMLElements(xmlFile, baseKey .. ".threshingFillParticleSystems", baseKey .. ".fillEffect")

------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\Cover.lua
------------------------------------------------------------------------------------------
73: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.cover#animationName", "vehicle.cover.coverConfigurations.coverConfiguration.cover#openAnimation")
74: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.foldable.foldingParts#closeCoverOnFold", "vehicle.cover.coverConfigurations.coverConfiguration.cover#closeCoverIfNotAllowed")

---------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\Crawlers.lua
---------------------------------------------------------------------------------------------
197: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#crawlerIndex", "Moved to external crawler config file")
198: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#length", "Moved to external crawler config file")
199: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#shaderParameterComponent", "Moved to external crawler config file")
200: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#shaderParameterName", "Moved to external crawler config file")
201: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#scrollLength", "Moved to external crawler config file")
202: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#scrollSpeed", "Moved to external crawler config file")
203: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#index", "Moved to external crawler config file")
204: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. ".rotatingPart", "Moved to external crawler config file")
205: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#linkIndex", key .. "#linkNode")
226: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#speedRefWheel", key .. "#wheelIndex")
260: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, self.configFileName, key .. "#speedRefNode", key .. "#speedReferenceNode")

-----------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\Cultivator.lua
-----------------------------------------------------------------------------------------------
84: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.cultivator.directionNode#index", "vehicle.cultivator.directionNode#node")

-------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\Cutter.lua
-------------------------------------------------------------------------------------------
103: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.turnedOnRotationNodes.turnedOnRotationNode#type", "vehicle.cutter.animationNodes.animationNode", "cutter")
104: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.turnedOnScrollers", "vehicle.cutter.animationNodes.animationNode")
105: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.cutter.turnedOnScrollers", "vehicle.cutter.animationNodes.animationNode")
106: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.cutter.reelspikes", "vehicle.cutter.rotationNodes.rotationNode or vehicle.turnOnVehicle.turnedOnAnimation")
107: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.cutter.threshingParticleSystems.threshingParticleSystem", "vehicle.cutter.fillEffect.effectNode")
108: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.cutter.threshingParticleSystems.emitterShape", "vehicle.cutter.fillEffect.effectNode")
109: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.cutter#convertedFillTypeCategories", "vehicle.cutter#fruitTypeConverter")
110: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.cutter#startAnimationName", "vehicle.turnOnVehicle.turnOnAnimation#name")
111: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.cutter.testAreas", "vehicle.workAreas.workArea.testAreas")
176: 			XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. "#index", key .. "#node")

-----------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\Cylindered.lua
-----------------------------------------------------------------------------------------------
330: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.movingParts", "vehicle.cylindered.movingParts")
331: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.movingTools", "vehicle.cylindered.movingTools")
332: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.cylinderedHydraulicSound", "vehicle.cylindered.sounds.hydraulic")
333: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.cylindered.movingParts#isActiveDirtyTimeOffset")
334: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.cylindered.movingParts.sounds", "vehicle.cylindered.sounds")
1352: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. ".xRotationNodes#maxDistance")
1353: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. ".xRotationNodes#transRotRatio")
1430: 				XMLUtil.checkDeprecatedXMLElements(xmlFile, xRotKey .. "#refNode")
2038: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#index", key .. "#node")
2202: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#index", key .. "#node")
2213: 		XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#rotSpeed", key .. ".rotation#rotSpeed")
2236: 		XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#transSpeed", key .. ".rotation#transSpeed")
2288: 		XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. ".controls#iconFilename", key .. ".controls#iconName")
2366: 		XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#delayedIndex", key .. "#delayedNode")
2432: 		XMLUtil.checkDeprecatedXMLElements(xmlFile, refBaseName .. "#index", refBaseName .. "#index")
2491: 		XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#index", key .. "#node")
2551: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, baseName .. "#componentJointIndex", baseName .. ".componentJoint#index")
2552: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, baseName .. "#anchorActor", baseName .. ".componentJoint#anchorActor")
2594: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, baseName .. "#jointIndices", baseName .. ".attacherJoint#jointIndices")
2617: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, baseName .. "#inputAttacherJoint", baseName .. ".inputAttacherJoint#value")
2673: 			XMLUtil.checkDeprecatedXMLElements(xmlFile, refBaseName .. "#index", refBaseName .. "#node")
2765: 		XMLUtil.checkDeprecatedXMLElements(xmlFile, refBaseName .. "#index", refBaseName .. "#node")

----------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\Dashboard.lua
----------------------------------------------------------------------------------------------
519: 		XMLUtil.checkDeprecatedXMLElements(xmlFile, self.configFileName, key .. "#hiddenAlpha")

--------------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\Dischargeable.lua
--------------------------------------------------------------------------------------------------
157: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.pipeEffect", "vehicle.dischargeable.dischargeNode.effects")

---------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\Drivable.lua
---------------------------------------------------------------------------------------------
88: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.steering#index", "vehicle.drivable.steeringWheel#node")
89: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.steering#node", "vehicle.drivable.steeringWheel#node")
90: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.cruiseControl", "vehicle.drivable.cruiseControl")
91: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.indoorHud.cruiseControl", "vehicle.drivable.dashboards.dashboard with valueType 'cruiseControl'")
92: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.showChangeToolSelectionHelp")
93: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.maxRotatedTimeSpeed#value")
94: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.speedRotScale#scale", "vehicle.drivable.speedRotScale#scale")
95: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.speedRotScale#offset", "vehicle.drivable.speedRotScale#offset")

---------------------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\DynamicMountAttacher.lua
---------------------------------------------------------------------------------------------------------
79: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.dynamicMountAttacher#index", "vehicle.dynamicMountAttacher#node")

----------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\Enterable.lua
----------------------------------------------------------------------------------------------
138: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.mirrors.mirror(0)#index", "vehicle.enterable.mirrors.mirror(0)#node")
139: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.enterReferenceNode", "vehicle.enterable.enterReferenceNode")
140: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.enterReferenceNode#index", "vehicle.enterable.enterReferenceNode#node")
141: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.enterable.enterReferenceNode#index", "vehicle.enterable.enterReferenceNode#node")
142: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.exitPoint", "vehicle.enterable.exitPoint")
143: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.exitPoint#index", "vehicle.enterable.exitPoint#node")
144: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.enterable.exitPoint#index", "vehicle.enterable.exitPoint#node")
145: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.characterNode", "vehicle.enterable.characterNode")
146: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.characterNode#index", "vehicle.enterable.characterNode#node")
147: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.enterable.characterNode#index", "vehicle.enterable.characterNode#node")
148: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.nicknameRenderNode", "vehicle.enterable.nicknameRenderNode")
149: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.enterAnimation", "vehicle.enterable.enterAnimation")
150: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.cameras.camera1", "vehicle.enterable.cameras.camera")
151: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.enterable.cameras.camera1", "vehicle.enterable.cameras.camera")
152: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.indoorHud.time", "vehicle.enterable.dashboards.dashboard with valueType 'time'")
153: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.indoorHud.operatingTime", "vehicle.enterable.dashboards.dashboard with valueType 'operatingTime'")
154: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.enterable.nicknameRenderNode#index", "vehicle.enterable.nicknameRenderNode#node")
536: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, "vehicle.cameras.camera(0)#index", "vehicle.enterable.cameras.camera(0)#node")
537: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, "vehicle.cameras.camera(0).raycastNode(0)#index", "vehicle.enterable.cameras.camera(0).raycastNode(0)#node")
582: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, xmlKey .. "#index", xmlKey .. "#node")
605: 			XMLUtil.checkDeprecatedXMLElements(xmlFile, stateKey .. "#index", stateKey .. "#node")

---------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\FillUnit.lua
---------------------------------------------------------------------------------------------
246: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.measurementNodes.measurementNode", "vehicle.fillUnit.fillUnitConfigurations.fillUnitConfiguration.fillUnits.fillUnit.measurementNodes.measurementNode")
247: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.fillPlanes.fillPlane", "vehicle.fillUnit.fillUnitConfigurations.fillUnitConfiguration.fillUnits.fillUnit.fillPlane")
248: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.foldable.foldingParts#onlyFoldOnEmpty", "vehicle.fillUnit#allowFoldingWhileFilled")
249: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.fillAutoAimTargetNode", "vehicle.fillUnit.fillUnitConfigurations.fillUnitConfiguration.fillUnits.fillUnit.autoAimTargetNode")
1478: 		XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. ".exactFillRootNode#index", key .. ".exactFillRootNode#node")
1497: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. ".autoAimTargetNode#index", key .. ".autoAimTargetNode#node")
1655: 		XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. ".fillLevelHud", key .. ".dashboard")
1715: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#index", key .. "#node")
1758: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#fillType", "Material is dynamically assigned to the nodes")
1774: 		XMLUtil.checkDeprecatedXMLElements(xmlFile, nodeKey .. "#index", nodeKey .. "#node")
2442: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, rootName .. ".storeData.specs.capacity#unit", rootName .. ".storeData.specs.capacity#unitTextOverride")
2467: 			XMLUtil.checkDeprecatedXMLElements(xmlFile, fillUnitKey .. "#unit", fillUnitKey .. "#unitTextOverride")
2588: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, rootName .. ".fillTypes", rootName .. ".cutter#fruitTypes")
2589: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, rootName .. ".fruitTypes", rootName .. ".storeData.specs.fillTypes")
2590: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, rootName .. ".fillTypeCategories", rootName .. ".storeData.specs.fillTypeCategories")

-----------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\FillVolume.lua
-----------------------------------------------------------------------------------------------
373: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#index", key .. "#node")
463: 		XMLUtil.checkDeprecatedXMLElements(xmlFile, deformerKey .. "#index", deformerKey .. "#node")
504: 		XMLUtil.checkDeprecatedXMLElements(xmlFile, infoKey .. "#index", infoKey .. "#node")
560: 		XMLUtil.checkDeprecatedXMLElements(xmlFile, nodeKey .. "#index", nodeKey .. "#node")
585: 		XMLUtil.checkDeprecatedXMLElements(xmlFile, nodeKey .. "#index", nodeKey .. "#node")

---------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\Foldable.lua
---------------------------------------------------------------------------------------------
232: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.foldingParts", "vehicle.foldable.foldingConfigurations.foldingConfiguration.foldingParts")
233: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.foldable.foldingParts", "vehicle.foldable.foldingConfigurations.foldingConfiguration.foldingParts")
909: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, "vehicle.wheels#versatileFoldMinLimit", key .. wheelnamei .. "#versatileFoldMinLimit")
910: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, "vehicle.wheels#versatileFoldMaxLimit", key .. wheelnamei .. "#versatileFoldMaxLimit")
938: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#foldMinLimit", key .. ".folding#minLimit")
939: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#foldMaxLimit", key .. ".folding#maxLimit")
1195: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#foldMinLimit", key .. ".foldable#minLimit")
1196: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#foldMaxLimit", key .. ".foldable#maxLimit")
1298: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. "#foldMinLimit", key .. ".folding#minLimit")
1299: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. "#foldMaxLimit", key .. ".folding#maxLimit")
1318: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. "#foldMinLimit", key .. ".folding#minLimit")
1319: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. "#foldMaxLimit", key .. ".folding#maxLimit")

------------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\ForageWagon.lua
------------------------------------------------------------------------------------------------
62: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.forageWagon#turnedOnTipScrollerSpeedFactor")
63: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.turnedOnRotationNodes.turnedOnRotationNode#type", "vehicle.turnOnVehicle.rotationNodes.rotationNode", "forageWagon")

--------------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\FruitPreparer.lua
--------------------------------------------------------------------------------------------------
50: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.turnOnAnimation#name", "vehicle.turnOnVehicle.turnedAnimation#name")
51: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.turnOnAnimation#speed", "vehicle.turnOnVehicle.turnedAnimation#turnOnSpeedScale")
52: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.fruitPreparer#useReelStateToTurnOn")
53: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.fruitPreparer#onlyActiveWhenLowered")
54: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.vehicle.fruitPreparerSound", "vehicle.fruitPreparer.sounds.work")
55: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.turnedOnRotationNodes.turnedOnRotationNode", "vehicle.fruitPreparer.animationNodes.animationNode", "fruitPreparer")
138: 		XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. "#dropStartIndex", key .. ".fruitPreparer#dropWorkAreaIndex")
139: 		XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. "#dropWidthIndex", key .. ".fruitPreparer#dropWorkAreaIndex")
140: 		XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. "#dropHeightIndex", key .. ".fruitPreparer#dropWorkAreaIndex")

--------------------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\GroundAdjustedNodes.lua
--------------------------------------------------------------------------------------------------------
122: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, self.configFileName, key .. "#index", key .. "#node")
182: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, self.configFileName, key .. "#index", key .. "#node")

----------------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\GroundReference.lua
----------------------------------------------------------------------------------------------------
130: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, baseName .. "#index", baseName .. "#node")
222: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. "#refNodeIndex", key .. "#groundReferenceNodeIndex")

--------------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\JigglingParts.lua
--------------------------------------------------------------------------------------------------
76: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#index", key .. "#node")

--------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\Leveler.lua
--------------------------------------------------------------------------------------------
69: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, self.configFileName, "vehicle.leveler.levelerNode#index", "vehicle.leveler.levelerNode#node")
70: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, self.configFileName, "vehicle.levelerEffects", "vehicle.leveler.effects")
71: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, self.configFileName, "vehicle.leveler.levelerNode(0)#minDropHeight")
72: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, self.configFileName, "vehicle.leveler.levelerNode(0)#maxDropHeight")

-------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\Lights.lua
-------------------------------------------------------------------------------------------
214: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.lights.low.light#decoration", "vehicle.lights.defaultLights#node")
215: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.lights.high.light#decoration", "vehicle.lights.defaultLights#node")
216: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.lights.low.light#realLight", "vehicle.lights.realLights.low.light#node")
217: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.lights.high.light#realLight", "vehicle.lights.realLights.high.light#node")
218: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.brakeLights.brakeLight#realLight", "vehicle.lights.realLights.high.brakeLight#node")
219: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.brakeLights.brakeLight#decoration", "vehicle.lights.brakeLights.brakeLight#node")
220: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.reverseLights.reverseLight#realLight", "vehicle.lights.realLights.high.reverseLight#node")
221: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.reverseLights.reverseLight#decoration", "vehicle.lights.reverseLights.reverseLight#node")
222: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.turnLights.turnLightLeft#realLight", "vehicle.lights.realLights.high.turnLightLeft#node")
223: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.turnLights.turnLightLeft#decoration", "vehicle.lights.turnLights.turnLightLeft#node")
224: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.turnLights.turnLightRight#realLight", "vehicle.lights.realLights.high.turnLightRight#node")
225: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.turnLights.turnLightRight#decoration", "vehicle.lights.turnLights.turnLightRight#node")
226: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.reverseLights.reverseLight#realLight", "vehicle.lights.realLights.high.reverseLight#node")
227: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.reverseLights.reverseLight#decoration", "vehicle.lights.reverseLights.reverseLight#node")

-------------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\ManureBarrel.lua
-------------------------------------------------------------------------------------------------
28: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.manureBarrel#toolAttachAnimName", "vehicle.attacherJoints.attacherJoint.objectChange")

-----------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\MixerWagon.lua
-----------------------------------------------------------------------------------------------
61: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.mixerWagonBaleTrigger#index", "vehicle.mixerWagon.baleTrigger#node")
62: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.mixerWagon.baleTrigger#index", "vehicle.mixerWagon.baleTrigger#node")
63: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.mixerWagonPickupStartSound", "vehicle.turnOnVehicle.sounds.start")
64: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.mixerWagonPickupStopSound", "vehicle.turnOnVehicle.sounds.stop")
65: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.mixerWagonPickupSound", "vehicle.turnOnVehicle.sounds.work")
66: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.mixerWagonRotatingParts.mixerWagonRotatingPart#type", "vehicle.mixerWagon.mixAnimationNodes.animationNode", "mixerWagonMix")
67: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.mixerWagonRotatingParts.mixerWagonRotatingPart#type", "vehicle.mixerWagon.pickupAnimationNodes.animationNode", "mixerWagonPickup")
68: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.mixerWagonRotatingParts.mixerWagonScroller", "vehicle.mixerWagon.pickupAnimationNodes.pickupAnimationNode")
69: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.mixerWagon.baleTrigger#node", "vehicle.mixerWagon.baleTriggers.baleTrigger#node")

----------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\Motorized.lua
----------------------------------------------------------------------------------------------
279: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, self.configFileName, "vehicle.turnedOnRotationNodes.turnedOnRotationNode#type", "vehicle.motor.animationNodes.animationNode", "motor")
280: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, self.configFileName, "vehicle.differentialConfigurations", "vehicle.motorized.differentialConfigurations")
281: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, self.configFileName, "vehicle.motorConfigurations", "vehicle.motorized.motorConfigurations")
282: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, self.configFileName, "vehicle.maximalAirConsumptionPerFullStop", "vehicle.motorized.consumerConfigurations.consumerConfiguration.consumer(with fill type 'air')#usage (is now in usage per second at full brake power)")
283: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, self.configFileName, "vehicle.indoorHud.rpm", "vehicle.motorized.dashboards.dashboard with valueType 'rpm'")
284: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, self.configFileName, "vehicle.indoorHud.speed", "vehicle.motorized.dashboards.dashboard with valueType 'speed'")
285: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, self.configFileName, "vehicle.indoorHud.fuelUsage", "vehicle.motorized.dashboards.dashboard with valueType 'fuelUsage'")
286: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, self.configFileName, "vehicle.indoorHud.fuel", "fillUnit.dashboard with valueType 'fillLevel'")
287: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, self.configFileName, "vehicle.motor", "vehicle.motorized.motorConfigurations.motorConfiguration(?).motor")
288: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, self.configFileName, "vehicle.transmission", "vehicle.motorized.motorConfigurations.motorConfiguration(?).transmission")
289: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, self.configFileName, "vehicle.fuelCapacity", "vehicle.motorized.consumerConfigurations.consumerConfiguration.consumer#capacity")
290: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, self.configFileName, "vehicle.motorized.motorConfigurations.motorConfiguration(?).fuelCapacity", "vehicle.motorized.consumerConfigurations.consumerConfiguration.consumer#capacity")
291: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, self.configFileName, "vehicle#consumerConfigurationIndex", "vehicle.motorized.motorConfigurations.motorConfiguration(?)#consumerConfigurationIndex'")
292: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, self.configFileName, "vehicle.motorized.exhaustParticleSystems#count")
293: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, self.configFileName, "vehicle.motorized.exhaustParticleSystems.exhaustParticleSystem1", "vehicle.motorized.exhaustParticleSystems.exhaustParticleSystem")
1423: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, self.configFileName, "vehicle.motorized.exhaustFlap#index", "vehicle.motorized.exhaustFlap#node")
1439: 		XMLUtil.checkDeprecatedXMLElements(xmlFile, self.configFileName, key .. "#index", key .. "#node")

----------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\Mountable.lua
----------------------------------------------------------------------------------------------
67: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.dynamicMount#triggerIndex", "vehicle.dynamicMount#triggerNode")

------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\Mower.lua
------------------------------------------------------------------------------------------
70: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.mowerEffects.mowerEffect", "vehicle.mower.dropEffects.dropEffect")
71: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.mowerEffects.mowerEffect#mowerCutArea", "vehicle.mower.dropEffects.dropEffect#dropAreaIndex")
72: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.turnedOnRotationNodes.turnedOnRotationNode#type", "vehicle.mower.turnOnNodes.turnOnNode", "mower")
73: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.mowerStartSound", "vehicle.turnOnVehicle.sounds.start")
74: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.mowerStopSound", "vehicle.turnOnVehicle.sounds.stop")
75: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.mowerSound", "vehicle.turnOnVehicle.sounds.work")

-------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\Pickup.lua
-------------------------------------------------------------------------------------------
158: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, "vehicle.pickupAnimation", key .. ".animation")

-----------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\Pipe.lua
-----------------------------------------------------------------------------------------
130: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.pipeEffect.effectNode", baseKey .. ".pipeEffect.effectNode")
131: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.overloading.trailerTriggers.trailerTrigger(0)#index", baseKey .. ".unloadingTriggers.unloadingTrigger(0)#node")
132: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.pipe#raycastNodeIndex", baseKey .. ".raycast#node")
133: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.pipe#raycastDistance", baseKey .. ".raycast#maxDistance")
134: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.pipe#effectExtraDistanceOnTrailer", baseKey .. ".raycast#extraDistance")
135: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.pipe#animName", baseKey .. ".animation#name")
136: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.pipe#animSpeedScale", baseKey .. ".animation#speedScale")
137: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.pipe#animSpeedScale", baseKey .. ".animation#speedScale")
138: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.pipe.node#node", baseKey .. ".node#node")
139: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.pipe#numStates", baseKey .. ".states#num")
140: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.pipe#unloadingStates", baseKey .. ".states#unloading")
141: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.pipe#autoAimingStates", baseKey .. ".states#autoAiming")
142: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.pipe#turnOnAllowed", baseKey .. ".states#turnOnAllowed")
398: 		XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. "#index", key .. "#node")
446: 			XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. ".state1", key .. ".state")

-----------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\Plow.lua
-----------------------------------------------------------------------------------------
130: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.rotationPart", "vehicle.plow.rotationPart")
131: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.ploughDirectionNode#index", "vehicle.plow.directionNode#node")
132: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.rotateLeftToMax#value", "vehicle.plow.rotateLeftToMax#value")
133: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.animTimeCenterPosition#value", "vehicle.plow.ai#centerPosition")
134: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.aiPlough#rotateEarly", "vehicle.plow.ai#rotateCompletelyHeadlandPos")
135: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.onlyActiveWhenLowered#value", "vehicle.plow.onlyActiveWhenLowered#value")

--------------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\PowerConsumer.lua
--------------------------------------------------------------------------------------------------
143: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, baseKey .. "#neededPtoPower", string.format("%s#neededMinPtoPower and %s#neededMaxPtoPower", baseKey, baseKey))

--------------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\PowerTakeOffs.lua
--------------------------------------------------------------------------------------------------
357: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, baseName .. "#linkNode", baseName .. "#outputNode")
358: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, baseName .. "#filename", "pto file is now defined in the pto input node")

--------------------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\RandomlyMovingParts.lua
--------------------------------------------------------------------------------------------------------
88: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#index", key .. "#node")

----------------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\ReceivingHopper.lua
----------------------------------------------------------------------------------------------------
46: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.receivingHopper#unloadingDelay", "Dischargeable functionalities")
47: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.receivingHopper#unloadInfoIndex", "Dischargeable functionalities")
48: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.receivingHopper#dischargeInfoIndex", "Dischargeable functionalities")
49: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.receivingHopper.tipTrigger#index", "Dischargeable functionalities")
50: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.receivingHopper.boxTrigger#index", "Dischargeable functionalities")
51: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.receivingHopper.fillScrollerNodes.fillScrollerNode", "Dischargeable functionalities")
52: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.receivingHopper.fillEffect", "Dischargeable functionalities")
53: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.receivingHopper.fillEffect", "Dischargeable functionalities")
54: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.receivingHopper.boxTrigger#litersPerMinute", "Dischargeable functionalities")
55: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.receivingHopper.raycastNode#index", "Dischargeable functionalities")
56: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.receivingHopper.raycastNode#raycastLength", "Dischargeable functionalities")
57: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.receivingHopper.boxTrigger#boxSpawnPlaceIndex", "vehicle.receivingHopper.boxes#spawnPlaceNode")
58: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.receivingHopper.boxTrigger.box(0)", "vehicle.receivingHopper.boxes.box(0)")

---------------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\ReverseDriving.lua
---------------------------------------------------------------------------------------------------
96: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.reverseDriving.steering#reversedIndex", "vehicle.reverseDriving.steeringWheel#node")
97: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.reverseDriving.steering#reversedNode", "vehicle.reverseDriving.steeringWheel#node")

------------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\RidgeMarker.lua
------------------------------------------------------------------------------------------------
76: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.ridgeMarkers", "vehicle.ridgeMarker")
77: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.ridgeMarkers.ridgeMarker", "vehicle.ridgeMarker.marker")
78: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.ridgeMarker.ridgeMarker", "vehicle.ridgeMarker.marker")
310: 		XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. ".testArea#startNode", key .. ".ridgeMarkerArea#node")
311: 		XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. ".testArea#widthNode", key .. ".ridgeMarkerArea#node")
312: 		XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. ".testArea#heightNode", key .. ".ridgeMarkerArea#node")

-------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\Roller.lua
-------------------------------------------------------------------------------------------
70: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.rollerSound", "vehicle.roller.sounds.work")
71: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.onlyActiveWhenLowered#value", "vehicle.roller#onlyActiveWhenLowered")

------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\Ropes.lua
------------------------------------------------------------------------------------------
130: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#index", key .. "#node")

-------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\Shovel.lua
-------------------------------------------------------------------------------------------
73: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.shovel#pickUpNode", "vehicle.shovel.shovelNode#node")
74: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.shovel#pickUpWidth", "vehicle.shovel.shovelNode#width")
75: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.shovel#pickUpLength", "vehicle.shovel.shovelNode#length")
76: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.shovel#pickUpYOffset")
77: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.shovel#pickUpRequiresMovement", "vehicle.shovel.shovelNode#needsMovement")
78: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.shovel#pickUpNeedsToBeTurnedOn", "vehicle.shovel.shovelNode#needsActivation")

--------------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\SowingMachine.lua
--------------------------------------------------------------------------------------------------
111: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.turnedOnRotationNodes.turnedOnRotationNode#type", "vehicle.sowingMachine.animationNodes.animationNode", "sowingMachine")
112: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.turnedOnScrollers", "vehicle.sowingMachine.scrollerNodes.scrollerNode")
113: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.useDirectPlanting", "vehicle.sowingMachine.useDirectPlanting#value")
114: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.needsActivation#value", "vehicle.sowingMachine.needsActivation#value")
115: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.sowingEffects", "vehicle.sowingMachine.effects")
116: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.sowingEffectsWithFixedFillType", "vehicle.sowingMachine.fixedEffects")
117: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.sowingMachine#supportsAiWithoutSowingMachine", "vehicle.turnOnVehicle.aiRequiresTurnOn")
118: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.sowingMachine.directionNode#index", "vehicle.sowingMachine.directionNode#node")

-------------------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\SpeedRotatingParts.lua
-------------------------------------------------------------------------------------------------------
71: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.speedRotatingParts.speedRotatingPart(0)#index", "vehicle.speedRotatingParts.speedRotatingPart(0)#node")

--------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\Sprayer.lua
--------------------------------------------------------------------------------------------
148: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.sprayParticles.emitterShape", "vehicle.sprayer.effects.effectNode#effectClass='ParticleEffect'")
149: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.sprayer#needsTankActivation")

------------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\StrawBlower.lua
------------------------------------------------------------------------------------------------
45: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.strawBlower.baleTrigger#index", "vehicle.strawBlower.baleTrigger#node")
46: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.strawBlower.doorAnimation#name", "vehicle.foldable.foldingParts.foldingPart.animationName")

------------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\StumpCutter.lua
------------------------------------------------------------------------------------------------
58: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.turnedOnRotationNodes.turnedOnRotationNode", "vehicle.stumpCutter.animationNodes.animationNode", "stumbCutter")
59: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.stumpCutterStartSound", "vehicle.stumpCutter.sounds.start")
60: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.stumpCutterIdleSound", "vehicle.stumpCutter.sounds.idle")
61: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.stumpCutterWorkSound", "vehicle.stumpCutter.sounds.work")
62: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.stumpCutterStopSound", "vehicle.stumpCutter.sounds.stop")
63: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.stumpCutter.emitterShape(0)", "vehicle.stumpCutter.effects.effectNode")
64: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.stumpCutter.particleSystem(0)", "vehicle.stumpCutter.effects.effectNode")
65: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.stumpCutter#cutNode", "vehicle.stumpCutter.cutNode#node")
66: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.stumpCutter#cutSizeY", "vehicle.stumpCutter.cutNode#cutSizeY")
67: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.stumpCutter#cutSizeZ", "vehicle.stumpCutter.cutNode#cutSizeZ")
68: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.stumpCutter#cutFullTreeThreshold", "vehicle.stumpCutter.cutNode#cutFullTreeThreshold")
69: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.stumpCutter#cutPartThreshold", "vehicle.stumpCutter.cutNode#cutPartThreshold")

-------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\Tedder.lua
-------------------------------------------------------------------------------------------
53: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.turnedOnRotationNodes.turnedOnRotationNode#type", "vehicle.tedder.animationNodes.animationNode", "tedder")
54: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.tedder.sounds", "vehicle.turnOnVehicle.sounds.work")

------------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\TipOccluder.lua
------------------------------------------------------------------------------------------------
34: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.tipOcclusionAreas.tipOcclusionArea", "vehicle.tipOccluder.occlusionArea")

--------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\Trailer.lua
--------------------------------------------------------------------------------------------
127: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.tipScrollerNodes.tipScrollerNode", "vehicle.trailer.trailerConfigurations.trailerConfiguration.trailer.tipSide.animationNodes.animationNode")
128: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.tipRotationNodes.tipRotationNode", "vehicle.trailer.trailerConfigurations.trailerConfiguration.trailer.tipSide.animationNodes.animationNode")
129: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.tipAnimations.tipAnimation", "vehicle.trailer.trailerConfigurations.trailerConfiguration.trailer.tipSide")

------------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\TreePlanter.lua
------------------------------------------------------------------------------------------------
95: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.treePlanterSound", "vehicle.treePlanter.sounds.work")
96: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.turnedOnRotationNodes.turnedOnRotationNode(0)", "vehicle.treePlanter.animationNodes.animationNode")

--------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\TreeSaw.lua
--------------------------------------------------------------------------------------------
36: 		XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.turnedOnRotationNodes.turnedOnRotationNode", "vehicle.treeSaw.animationNodes.animationNode", "stumbCutter")
37: 		XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.treeSaw.cutParticleSystems.emitterShape(0)", "vehicle.treeSaw.effects.effectNode")
38: 		XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.treeSaw.sawSound", "vehicle.treeSaw.sounds.saw")
39: 		XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.treeSaw.cutSound", "vehicle.treeSaw.sounds.cut")

--------------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\TurnOnVehicle.lua
--------------------------------------------------------------------------------------------------
114: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.turnOnSettings#turnOffText", "vehicle.turnOnVehicle#turnOffText")
115: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.turnOnSettings#turnOnText", "vehicle.turnOnVehicle#turnOnText")
116: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.turnOnSettings#needsSelection")
117: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.turnOnSettings#isAlwaysTurnedOn", "vehicle.turnOnVehicle#isAlwaysTurnedOn")
118: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.turnOnSettings#toggleButton", "vehicle.turnOnVehicle#toggleButton")
119: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.turnOnSettings#animationName", "vehicle.turnOnVehicle.turnedAnimation#name")
120: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.turnOnSettings#turnOnSpeedScale", "vehicle.turnOnVehicle.turnedAnimation#turnOnSpeedScale")
121: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.turnOnSettings#turnOffSpeedScale", "vehicle.turnOnVehicle.turnedAnimation#turnOffSpeedScale")
122: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.turnedOnRotationNodes.turnedOnRotationNode#type", "vehicle.turnOnVehicle.animationNodes.animationNode", "turnOn")
123: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.foldable.foldingParts#turnOffOnFold", "vehicle.turnOnVehicle#turnOffIfNotAllowed")

-------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\Wheels.lua
-------------------------------------------------------------------------------------------
461: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.driveGroundParticleSystems", "vehicle.wheels.wheelConfigurations.wheelConfiguration.wheels.wheel#hasParticles")
462: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.wheelConfigurations.wheelConfiguration", "vehicle.wheels.wheelConfigurations.wheelConfiguration")
463: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.rimColor", "vehicle.wheels.rimColor")
464: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.hubColor", "vehicle.wheels.hubs.color0")
465: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.dynamicallyLoadedWheels", "vehicle.wheels.dynamicallyLoadedWheels")
466: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.ackermannSteeringConfigurations", "vehicle.wheels.ackermannSteeringConfigurations")
467: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.wheels.wheel", "vehicle.wheels.wheelConfigurations.wheelConfiguration.wheels.wheel")
468: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.wheels.wheel#repr", "vehicle.wheels.wheelConfigurations.wheelConfiguration.wheels.wheel.physics#repr")
469: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.wheelConfigurations.wheelConfiguration.wheels.wheel#repr", "vehicle.wheels.wheelConfigurations.wheelConfiguration.wheels.wheel.physics#repr")
470: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.wheels.wheelConfigurations.wheelConfiguration.wheels.wheel#repr", "vehicle.wheels.wheelConfigurations.wheelConfiguration.wheels.wheel.physics#repr")
471: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.wheels.wheelConfigurations.wheelConfiguration.wheels.wheel#configIndex", "vehicle.wheels.wheelConfigurations.wheelConfiguration.wheels.wheel#configId")
472: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.ackermannSteering", "vehicle.wheels.ackermannSteeringConfigurations.ackermannSteering")
599: 		XMLUtil.checkDeprecatedXMLElements(self.xmlFile, baseName .. "#configIndex", baseName .. "#configId")
1232: 		XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. ".wheels.foliageBendingModifier", key .. ".foliageBendingModifier")
1270: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, string.format("vehicle.wheels.wheel(%d)#hasTyreTracks", wheel.xmlIndex), string.format("vehicle.wheels.wheelConfigurations.wheelConfiguration.wheels.wheel(%d)#hasTireTracks", wheel.xmlIndex))
1271: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, string.format("vehicle.wheels.wheel(%d)#tyreTrackAtlasIndex", wheel.xmlIndex), string.format("vehicle.wheels.wheelConfigurations.wheelConfiguration.wheels.wheel(%d)#tireTrackAtlasIndex", wheel.xmlIndex))
1272: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, string.format("vehicle.wheels.wheel(%d)#configIndex", wheel.xmlIndex), string.format("vehicle.wheels.wheelConfigurations.wheelConfiguration.wheels.wheel(%d)#configId", wheel.xmlIndex))
1628: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, configKey .. wheelKey .. "#steeringNode", string.format("vehicle.wheels.wheelConfigurations.wheelConfiguration.wheels.wheel(%d).steering#node", wheel.xmlIndex))
1681: 			XMLUtil.checkDeprecatedXMLElements(xmlFile, configKey .. additionalWheelKey .. "#configIndex", configKey .. additionalWheelKey .. "#configId")
1682: 			XMLUtil.checkDeprecatedXMLElements(xmlFile, configKey .. additionalWheelKey .. "#addRaycast", nil)
1725: 		XMLUtil.checkDeprecatedXMLElements(xmlFile, configKey .. wheelKey .. ".connector#index", configKey .. wheelKey .. ".connector#node")

----------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\Windrower.lua
----------------------------------------------------------------------------------------------
57: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.animation", "vehicle.windrowers.windrower")
58: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.windrowerParticleSystems", "vehicle.windrower.effects")
59: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.turnedOnRotationNodes.turnedOnRotationNode#type", "vehicle.windrower.animationNodes.animationNode", "windrower")
60: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.windrowerSound", "vehicle.windrower.sounds.work")
61: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.windrower.rakes.rake", "vehicle.windrower.animationNodes.animationNode with type 'RotationAnimationSpikes'")

------------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\WoodCrusher.lua
------------------------------------------------------------------------------------------------
211: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, xmlRoot .. ".woodCrusher.moveTrigger(0)#index", xmlRoot .. ".woodCrusher.moveTriggers.trigger#node")
212: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, xmlRoot .. ".woodCrusher.moveCollision(0)#index", xmlRoot .. ".woodCrusher.moveCollisions.collision#node")
213: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, xmlRoot .. ".woodCrusher.emitterShape(0)", xmlRoot .. ".woodCrusher.crushEffects with effectClass 'ParticleEffect'")
214: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, xmlRoot .. ".woodCrusherStartSound", xmlRoot .. ".woodCrusher.sounds.start")
215: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, xmlRoot .. ".woodCrusherIdleSound", xmlRoot .. ".woodCrusher.sounds.idle")
216: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, xmlRoot .. ".woodCrusherWorkSound", xmlRoot .. ".woodCrusher.sounds.work")
217: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, xmlRoot .. ".woodCrusherStopSound", xmlRoot .. ".woodCrusher.sounds.stop")
218: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, xmlRoot .. ".turnedOnRotationNodes.turnedOnRotationNode#type", xmlRoot .. ".woodCrusher.animationNodes.animationNode", "woodCrusher")
219: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, xmlRoot .. ".turnedOnScrollers.turnedOnScroller", xmlRoot .. ".woodCrusher.animationNodes.animationNode")
220: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, baseKey .. "#downForceNode", baseKey .. ".downForceNodes.downForceNode#node")
221: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, baseKey .. "#downForce", baseKey .. ".downForceNodes.downForceNode#force")
222: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, baseKey .. "#downForceSizeY", baseKey .. ".downForceNodes.downForceNode#sizeY")
223: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, baseKey .. "#downForceSizeZ", baseKey .. ".downForceNodes.downForceNode#sizeZ")

--------------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\WoodHarvester.lua
--------------------------------------------------------------------------------------------------
95: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.woodHarvester.delimbSound", "vehicle.woodHarvester.sounds.delimb")
96: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.woodHarvester.cutSound", "vehicle.woodHarvester.sounds.cut")
97: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.woodHarvester.treeSizeMeasure#index", "vehicle.woodHarvester.treeSizeMeasure#node")
98: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.woodHarvester.forwardingWheels.wheel(0)", "vehicle.woodHarvester.forwardingNodes.animationNode")
99: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.woodHarvester.cutParticleSystems", "vehicle.woodHarvester.cutEffects")
100: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.woodHarvester.delimbParticleSystems", "vehicle.woodHarvester.delimbEffects")

---------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\WorkArea.lua
---------------------------------------------------------------------------------------------
77: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.workAreas.workArea(0)#startIndex", "vehicle.workAreas.workArea(0).area#startIndex")
78: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.workAreas.workArea(0)#widthIndex", "vehicle.workAreas.workArea(0).area#widthIndex")
79: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.workAreas.workArea(0)#heightIndex", "vehicle.workAreas.workArea(0).area#heightIndex")
80: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.workAreas.workArea(0)#foldMinLimit", "vehicle.workAreas.workArea(0).folding#minLimit")
81: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.workAreas.workArea(0)#foldMaxLimit", "vehicle.workAreas.workArea(0).folding#maxLimit")
82: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.workAreas.workArea(0)#refNodeIndex", "vehicle.workAreas.workArea(0).groundReferenceNode#index")
314: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. ".area#startIndex", key .. ".area#startNode")
315: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. ".area#widthIndex", key .. ".area#widthNode")
316: 	XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. ".area#heightIndex", key .. ".area#heightNode")
348: 				XMLUtil.checkDeprecatedXMLElements(xmlFile, key .. "#refNodeIndex", key .. ".groundReferenceNode#index")

--------------------------------------------------------------------------------------------------
C:\Users\jtsag\Desktop\ModEdit\_decodedPatch1.5\scripts\vehicles\specializations\WorkParticles.lua
--------------------------------------------------------------------------------------------------
74: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.groundParticleAnimations.groundParticleAnimation", "vehicle.workParticles.particleAnimation")
75: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, "vehicle.groundParticleAnimations.groundParticle", "vehicle.workParticles.particle")
323: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. "#index", key .. "#node")
324: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. "#animMeshIndex", key .. "#animMeshNode")
457: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. "#index", key .. "#node")
458: 	XMLUtil.checkDeprecatedXMLElements(self.xmlFile, key .. "#particleIndex", key .. "#particleNode")


    """