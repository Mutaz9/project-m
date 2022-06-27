#!/bin/bash
tmux kill-server
cd project-m
git fetch && git reset origin/main --hard
python3.10 -m venv venv
source venv/bin/activate
python3.10 -m pip install --upgrade pip
python3.10 -m pip install -r requirements.txt
systemctl daemon-reload
systemctl restart myportfolio