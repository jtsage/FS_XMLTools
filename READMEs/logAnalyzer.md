# logAnalyzer.py

This is a *very* simple log parser that tries to pull out the important bits for easy viewing.

## Usage

```shell
$ python logAnalyzer.py --help

usage: logAnalyzer.py [-h] [-d [version]] [--startup | --no-startup] [file]

Grab the interesting bits of a log file. Defaults to the log file from your
FS2022 install

positional arguments:
  file

optional arguments:
  -h, --help            show this help message and exit
  -d [version], --detect [version]
                        Detect log file from Farming Simulator [version]
  --startup, --no-startup
                        Show startup errors (default: True)


```

## Options

With the `-d` / `--detect` option, you can specify the Farming Simulator log file to look for.  Version can be either 4 digit `2022` or 2 digit `22`

With `--no-startup`, suppress printing the errors before the first timestamp.  In practice, this is problems with mods not loading, or unzipped, or missing translations.

## LICENSE

This script is licensed under the MIT license, as such, you can do whatever you like to it, so long as attribution is given to the original author
