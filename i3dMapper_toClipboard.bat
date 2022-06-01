@echo off
cd /D "%~dp0"
python.exe ./i3dMapper.py %* | clip
echo Mappings are now on your clipboard!
pause