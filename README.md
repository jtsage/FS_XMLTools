# Farming Simulator XML Tools

This contains some quick python tools to make some aspects of modding a little easier

## Installation

To install just download the python script you want (or all of them).

If for some reason drag-and-drop to the python script doesn't work, make sure you have python files set to open with the python interpreter, if that doesn't work, repair your installation / re-install

### Note About Python

Your life will be much better, and the use of these is far easier if you __DO__ check the box to add python to your `$PATH` environmental variable when you are installing it.  If you did not do this, you can re-install python, or 'modify' your installation from Add/Remove programs.  Be warned, this is one of the times that an installer tells you to reboot that you actually have to do it.

### LXML Requirement (xmlChecker only)

Sadly, the native ETree implementation in python cannot do schema validation, so you will need to install `lxml` - the simplest method of this is to open a `cmd` or `Windows Terminal` __with administrator privileges__ and run:

```shell
$ pip install lxml
```

Note from the initial warning above, python must be installed __with__ the option to add it to your `$PATH` environmental variable.

---

## checkLiterals.py

This script checks the literal strings in your XML storeItem file to see if there are obvious entries that should be translated using the $l10n system.

[checkLiterals documentation](READMEs/checkLiterals.md)

---

## comparei3dMappings.py

This script is for use with multiple storeItem xml files that share an I3D file.  It will compare the `<i3dMappings>` section of each and let you know what, if any, differences it finds. If you are using a shared I3D between multiple storeItems, this can help keep any changes in sync.

[comparei3dMappings documentation](READMEs/comparei3dMappings.md)

---

## compareTranslations.py

This script compares two or more translation files to make sure the same keys appear in all files, so you do not have un-translated text in one language.

[compareTranslations documentation](READMEs/compareTranslations.md)

---

## i3dChecker.py

This script checks an i3d file and outputs problems it finds with linked files, linked lights, unusual or unknown rigid body collisions, and visible shapes that are missing shadow maps.  It also outputs realLight information in an easy to read format.

[i3dChecker documentation](READMEs/i3dChecker.md)

---

## i3dMapper.py

This script generates i3d Mapping for your XML file, *from* your I3D file.  It does it's best to avoid name collisions.

[i3dMapper documentation](READMEs/i3dMapper.md)

### Variants

#### i3dMapper_toClipboard.bat

This is a simple batch file that dumps the output of the mapper to the windows clipboard.  Takes the I3D file.

#### i3dMapper_toXML.py

This is a wrapper that takes your storeItem XML and writes the new i3dMapping directly to the supplied file.  Please note that due to ETree limitations, this *will* remove any comments in the XML file.

#### i3dMapper_replacer.py

This is a wrapper that takes your storeItem XML and write the new i3dMapping directly to the supplied file.  This will *also* attempt to re-write any numeric nodes in the existing file into the new name mapping.  Please note, that like the _toXML variant, this also *will* remove any comments in the file.

---

## logAnalyzer.py

This is a *very* simple log parser that tries to pull out the important bits for easy viewing.

[logAnalyzer documentation](READMEs/logAnalyzer.md)

---

## modDescChecker.py

This script checks for common problems in your modDesc.xml file.

[modDescChecker documentation](READMEs/modDescChecker.md)

---

## xmlChecker.py

This script checks your storeItem xml for broken file links, and against the XSD schema.  It also forces the $l10n strings to validate against a modified pattern for those entries (a super powered version of checkLiterals.py)

[xmlChecker documentation](READMEs/xmlChecker.md)
