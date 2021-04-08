#/bin/bash
docker run   -p 3478:3478/udp \
  -p 10001:10001/udp \
  -p 8080:8080 \
  -p 8443:8443 \
  -p 1900:1900/udp  \
  -p 8843:8843  \
  -p 8880:8880  \
  -p 6789:6789  \
  -p 5514:5514   -e TZ='Europe/Madrid' -v ~/unifi:/unifi --name unifi --restart=always jacobalberty/unifi:6.0.45
