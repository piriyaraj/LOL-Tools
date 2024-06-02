@echo off
REM Get the directory of the script
set DIR=%~dp0
cd /d %DIR%
if not exist LOL-Tools (
    echo Setup starting...
    call git clone https://github.com/piriyaraj/LOL-Tools.git > NUL 2>&1
)
cd LOL-Tools

call git restore .
call git pull > NUL 2>&1

if exist requirements.txt (
    pip install -r requirements.txt > NUL 2>&1
)

REM Run the Python script
python ShortsMaker.py
REM python test.py
