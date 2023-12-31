#!/usr/bin/bash

sudo systemctl daemon-reload
sudo rm -f /etc/nginx/sites-enabled/default

sudo cp /home/ubuntu/TaskNet/nginx/nginx.conf /etc/nginx/sites-available/TaskNet
sudo ln -s /etc/nginx/sites-available/TaskNet /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
sudo ufw delete allow 8000
sudo ufw allow 'Nginx Full'