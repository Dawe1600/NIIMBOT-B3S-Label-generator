@echo off
cd /d "C:\Programowanie\auto_ewidencja"

:: Aktywuj wirtualne środowisko
call .venv\Scripts\activate.bat

:: Uruchom skrypt przez pythonw (w tle) i zamknij plik .bat
start "" pythonw kreator_naklejek_gui.py