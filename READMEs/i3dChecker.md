# i3dChecker.py

This script checks an i3d file and outputs problems it finds with linked files, linked lights, unusual or unknown rigid body collisions, and visible shapes that are missing shadow maps.  It also outputs realLight information in an easy to read format.

## Usage

```shell
$ python i3dChecker.py --help

usage: i3dChecker.py [-h] [--shadows | --no-shadows]
                     [--link-check | --no-link-check]
                     [--light-check | --no-light-check]
                     [--light-info | --no-light-info]
                     [--collisions | --no-collisions]
                     [--install-path INSTALLPATH]
                     files [files ...]

Sanity check an i3d file.

positional arguments:
  files

optional arguments:
  -h, --help            show this help message and exit
  --shadows, --no-shadows
                        Check for shadow maps on visible shapes (default:
                        True)
  --link-check, --no-link-check
                        Check that linked files exist (default: True)
  --light-check, --no-light-check
                        Check linked lights (default: True)
  --light-info, --no-light-info
                        Output realLight attributes (default: True)
  --collisions, --no-collisions
                        Check for unusual or unknown collision masks (default:
                        True)
  --install-path INSTALLPATH
                        Installation path to FS data files (.../data/)
```

This script expects to see .i3d files and will exit with an error if given something else.

## Options

### --install-path

By default, the script will attempt to find your Farming Simulator 2022 files on it's own - if it is unable to, you can force your install path with this switch

### --shadows / --no-shadows

This switch is for checking all visible (renderable) shapes for the presence of `receivesShadows` and `castsShadows`

### --link-check / --no-link-check

This switch is for checking of linked files in the I3D to make sure they exist.

### --light-check / --no-light-check

This switch is for explicitly checking linked lights against the "OLD" names, and suggesting the change.

### --light-info / --no-light-info

This switch is for outputting all of the real light information in the I3D file.

### --collisions / --no-collisions

This switch is for checking collisions against a list of known common and known uncommon bit masks.  It also will produce an error if you are using any of the depreciated bits.

## Sample Output

### --shadows

```text
hasShadowMap | castsShadowMap on renderable shapes:
  Node Name: cw_crumble_hanger
   Casts Shadow Map: no | Receives Shadow Map: no
  Node Name: decalAmazone_02
   Casts Shadow Map: no | Receives Shadow Map: yes
```

### --link-check

```text
Check path of linked files:
  FILE NOT FOUND: $data/shared/assets/assetLibraryDecals_specular.dds
  FILE NOT FOUND: $data/vehicles/seedHawk/980AirCart/980AirCartTubes_normal.dds
  FILE NOT FOUND: $data/vehicles/seedHawk/980AirCart/980AirCartTubes_specular.dds
```

### --light-check

```text
Links to old lights in i3d:
  Linked Light with fileId '5' is 'rearLightOvalWhite_01', should be 'rearLight26White'
```

### --light-info

```text
RealLights Information:
  Node Name: frontLightLow
   Type: spot, Color: #D8D8FF, Shadows: no, Range: 20 m, Cone Angle: 80 °, Drop Off: 3 m
```

### --collisions

```text
Unknown, uncommon, or depreciated collisionMasks:
  collisionMask for 'torion1914_main_component1' (1075851266)/(0x40203002) is unknown, and should be checked
```

```text
Unknown, uncommon, or depreciated collisionMasks:
  collisionMask for 'mixerWagonHUDTrigger' (3170304)/(0x306000) is unusual, but does exist in some giants files
```

```text
Unknown, uncommon, or depreciated collisionMasks:
  collisionMask for 'torion1914_main_component1' (6303746)/(0x603002) uses depreciated bits and needs corrected
```

## LICENSE

This script is licensed under the MIT license, as such, you can do whatever you like to it, so long as attribution is given to the original author
