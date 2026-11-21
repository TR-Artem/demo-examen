@echo off
chcp 65001 >nul
cd /d "%~dp0"
title ДЭ 09.02.07 - тренажёр

where python >nul 2>nul
if %errorlevel%==0 (
    python trainer.py
) else (
    py -3 trainer.py
)

if errorlevel 1 (
    echo.
    echo ============================================================
    echo  Не удалось запустить тренажёр.
    echo  Установите Python 3.10+ с https://www.python.org/downloads/
    echo  При установке отметьте "Add Python to PATH".
    echo ============================================================
    pause
)
