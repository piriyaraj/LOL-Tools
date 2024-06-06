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
@REM call git add .
@REM call git commit -m "LOL-Tools updated"
@REM call git push


if exist requirements.txt (
    pip install -r requirements.txt > NUL 2>&1
)

REM Run the Python script
python ThumbnailMaker.py
REM python test.py
@REM call git add .
@REM call git commit -m "LOL-Tools updated"
@REM call git push
@REM call git pull > NUL 2>&1