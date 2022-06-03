# compareTranslations.py

This script compares two or more translation files to make sure the same keys appear in all files, so you do not have un-translated text in one language.

## Usage

```shell
$ python compareTranslations.py --help

usage: compareTranslations.py [-h] [--folder FOLDER] [--giants_ekv]
                              [files ...]

Compare translation files.

positional arguments:
  files

optional arguments:
  -h, --help       show this help message and exit
  --folder FOLDER  Process a folder rather than a list of files.
  --giants_ekv     Use Giants <e k= v=> mode
Press ENTER to close terminal.

```

This script expects to see at least two .xml files and will exit with an error if given something else.

## Options

### --folder

Scan the entire given folder instead of using file.  When present, and file arguments on the command line are ignored.

### --giants_ekv

Turns on e/k/v mode.

By default, the script expects localization files in the format of:

```xml
<l10n>
  <texts>
    <text name="translation_key" text="Translated Text" />
  </texts>
</l10n>
```

However, some Giants files, and some mod authors prefer the e/k/v format:

```xml
<l10n>
  <elements>
    <e k="translation_key" v="Translated Text" />
  </elements>
</l10n>
```

## Sample Output

```text
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
  compareTranslations v1.0.2
    by JTSModding
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

Files Found: 2
WARNING: 'translation_en.xml' contains a duplicate entry for 'input_SimpleInspector_reload_config'

Mismatch(es) Found:

  Text Name : input_SimpleInspector_reload_config
   Found In      : ['translation_en.xml']
   Not Found In  : ['translation_de.xml']

  Text Name : input_SimpleInspector_toggle_visible
   Found In      : ['translation_en.xml']
   Not Found In  : ['translation_de.xml']

  Text Name : input_SimpleInspector_toggle_allfarms
   Found In      : ['translation_en.xml']
   Not Found In  : ['translation_de.xml']

There are mismatched translations
```

## LICENSE

This script is licensed under the MIT license, as such, you can do whatever you like to it, so long as attribution is given to the original author
