# comparei3dMappings.py

This script is for use with multiple storeItem xml files that share an I3D file.  It will compare the `<i3dMappings>` section of each and let you know what, if any, differences it finds. If you are using a shared I3D between multiple storeItems, this can help keep any changes in sync.

## Usage

```shell
$ python comparei3dMappings.py --help

usage: comparei3dMappings.py [-h] file.xml file.xml [file.xml ...]

Compare i3d Mapping in xml files.

positional arguments:
  file

optional arguments:
  -h, --help  show this help message and exit
```

This script requires at least two XML files to function.

## Sample Output

```text
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
  comparei3dMappings v1.0.2
    by JTSModding
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

Files Found: 2

Mismatch(es) Found (missing):

  Text Name : mrplow_component5
   Found In      : ['mrplow_light_5.xml']
   Not Found In  : ['mrplow_light_3.xml']
   
  ...

  Text Name : rowOutsideWheel_phy
   Found In      : ['mrplow_light_5.xml']
   Not Found In  : ['mrplow_light_3.xml']

Mismatch(es) Found (different):

  ID Name : liWingHinge
   Mappings : [{'mrplow_light_3.xml': '0>0|11|5|6'}, {'mrplow_light_5.xml': '0>0|11|5|2'}]

There are mismatched I3D Mappings
```

## LICENSE

This script is licensed under the MIT license, as such, you can do whatever you like to it, so long as attribution is given to the original author
