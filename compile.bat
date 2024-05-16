@echo off
REM This batch file compiles main.py using PyInstaller

pyinstaller --onefile --noconsole --add-data "azure.tcl;." --add-data "theme;theme" --add-data "config.py;." main.py

pause
