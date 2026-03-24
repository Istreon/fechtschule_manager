setlocal

:: Vérifie que le venv existe
if not exist ".venv\Scripts\python.exe" (
    echo Erreur : l'environnement virtuel .venv n'existe pas.
    echo Lance "python -m venv .venv" puis installe les dépendances.
    exit /b 1
)

:: Utilise le Python du venv
set PYTHON_EXEC=.\.venv\Scripts\python.exe

:: Build avec PyInstaller depuis le venv
%PYTHON_EXEC% -m PyInstaller main.py --noconfirm --onefile --name "Fechtool"


endlocal
