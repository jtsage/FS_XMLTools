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


def enter_key_exit():
    """ Exit when enter key pressed """
    print("Press ENTER to close terminal.")
    try:
        input()
    except BaseException:
        pass
    exit()


print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
print("  logAnalyzer v1.0.2")
print("    by JTSModding")
print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")

parser = argparse.ArgumentParser(description='Grab the interesting bits of a log file')
parser.add_argument('file', metavar='file', nargs=1, type=argparse.FileType('r', encoding='utf-8'))

try:
    args = parser.parse_args()
except BaseException:
    enter_key_exit()

try:
    thisLogFile = args.file[0].read().split("\n")
    args.file[0].close()
except BaseException:
    print("ERROR: Unable to read / parse file '" + os.path.basename(args.file[0].name) + "'")
    enter_key_exit()

lineNo = 0
for line in thisLogFile:
    lineNo += 1
    if "Error:" in line or "Warning:" in line:
        print(str(lineNo) + " :: " + line)

if sys.stdout.isatty():
    # Don't pause on finish if we re-directed to a file.
    enter_key_exit()
