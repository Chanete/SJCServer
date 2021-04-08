#!/bin/sh
sudo cp SJCServer.service /etc/systemd/system/
sudo mkdir -p /var/log/SJCServer
sudo chown sjc:root /var/log/SJCServer
sudo systemctl enable SJCServer 
