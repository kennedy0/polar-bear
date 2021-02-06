#!/usr/bin/env bash
OLD_CWD=$(pwd)
TOOLS_DIR=$(dirname "$0")
PROJECT_DIR="$TOOLS_DIR/.."
RESOURCES_DIR="$PROJECT_DIR/resources"
ICON_FILE="$RESOURCES_DIR/icon.png"
DIST_FOLDER="$PROJECT_DIR/dist"
PB_BUILD="$DIST_FOLDER/PolarBear"
ARCHIVE_SCRIPT="$TOOLS_DIR/archive_build.py"

# Setup
cd $PROJECT_DIR
rm -rf "$DIST_FOLDER"

# Create venv
echo "Creating virtual environment..."
python3 -m venv build-venv
. ./build-venv/bin/activate
echo "Installing requirements..."
python3 -m pip install -r "./requirements.txt"
python3 -m pip install pyinstaller==4.2

# Build
echo "Building PolarBear..."
pyinstaller \
  -y \
  --onedir \
  --noconsole \
  --name PolarBear \
  --icon=$ICON_FILE \
  --add-data="$PROJECT_DIR/config/presets/*:config/presets" \
  --add-data="$PROJECT_DIR/config/themes/*:config/themes" \
  --add-data="$PROJECT_DIR/resources/*:resources" \
  main.py

## Archive build
echo "Archiving build..."
python $ARCHIVE_SCRIPT $PB_BUILD

# Cleanup
echo Cleaning up...
rm -rf "$PROJECT_DIR/build"
rm -rf "$PROJECT_DIR/build-venv"
rm "$PROJECT_DIR/PolarBear.spec"
cd "$OLD_CWD"

echo "Build complete."