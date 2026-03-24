@echo off
setlocal

:: Vérifie que le venv existe
if not exist ".venv\Scripts\python.exe" (
    echo Erreur : l'environnement virtuel .venv n'existe pas.
    echo Lance "python -m venv .venv" puis installe les dépendances.
    exit /b 1
)

:: Utilise le Python du venv
set PYTHON_EXEC=.\.venv\Scripts\python.exe

:: Lancer deux fenêtres cmd avec différents arguments
start cmd /k "%PYTHON_EXEC% main.py"

endlocal
