@echo off
title Script Coverage AI

REM Check if the venv folder exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    echo.
    echo Virtual environment created.
    echo Installing required libraries...
    venv\Scripts\activate.bat
    pip install -r requirements.txt
    echo.
    echo Required libraries installed.
    echo.
)

REM Check if the venv folder exists after creating it
if exist venv (
    echo Activating virtual environment...
    venv\Scripts\activate.bat

    REM Launch main.py
    echo Launching AI Script Coverage...
    python main.py

    REM Deactivate the virtual environment
    echo Deactivating virtual environment...
    deactivate
) else (
    echo Failed to create virtual environment. Please check your Python installation and try again.
)

pause