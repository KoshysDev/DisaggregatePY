#!/bin/bash
# This shell script compiles main.py using PyInstaller

pyinstaller --onefile --noconsole --add-data "azure.tcl:." --add-data "theme:theme" --add-data "config.py:." GUI_DIS.py

read -p "Press Enter to continue..."
