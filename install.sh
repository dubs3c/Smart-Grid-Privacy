#!/bin/bash

if [ "$EUID" -ne 0 ]
	then echo "[*] Please run as root"
	exit
fi


echo "============================ BEGIN INSTALLATION ============================"
apt-get install python-dev libssl-dev libffi-dev vim -y
echo 'alias ll="ls -lah"' >> ~/.bashrc
source ~/.bashrc
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
pip install -r requirements.txt
python -c "import petlib; petlib.run_tests()"
echo ""
echo "============================ INSTALLATION COMPLETE ============================"
