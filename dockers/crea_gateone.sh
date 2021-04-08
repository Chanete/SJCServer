#/bin/bash
docker run -d --name=gateone --restart=always -p 8008:443 -v /etc/gateone:/etc/gateone dezota/gateone
