# Setup script for Configuration Language Parser
# This script finds Python and installs dependencies

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Configuration Language Parser - Setup" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Function to find Python
function Find-Python {
    # Check if python command works
    try {
        $version = & python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            return "python"
        }
    } catch {}
    
    # Search in common locations
    $locations = @(
        "$env:LOCALAPPDATA\Programs\Python\Python*\python.exe",
        "C:\Python*\python.exe",
        "C:\Program Files\Python*\python.exe"
    )
    
    foreach ($pattern in $locations) {
        $found = Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($found) {
            return $found.FullName
        }
    }
    
    return $null
}

Write-Host "Searching for Python installation..." -ForegroundColor Yellow
$pythonPath = Find-Python

if (-not $pythonPath) {
    Write-Host "ERROR: Python not found!" -ForegroundColor Red
    Write-Host "Please install Python 3.7+ from https://www.python.org/" -ForegroundColor Red
    Write-Host "Or add Python to PATH" -ForegroundColor Red
    pause
    exit 1
}

Write-Host "Found Python: $pythonPath" -ForegroundColor Green
& $pythonPath --version
Write-Host ""

# Save Python path for future use
$pythonPath | Out-File -FilePath "python_path.txt" -Encoding UTF8

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
& $pythonPath -m pip install --upgrade pip
& $pythonPath -m pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    pause
    exit 1
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "Setup completed successfully!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "You can now run the parser:" -ForegroundColor Cyan
Write-Host "  & `"$pythonPath`" config_lang_parser.py test_simple.conf" -ForegroundColor White
Write-Host ""
Write-Host "Run tests:" -ForegroundColor Cyan
Write-Host "  & `"$pythonPath`" -m pytest test_config_parser.py -v" -ForegroundColor White
Write-Host ""

pause
