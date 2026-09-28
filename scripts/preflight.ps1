$ErrorActionPreference = 'Stop'
python -m pip install --upgrade pip
pip install -r requirements.txt
pytest -q
Write-Host "Preflight complete. This does not verify live Hindsight credentials or remote retain/recall."
