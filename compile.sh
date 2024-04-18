#!/bin/bash
pyinstaller --onefile --noconsole --add-data "azure.tcl:." --add-data "theme:theme" GUI_DIS.py
