@echo off
chcp 65001 >nul
cd /d "%~dp0"
set DEMOEXAM_COURSE=programmer
title ДЭ 09.02.07-2-2027 - тренажёр «Программист»
call run.bat
