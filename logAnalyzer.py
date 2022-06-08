# pylama:ignore=W605,E221,C901
"""
        __ ______     __     _   _
        /    /      /    )   /  /|              /       /   ,
-------/----/-------\-------/| /-|----__----__-/----__-/--------__----__-
      /    /         \     / |/  |  /   ) /   /   /   /   /   /   ) /   )
_(___/____/______(____/___/__/___|_(___/_(___/___(___/___/___/___/_(___/_
                                                                      /
    logAnalyzer.py - v1.0.2                                       (_ /

Version History:
 v1.0.2 - Initial Release
"""

import argparse
import os
import sys
import re
import hashlib
import pprint


def enter_key_exit():
    """ Exit when enter key pressed """
    print("Press ENTER to close terminal.")
    try:
        input()
    except BaseException:
        pass
    exit()


def hashedError(thisLine):
    dateFreeText = re.sub("^\d\d\d\d-\d\d-\d\d \d\d:\d\d ", "", thisLine["lineText"])
    contextLines = "".join(thisLine["context"])
    return(
        hashlib.md5(dateFreeText.encode('utf-8')).hexdigest() +
        hashlib.md5(contextLines.encode('utf-8')).hexdigest()
    )


print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
print("  logAnalyzer v1.0.2")
print("    by JTSModding")
print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")

parser = argparse.ArgumentParser(
    description='Grab the interesting bits of a log file. ' +
    'Defaults to the log file from your FS2022 install'
)
parser.add_argument(
    'file',
    metavar='file',
    nargs='?',
    type=argparse.FileType('r', encoding='utf-8')
)
parser.add_argument(
    '-d', '--detect',
    help='Detect log file from Farming Simulator [version]',
    metavar='version',
    nargs='?'
)
parser.add_argument(
    '--startup',
    help="Show startup errors",
    action=argparse.BooleanOptionalAction,
    default=True
)

try:
    args = parser.parse_args()
except BaseException:
    enter_key_exit()

currentFile = None

if args.file is None:
    thisVersion = "2022"
    if args.detect is not None:
        if len(args.detect) == 4:
            thisVersion = str(args.detect)
        if len(args.detect) == 2:
            thisVersion = "20" + str(args.detect)

    print("Auto-Reading FarmingSimulator{0}\n".format(thisVersion))
    try:
        currentFile = open(
            "{0}\Documents\My Games\FarmingSimulator{1}\log.txt".format(
                os.getenv("USERPROFILE"),
                thisVersion
            ),
            "r"
        )
    except BaseException:
        print("ERROR: Unable to read log for version '" + thisVersion + "'")
        enter_key_exit()
else:
    currentFile = args.file


try:
    thisLogFile = currentFile.read().split("\n")
    currentFile.close()
except BaseException:
    print("ERROR: Unable to read / parse file '" + os.path.basename(currentFile.name) + "'")
    enter_key_exit()

runtimeChunks  = []
startupErrors  = []
runtimeErrors  = []
errorsFound    = 0
runtimeStarted = False

if thisLogFile[0].startswith("GIANTS Engine Runtime"):
    for lineNum, line in enumerate(thisLogFile, start=1):
        if line:
            if line[0].isdigit():
                runtimeStarted = True
                runtimeChunks.append({
                    "lineNum": lineNum,
                    "lineText": line,
                    "context": []
                })
            else:
                if not runtimeStarted:
                    if "Error:" in line or "Warning:" in line or "ERROR" in line:
                        startupErrors.append({
                            "lineNum": lineNum,
                            "lineText": line
                        })
                else:
                    runtimeChunks[len(runtimeChunks) - 1]["context"].append(line)

    if args.startup:
        print("Startup Errors:\n")
        for thisLine in startupErrors:
            errorsFound += 1
            print("{0} : {1}".format(
                thisLine["lineNum"],
                thisLine["lineText"]
            ))

    pp = pprint.PrettyPrinter(indent=4, width=120)

    ERROR_STRINGS = [
        "Error",
        "Warning",
        "call stack"
    ]

    for thisLine in runtimeChunks:
        for thisErr in ERROR_STRINGS:
            if thisErr in thisLine["lineText"]:
                thisHash = hashedError(thisLine)
                if thisHash not in runtimeErrors:
                    runtimeErrors.append(thisHash)
                    errorsFound += 1
                    print("{0} : {1}".format(
                        thisLine["lineNum"],
                        thisLine["lineText"]
                    ))
                    for thisContext in thisLine["context"]:
                        print("  {0}".format(thisContext))

    print("\nErrors Found: {0}".format(errorsFound))

else:
    for lineNum, line in enumerate(thisLogFile, start=1):
        if "Error:" in line or "Warning:" in line or "ERROR" in line:
            print(str(lineNum) + " :: " + line)

if sys.stdout.isatty():
    # Don't pause on finish if we re-directed to a file.
    enter_key_exit()
