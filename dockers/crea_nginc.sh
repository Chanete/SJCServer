#/bin/bash
docker run --name nginx -p 1313-1320:1313-1320 -p 8081:8081 -v /var/log/nginx:/var/log/nginx -v /home/:/home/ -v /etc/nginx/conf.d/:/etc/nginx/conf.d/:ro -d nginx
