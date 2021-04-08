#!/bin/sh
sudo cp broadlink_mqtt.service /etc/systemd/system/
sudo mkdir -p /var/log/broadlink
sudo chown sjc:root /var/log/broadlink 
sudo systemctl enable broadlink_mqtt
