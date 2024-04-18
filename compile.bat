@echo off
REM This batch file compiles GUI_DIS.py using PyInstaller

pyinstaller --onefile --noconsole --add-data "azure.tcl;." --add-data "theme;theme" GUI_DIS.py

pause
