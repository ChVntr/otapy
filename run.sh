#!/bin/bash

clear

cd ~
file=./otapy
if [ ! -e "$file" ]; then
    mkdir otapy
fi

cd otapy

file=./ota.py
if [ -e "$file" ]; then
    rm ota.py
fi

wget https://raw.githubusercontent.com/ChVntr/otapy/refs/heads/main/ota.py

clear

python ota.py