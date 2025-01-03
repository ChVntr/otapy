@echo off





:: checando se tem python instalado

(python -V) || (
    echo PYTHON NAO ENCONTRADO
    echo.
    echo INSTALE PYTHON E REINICIE O PROGRAMA PARA CONTINUAR
    echo.
    pause
    exit
) 
cls





:: baixando o script em python

set pylink=https://raw.githubusercontent.com/ChVntr/otapy/refs/heads/main/ota.py

if exist otapy\ (
    set otapy=1
) else (
    echo BAIXANDO ARQUIVOS NECESSARIOS...
    echo.
    mkdir otapy
    cd otapy
    powershell Invoke-WebRequest %pylink% -OutFile ota.py
    cd ..
    set otapy=1
) 
cls







:: instalando player se não tiver um instalado


    if exist otapy\mpv (
        set player=1
        cls
        echo VERIFICANDO VERSAO DO REPRODUTOR...
        echo.
        cd otapy\mpv
        del updater.bat
        powershell Invoke-WebRequest https://github.com/ChVntr/otapy/releases/download/depend/updater.bat -OutFile updater.bat
        CALL updater.bat
        cd..
        cd..
    ) else (
        set player=0
    )

cls

if %player% == 0 (
    echo INSTALANDO REPRODUTOR DE VIDEO...
    cd otapy
    mkdir mpv
    powershell Invoke-WebRequest https://github.com/ChVntr/otapy/releases/download/depend/mpv.zip -OutFile mpv.zip
    powershell Expand-Archive mpv.zip -DestinationPath mpv
    del mpv.zip
    cd mpv
    echo fs=yes >> mpv.conf
    del updater.bat
    powershell Invoke-WebRequest https://github.com/ChVntr/otapy/releases/download/depend/updater.bat -OutFile updater.bat
    CALL updater.bat
    cd..
    cd..
) 
cls







if %otapy% == 1 (
    cd otapy
    del ota.py
)

powershell Invoke-WebRequest %pylink% -OutFile ota.py
cls
ota.py || (
    echo oh shit
    pause
)
exit

