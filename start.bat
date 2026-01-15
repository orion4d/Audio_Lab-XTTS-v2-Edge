@echo off
title Coqui XTTS-v2 Launcher
echo Demarrage de l'interface XTTS...
echo.

:: Se placer dans le dossier du script (au cas où on lance en admin)
cd /d "%~dp0"

:: Verification de l'environnement virtuel
if not exist venv (
    echo [ERREUR] Le dossier 'venv' est introuvable !
    echo Veuillez d'abord installer le projet.
    pause
    exit
)

:: Activation de l'environnement
call venv\Scripts\activate

:: Lancement du script Python
python app.py

:: Pause pour lire les erreurs si ça plante
if %errorlevel% neq 0 (
    echo.
    echo Une erreur s'est produite.
    pause
)