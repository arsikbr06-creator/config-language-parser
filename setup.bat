@echo off
REM Installation and Setup Script

echo ================================================
echo Configuration Language Parser - Setup
echo ================================================
echo.

REM Find Python installation
set "PYTHON_EXE="

REM Check common Python locations
for %%P in (
    "python.exe"
    "C:\Python*\python.exe"
    "C:\Program Files\Python*\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python*\python.exe"
) do (
    if exist "%%~P" (
        set "PYTHON_EXE=%%~P"
        goto :found_python
    )
)

REM Try to find via where command
where python.exe >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=*" %%i in ('where python.exe') do (
        set "PYTHON_EXE=%%i"
        goto :found_python
    )
)

REM Try to find in AppData
for /f "tokens=*" %%i in ('dir /b /s "%LOCALAPPDATA%\Programs\Python\python.exe" 2^>nul') do (
    set "PYTHON_EXE=%%i"
    goto :found_python
)

echo ERROR: Python not found!
echo Please install Python 3.7+ from https://www.python.org/
echo Or add Python to PATH
pause
exit /b 1

:found_python
echo Found Python: %PYTHON_EXE%
"%PYTHON_EXE%" --version
echo.

REM Install dependencies
echo Installing dependencies...
"%PYTHON_EXE%" -m pip install --upgrade pip
"%PYTHON_EXE%" -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ================================================
echo Setup completed successfully!
echo ================================================
echo.
echo You can now run the parser:
echo   "%PYTHON_EXE%" config_lang_parser.py test_simple.conf
echo.
echo Run tests:
echo   "%PYTHON_EXE%" -m pytest test_config_parser.py -v
echo.
echo Python path saved to python_path.txt
echo %PYTHON_EXE% > python_path.txt
pause
