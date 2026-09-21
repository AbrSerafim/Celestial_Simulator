Write-Host "Setting up project..."

winget install Python.Python.3.9 --accept-package-agreements --accept-source-agreements --disable-interactivity
py -3.9 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Host "Done!"