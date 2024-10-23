#!/bin/bash

rm -rfv build
rm -rfv dist

pyinstaller PythonBot.spec

# Create spec file:
# pyinstaller --onefile --windowed --icon app-icon.icns --name PythonBot src/main.py

cd dist
open .
