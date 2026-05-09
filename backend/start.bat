@echo off
cd /d "%~dp0"
set PYTHONPATH=%~dp0src
python -m uvicorn src.main:app --reload --port 8000
