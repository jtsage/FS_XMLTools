"""
  _____ _______ _______ _______  _____  ______  ______  _____ __   _  ______
    |      |    |______ |  |  | |     | |     \ |     \   |   | \  | |  ____
  __|      |    ______| |  |  | |_____| |_____/ |_____/ __|__ |  \_| |_____|
    checkLiterals.py

Version History:
 v0.0.9 - Initial Release
"""
import argparse
import os
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description='Compare i3d Mapping in xml files.')

parser.add_argument('files', metavar='files', nargs="*", type=argparse.FileType('r', encoding='utf-8'))
args = parser.parse_args()


file_list = args.files

def print_bad(tag, value):
	print("Possible missed translation in tag: " + tag + ", current value is: " + value)

attrib_to_check = {
	"abortUnloading",
	"activateText",
	"baleDoNotAllowFillTypeMixing",
	"baleNotSupported",
	"changeText",
	"clutchCrackingGearWarning",
	"clutchCrackingGroupWarning",
	"clutchNoEngagedWarning",
	"consumersEmptyWarning",
	"consumersEmptyWarning",
	"deactivateText",
	"detachWarning",
	"disableText",
	"enableText",
	"infoText",
	"lowering",
	"lowerPlattform",
	"middleNegDirectionText",
	"middlePosDirectionText",
	"minUnloadingFillLevelWarning",
	"negDirectionText",
	"noCutter",
	"objectText",
	"onlyOneBaleTypeWarning",
	"operatingPosition",
	"posDirectionText",
	"textNeg",
	"textPos",
	"tilting",
	"title",
	"transportPosition",
	"turnOffText",
	"turnOnNotAllowedWarning",
	"turnOnStateWarning",
	"turnOnText",
	"typeDesc",
	"unfoldWarning",
	"unload",
	"unloadBaleText",
	"unloadHere",
}
name_to_check = {
	"attacherJointConfiguration",
	"baseMaterialConfiguration",
	"configurationSet",
	"controlGroup",
	"coverConfiguration",
	"design8Configuration",
	"design7Configuration",
	"design6Configuration",
	"design5Configuration",
	"design4Configuration",
	"design3Configuration",
	"design2Configuration",
	"designConfiguration",
	"designMaterialConfiguration",
	"designMaterial2Configuration",
	"designMaterial3Configuration",
	"dischargeableConfiguration",
	"fillUnitConfiguration",
	"fillVolumeConfiguration",
	"foldingConfiguration",
	"frontloaderConfiguration",
	"inputAttacherJointConfiguration",
	"motorConfiguration",
	"pipeConfiguration",
	"powerConsumerConfiguration",
	"rimColorConfiguration",
	"steeringMode",
	"tipSide",
	"trailerConfiguration",
	"transmission",
	"variableWorkWidthConfiguration",
	"vehicleTypeConfiguration",
	"wheelConfiguration",
	"workAreaConfiguration",
	"workMode",
	"wrappingAnimationConfiguration",
	"wrappingColorConfiguration",
}
text_to_check = {
	"function",
	"typeDesc",
	"name",
}

print("Files Found: " +  str(len(file_list)))



fileCount     = 0
fileListShort = []
nameList      = {}
for file in file_list:
	cleanFile  = True
	thisName   = os.path.basename(file.name)
	thisXML    = ET.fromstring(file.read())

	for attrib_name in attrib_to_check :
		for texts in thisXML.findall(".//*[@" + attrib_name + "]") :
			if not texts.attrib[attrib_name].startswith('$l10n') :
				cleanFile = False
				print_bad(texts.tag, texts.attrib[attrib_name])
		
	for text_name in text_to_check :
		for texts in thisXML.findall(".//" + text_name) :
			if not texts.text.startswith('$l10n'):
				cleanFile = False
				print_bad(texts.tag, texts.text)

	for name_text in name_to_check :
		for texts in thisXML.findall(".//" + name_text) :
			if "name" in texts.attrib :
				if not texts.attrib["name"].startswith('$l10n') :
					cleanFile = False
					print_bad(texts.tag, texts.attrib["name"])
		
	if cleanFile :
		print("File: " + thisName + " had no detected missing translations\n")
	else :
		print("\nFile: " + thisName + " HAS detected missing translations\n")

print("done.")