#!/bin/bash
#gunicorn SJC_Server:api -b 192.168.1.246 --access-logfile /var/log/SJC_Server/SJC_Server.log
cd /home/sjc/SJCServer
#Xvfb -shmem -screen 0 1280x1024x24 &
export DISPLAY=:0
gunicorn SJC_Server:api -t 125      
