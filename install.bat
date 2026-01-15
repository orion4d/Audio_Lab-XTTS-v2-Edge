@echo off
title Installation XTTS & Edge-TTS
cd /d "%~dp0"

echo ===================================================
echo   INSTALLATION XTTS V2 + EDGE (Python 3.10)
echo ===================================================
echo.

:: 1. Vérification Python
py -3.10 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python 3.10 introuvable !
    pause
    exit
)

:: 2. Vérification existence venv
if not exist venv goto :creation

echo [ATTENTION] Le dossier 'venv' existe deja.
set /p choix="Voulez-vous le supprimer et reinstaller ? (O/N) : "

:: Si ce n'est pas O, on arrête
if /i "%choix%" neq "O" exit

echo.
echo Suppression de l'ancien venv...
rmdir /s /q venv

:: Vérification si la suppression a marché
if exist venv (
    echo.
    echo [ERREUR] Impossible de supprimer le dossier 'venv'.
    echo Quelque chose bloque le fichier (peut-etre VS Code ou un terminal).
    echo Veuillez supprimer le dossier 'venv' manuellement et relancer.
    pause
    exit
)

:creation
echo.
echo Creation de l'environnement virtuel...
py -3.10 -m venv venv

:: 3. Installation
echo.
echo Activation et installation des dependances...
call venv\Scripts\activate

python -m pip install --upgrade pip
echo Installation des paquets...
pip install -r requirements.txt

echo.
echo ===================================================
echo INSTALLATION TERMINEE !
echo ===================================================
pause