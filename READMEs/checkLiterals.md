# checkLiterals.py

This script checks the literal strings in your XML storeItem file to see if there are obvious entries that should be translated using the $l10n system.

## Usage

```shell
$ python checkLiterals.py --help

usage: checkLiterals.py [-h] files.xml [files.xml ...]

Check vehicle/placable xml(s) for untranslated strings.

positional arguments:
  files.xml

optional arguments:
  -h, --help  show this help message and exit
```

This script expects to see .xml files and will exit with an error if given something else.

## Sample Output

```text
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
  checkLiterals v1.0.2
    by JTSModding
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

Files Found: 1

Checking: lt699.xml...

  Possible missed translation in tag: name, current value is: LT699

File: lt699.xml HAS probable missing translations

done.
```

## LICENSE

This script is licensed under the MIT license, as such, you can do whatever you like to it, so long as attribution is given to the original author
