@echo off
chcp 65001 >nul
cd /d "%~dp0lab"
title ДЭ 09.02.07 - образец приложения

where python >nul 2>nul
if %errorlevel%==0 (
    python example_app.py
) else (
    py -3 example_app.py
)

if errorlevel 1 (
    echo.
    echo Не удалось запустить образец. Установите Python 3.10+ с python.org
    pause
)
