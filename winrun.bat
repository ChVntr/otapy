@echo off


%userprofile:~0,2%

cd %userprofile%\appdata\local\programs


rd /q /s "otapy"

set pylink=https://raw.githubusercontent.com/ChVntr/otapy/refs/heads/main/ota.py

if exist otapy\ (
    set otapy=1
) else (
    set otapy=0
    echo BAIXANDO ARQUIVOS NECESSARIOS...
    echo.
    mkdir otapy
    cd otapy
    powershell Invoke-WebRequest %pylink% -OutFile ota.py
    mkdir mpv
    powershell Invoke-WebRequest https://github.com/ChVntr/otapy/releases/download/depend/mpv.zip -OutFile mpv.zip
    powershell Expand-Archive mpv.zip -DestinationPath mpv
    del mpv.zip
)


if %otapy% == 1 (
    cd otapy
    del ota.py
)

powershell Invoke-WebRequest %pylink% -OutFile ota.py
cls
ota.py










echo oh shit
pause
