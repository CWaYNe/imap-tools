#!/bin/sh

python3 -m venv ./venv

echo "請直接在shell 手動執行以下指令 (Freebsd csh 執行以下會錯誤)"

# for freebsd c shell
source venv/bin/activate.csh

pip install -r ./requirements.txt