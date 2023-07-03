#!/usr/bin/env bash

virtualenv /home/ubuntu/env
source /home/ubuntu/env/bin/activate
sudo apt-get update
pip install -r /home/ubuntu/TaskNet/requirements.txt
