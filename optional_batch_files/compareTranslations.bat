@echo off
cd /D "%~dp0"
python.exe ./compareTranslations.py %*
