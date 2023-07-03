#!/usr/bin/env bash

virtualenv /home/ubuntu/env
source /home/ubuntu/env/bin/activate
sudo apt-get install pkg-config
pip install mysqlclient
pip install -r /home/ubuntu/TaskNet/requirements.txt