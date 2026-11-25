@echo off
chcp 65001 >nul
cd /d "%~dp0"
title ДЭ 09.02.07-2 - магазин обуви
where python >nul 2>nul
if %errorlevel%==0 (
    python app.py
) else (
    py -3 app.py
)
if errorlevel 1 pause
