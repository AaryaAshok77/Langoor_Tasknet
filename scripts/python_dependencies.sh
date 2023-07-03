#!/usr/bin/env bash

virtualenv /home/ubuntu/env
source /home/ubuntu/env/bin/activate
sudo apt-get update
sudo apt-get install -y libmysqlclient-dev
pip install mysqlclient
pip install -r /home/ubuntu/TaskNet/requirements.txt
