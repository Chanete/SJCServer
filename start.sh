#/bin/bash
#gunicorn SJC_Server:api -b 192.168.1.246 --access-logfile /var/log/SJC_Server/SJC_Server.log
gunicorn SJC_Server:api 