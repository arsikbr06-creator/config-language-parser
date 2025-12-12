@echo off
REM Quick test script

REM Try to find Python
set "PYTHON_EXE="

REM Check if python_path.txt exists
if exist "python_path.txt" (
    set /p PYTHON_EXE=<python_path.txt
    goto :run_tests
)

REM Try common locations
for %%P in (
    "python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python*\python.exe"
) do (
    if exist "%%~P" (
        set "PYTHON_EXE=%%~P"
        goto :run_tests
    )
)

REM Try to find in AppData
for /f "tokens=*" %%i in ('dir /b /s "%LOCALAPPDATA%\Programs\Python\python.exe" 2^>nul') do (
    set "PYTHON_EXE=%%i"
    goto :run_tests
)

echo ERROR: Python not found! Please run setup.bat first
pause
exit /b 1

:run_tests
echo Using Python: %PYTHON_EXE%
echo.

echo Running tests...
echo.
"%PYTHON_EXE%" -m pytest test_config_parser.py -v

echo.
echo ================================================
echo Testing parser with example file...
echo ================================================
echo.

echo Input (test_simple.conf):
type test_simple.conf
echo.
echo.

echo Output (YAML):
"%PYTHON_EXE%" config_lang_parser.py test_simple.conf

pause
