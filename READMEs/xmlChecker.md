# xmlChecker.py

This script checks your storeItem xml for broken file links, and against the XSD schema.  It also forces the $l10n strings to validate against a modified pattern for those entries (a super powered version of checkLiterals.py)

## Usage

```shell
$ python xmlChecker.py --help

usage: xmlChecker.py [-h] [--check-links | --no-check-links]
                     [--check-schema | --no-check-schema]
                     [--check-schema-l10n | --no-check-schema-l10n]
                     [--install-path INSTALLPATH]
                     files [files ...]

Sanity check an xml shopItem file.

positional arguments:
  files

optional arguments:
  -h, --help            show this help message and exit
  --check-links, --no-check-links
                        Check linked files for existence (default: True)
  --check-schema, --no-check-schema
                        Check XML against XSD Schema (default: True)
  --check-schema-l10n, --no-check-schema-l10n
                        Check XML against XSD Schema with $l10n type
                        restriction (default: True)
  --install-path INSTALLPATH
                        Installation path to FS data files (.../data/)
Press ENTER to close terminal.

```

This script expects to see .xml files and will exit with an error if given something else.

## Options

### --install-path

By default, the script will attempt to find your Farming Simulator 2022 files on it's own - if it is unable to, you can force your install path with this switch

### --check-links / --no-check-links

This switch enables checking linked files to make sure they exist and there is no path case mismatch

### --check-schema / --no-check-schema

This switch enables checking the document against the schema so long as LXML was detected

### --check-schema-l10n / --no-check-schema-l10n

This switch changes the schema on-the-fly to make checking of l10n capable entries to where they are required to start with `$l10n_`. You should expect some false positives from this.

## Sample Output

```text
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
  xmlChecker v1.0.2
    by JTSModding
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

Files Found: 1

Testing: 1870.xml
     in: C:\Users\jtsag\Desktop\ModEdit\__my_mods\FS_XMLTools\testFiles\FS19_1870
  PROCESSING: xml file is of type 'vehicle'
  PROCESSING: checking file links
    NOTICE: no missing linked file(s) detected.
  PROCESSING: Checking against XSD Schema
    NOTICE: Validation failed:
    Line 10: Element 'combination': Character content is not allowed, because the content type is empty.
    Line 58: Element 'designConfiguration', attribute 'name': [facet 'pattern'] The value '1' is not accepted by the pattern '$l10n_.+'.
    Line 342: Element 'objectChange', attribute 'visibilityInActive': The attribute 'visibilityInActive' is not allowed.
    Line 673: Element 'foldingParts': This element is not expected.
    Line 1197: Element 'fillUnit', attribute 'unit': The attribute 'unit' is not allowed.
    Line 1381: Element 'turnOnVehicle': This element is not expected.

done.
```

## LICENSE

This script is licensed under the MIT license, as such, you can do whatever you like to it, so long as attribution is given to the original author
