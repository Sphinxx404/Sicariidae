#bin/bash

PYTHON=python3
PIP=pip3

if [ ! -f requirements.txt ];
then
   echo "[!] FileNotFoundError: requirements.txt is required!"
   exit 1
fi

$PIP install -r requirements.txt
echo "[+] Sicariidae has been successfully installed."
echo "Tip: Run python3 sicariidae.py"
