Write-Host "Setting up project..."

winget install Python.Python.3.9 --accept-package-agreements --accept-source-agreements --disable-interactivity

Write-Host "Creating venv"

py -3.9 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pyinstaller --clean --noconfirm --onefile --name Celestial_Simulator --add-data "src/gui;gui" --add-data "data;data" .\src\celestial_simulator.py

Write-Host "Done!"

mv .\dist\Celestial_Simulator.exe .\Celestial_Simulator.exe
rm -r .\dist\
.\Celestial_Simulator.exe 