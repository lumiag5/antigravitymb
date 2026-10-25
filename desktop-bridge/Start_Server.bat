@echo off
title Antigravity Mobile - Desktop Bridge
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    where py >nul 2>nul
    if errorlevel 1 (
        echo.
        echo ====================================================================
        echo  [ERRO] Python nao foi encontrado no seu computador!
        echo ====================================================================
        echo.
        echo  Para usar o Antigravity Mobile:
        echo   1. Baixe o Python em: https://www.python.org/downloads/
        echo   2. Na instalacao, MARQUE a caixa "Add Python to PATH".
        echo.
        pause
        exit /b 1
    ) else (
        py -3 run.py
        goto end
    )
)

python run.py

:end
if errorlevel 1 (
    echo.
    echo ====================================================================
    echo  [AVISO] O servidor foi encerrado.
    echo ====================================================================
    echo.
    pause
)
