# i3dMapper.py

This script generates i3d Mapping for your XML file.  It does it's best to avoid name collisions.

## Variants

### i3dMapper_toClipboard.bat

This is a simple batch file that dumps the output of the mapper to the windows clipboard

### i3dMapper_toXML.py

This is a wrapper that takes your storeItem XML and writes the new i3dMapping directly to the supplied file.  Please note that due to ETree limitations, this *will* remove any comments in the XML file.

### i3dMapper_replacer.py

This is a wrapper that takes your storeItem XML and write the new i3dMapping directly to the supplied file.  This will *also* attempt to re-write any numeric nodes in the existing file into the new name mapping.  Please note, that like the _toXML variant, this also *will* remove any comments in the file.

## Usage

```shell
$ python i3dMapper.py --help

usage: i3dMapper.py [-h] [--pretty-print | --no-pretty-print] file

Export i3d Mapping

positional arguments:
  file

optional arguments:
  -h, --help            show this help message and exit
  --pretty-print, --no-pretty-print
                        Pretty print output (default: True)
```

The mapper and all variants can only take a single file at a time.

## Options

### --pretty-print / --no-pretty-print

When enabled, the output is pretty printed so that all of the `id` and `node` tags line up.

## Sample Output

```xml
<i3dMappings>
  <i3dMapping id="mrplow_component1"          node="0>" />
  <i3dMapping id="mrplow_vis"                 node="0>0" />
  <i3dMapping id="ai"                         node="0>0|0" />
  <!-- ... -->
</i3dMappings>
```
