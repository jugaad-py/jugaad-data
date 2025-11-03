# PowerShell script to check version before push
param(
    [string]$ProjectName = "jugaad-data"
)

# Read version from pyproject.toml
try {
    $content = Get-Content "pyproject.toml" -Raw
    if ($content -match 'version\s*=\s*"([^"]+)"') {
        $currentVersion = $matches[1]
        Write-Host "Current version in pyproject.toml: $currentVersion" -ForegroundColor Green
    } else {
        Write-Host "Error: Could not parse version from pyproject.toml" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "Error reading pyproject.toml: $_" -ForegroundColor Red
    exit 1
}

# Check PyPI
try {
    Write-Host "Checking PyPI for existing version..." -ForegroundColor Yellow
    $response = Invoke-RestMethod -Uri "https://pypi.org/pypi/$ProjectName/$currentVersion/json" -ErrorAction Stop
    Write-Host "❌ ERROR: Version $currentVersion already exists on PyPI!" -ForegroundColor Red
    Write-Host "Please update the version in pyproject.toml before pushing." -ForegroundColor Red
    Write-Host "Current PyPI versions: https://pypi.org/project/$ProjectName/#history" -ForegroundColor Blue
    exit 1
} catch {
    if ($_.Exception.Response.StatusCode -eq 404) {
        Write-Host "✅ Version $currentVersion not found on PyPI. Safe to push!" -ForegroundColor Green
        exit 0
    } else {
        Write-Host "Error checking PyPI: $_" -ForegroundColor Red
        exit 1
    }
}