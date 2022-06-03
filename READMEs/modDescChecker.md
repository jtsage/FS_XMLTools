# modDescChecker.py

This script checks for common problems in your modDesc.xml file.

## Usage

```shell
$ python modDescChecker.py --help

usage: modDescChecker.py [-h] file

Sanity check an xml shopItem file.

positional arguments:
  file

optional arguments:
  -h, --help  show this help message and exit
Press ENTER to close terminal.

```

This script expects to see a modDesc.xml files and will exit with an error if given something else.

## Sample Output

```text
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
  modDescChecker v1.0.2
    by JTSModding
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

CHECKING: .\FS22_25DU_Trailers\modDesc.xml
  SUCCESS :: TEST: descVersion is 66 or greater?
  SUCCESS :: TEST: Title L10N contains at least ['en', 'de']?
  SUCCESS :: TEST: Title ['en', 'de'] are not identical?
  SUCCESS :: TEST: Description L10N contains at least ['en', 'de']?
  SUCCESS :: TEST: Description ['en', 'de'] are not identical?
  SUCCESS :: TEST: iconFilename is 'modIcon.dds'?
  SUCCESS :: TEST: version 1.0.0.0+ contains changelog?

done.
```

The "TEST:" bit is the question being asked.  SUCCESS indicates everything is fine, FAIL indicates a problem - e.g. `FAIL :: TEST: Title L10N contains at least ['en', 'de']?` would mean that your `<title>` tag __does not__ contain at least those elements.

## LICENSE

This script is licensed under the MIT license, as such, you can do whatever you like to it, so long as attribution is given to the original author
