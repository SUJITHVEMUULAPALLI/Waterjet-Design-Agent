# Waterjet Design Agent Launcher (PowerShell)
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "   WATERJET DESIGN AGENT LAUNCHER" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://python.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check directory
Write-Host "Checking if in correct directory..." -ForegroundColor Yellow
if (!(Test-Path "app.py")) {
    Write-Host "✗ ERROR: Please run this script from the waterjet_design_agent directory" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✓ In correct directory" -ForegroundColor Green

# Check dependencies
Write-Host "Checking dependencies..." -ForegroundColor Yellow
try {
    python -c "import streamlit" 2>$null
    Write-Host "✓ All dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "Installing missing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Create outputs directory
Write-Host "Checking outputs directory..." -ForegroundColor Yellow
if (!(Test-Path "data\outputs")) {
    New-Item -ItemType Directory -Path "data\outputs" | Out-Null
    Write-Host "✓ Created outputs directory" -ForegroundColor Green
} else {
    Write-Host "✓ Outputs directory exists" -ForegroundColor Green
}

# Check catalog
Write-Host "Checking catalog..." -ForegroundColor Yellow
try {
    python -c "import json; json.load(open('data/catalogue.json'))" 2>$null
    Write-Host "✓ Catalog loaded successfully" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Catalog file is corrupted or missing" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "   STARTING WATERJET DESIGN AGENT" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "The app will open in your web browser at:" -ForegroundColor Green
Write-Host "http://localhost:8501" -ForegroundColor Green
Write-Host ""
# Dynamically compute shape and category counts
$shapeInfo = python -c "import json; d=json.load(open('data/catalogue.json')); cats=set(); shapes=0; details={}; [cats.add(x['category']) or details.setdefault(x['category'], []).append(x['name']) or 0 for x in d['shapes']]; print(f'{len(d[\"shapes\"])}|{len(cats)}|' + '|'.join(f'{k}: {\", \".join(details[k])}' for k in details))" 2>$null
if ($LASTEXITCODE -eq 0 -and $shapeInfo -match '^(\d+)\|(\d+)\|(.*)$') {
    $shapeCount = $Matches[1]
    $categoryCount = $Matches[2]
    $categories = $Matches[3] -split '\|'
    Write-Host "Available shapes: $shapeCount designs across $categoryCount categories" -ForegroundColor Magenta
    foreach ($cat in $categories) {
        Write-Host "- $cat"
    }
} else {
    Write-Host "Available shapes: [unknown] designs across [unknown] categories" -ForegroundColor Magenta
}
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the application
streamlit run app.py
