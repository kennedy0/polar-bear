@echo off
set VENV_ACTIVATE=C:\Users\a\venv\screen_cap_2\Scripts\activate
set OLD_CWD=%cd%
set TOOLS_DIR=%~dp0
set PROJECT_DIR=%TOOLS_DIR%\..
set RESOURCES_DIR=%PROJECT_DIR%\resources
set ICON_FILE=%RESOURCES_DIR%\icon.ico

cd %PROJECT_DIR%

:: Create venv
echo Creating virtual environment...
python -m venv build-venv
call build-venv\Scripts\activate
echo Installing requirements...
python -m pip install -r requirements.txt
python -m pip install pyinstaller==4.1

:: Build
echo Building PolarBear.exe...
pyinstaller^
 -y^
 --onedir^
 --noconsole^
 --name PolarBear^
 --icon=%ICON_FILE%^
 --add-data="config\presets\*;.\config\presets"^
 --add-data="resources\*;.\resources"^
 main.py

:: Cleanup
echo Cleaning up...
rmdir %PROJECT_DIR%\build /s /q
rmdir %PROJECT_DIR%\build-venv /s /q
del
cd %OLD_CWD%

echo Build complete.