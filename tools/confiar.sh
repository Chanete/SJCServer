#!/bin/sh
#ssh-keygen -t rsa
echo "Necesito Usuario IP $1 $2"
ssh -p 8022 $1@$2 'mkdir -p .ssh'
cat .ssh/id_rsa.pub | ssh -p 8022 $1@$2 'cat >> .ssh/authorized_keys'
