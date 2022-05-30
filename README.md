# Farming Simulator XML Tools

This contains some quick python tools to make some aspects of modding a little easier

---

## compareTranslations.py

This will compare two (or more) translation files to each other, and tell you if there are translated entities that do not appear in all files.

__Usage:__

```shell
$ python .\compareTranslations.py --folder ./testFiles/translations

$ python .\compareTranslations.py .\testFiles\translations\translation_en.xml .\testFiles\translations\translation_de.xml
```

### Translation file format
By default, compareTranslations.py expects a file of the format:

```xml
<l10n>
  <translationContributors>JTSage</translationContributors>

  <texts>
    <text name="title_simpleInspector" text="Simple Inspector" />
  </texts>
</l10n>
```

If you have a file that uses the other format, you can use the `--giants_ekv` command line argument

```xml
<l10n><elements>
  <e k="some_tag" v="Some Translated Text" tag="0"/>
</elements></l10n>
```

### Sample Output

```text
Files Found: 2
Mismatch Found:
  Text Name : input_SimpleInspector_reload_config
   Found In      : ['translation_en.xml']
   Not Found In  : ['translation_de.xml']

There are mismatched translations
```

---

## comparei3dMappings.py

This will compare the `<i3dMappings>` section in your vehicle / implement / placable XML files and tell you what is different.  Useful when using the same I3D file for multiple store items.

__Usage:__

```shell
$ python .\comparei3dMappings.py .\testFiles\i3dMap\mrplow_light_5.xml .\testFiles\i3dMap\mrplow_heavy_5.xml
```

Requires at least 2 files.

### Sample Output

```text
Files Found: 4
Mismatch Found (different):
  ID Name : mrplow_vis
   Mappings : [{'mrplow_heavy_3.xml': '0>40'}, {'mrplow_heavy_5.xml': '0>0'}, {'mrplow_light_3.xml': '0>0'}, {'mrplow_light_5.xml': '0>0'}]
Mismatch Found (missing):
  Text Name : mrplow_component5
   Found In      : ['mrplow_heavy_5.xml', 'mrplow_light_5.xml']
   Not Found In  : ['mrplow_heavy_3.xml', 'mrplow_light_3.xml']

There are mismatched I3D Mappings
```

---

## i3dMapper.py

This is just an i3d mapper, built to be fast in python

__Usage:__

```shell
$ python .\i3dMapper.py .\testFiles\i3d\mrplow.i3d
```
__Options:__

* `--no_pretty_print` Do not line up the "node" entries on output.  Pretty print is on by default.

### Sample Output

```xml
<i3dMappings>
  <i3dMapping id="mrplow_component1"          node="0>" />
  <i3dMapping id="mrplow_vis"                 node="0>0" />
  <i3dMapping id="ai"                         node="0>0|0" />
</i3dMappings>
```
