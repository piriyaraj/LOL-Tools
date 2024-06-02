@echo off
REM Get the directory of the script
set DIR=%~dp0
cd /d %DIR%
if not exist LOL-Tools (
    call git clone https://github.com/piriyaraj/LOL-Tools.git
)
cd LOL-Tools

if exist requirements.txt (
    pip install -r requirements.txt > NUL 2>&1
)

REM Configure git
git restore .
git pull

REM Run the Python script
python ChangeGUI.py
REM python test.py
