#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import os
import psutil

import logging
logging.basicConfig(level=logging.INFO)

from obswebsocket import obsws, requests  # noqa: E402

def dump(obj):
  for attr in dir(obj):
    print("obj.%s = %r" % (attr, getattr(obj, attr)))

host = "localhost"
port = 4444
password = "secret"

ws = obsws(host, port, password)
try:
    ws.connect()
except:
    print("Error de conexion")
    sys.exit(12)

resp=ws.call(requests.GetSourcesList())
print("\n\n***")

for resource in resp.getSources():
    nombre=resource["name"]
    print(nombre)

    if (nombre=="Cam1"):
        sett=ws.call(requests.GetSourceSettings(nombre))
        print(sett)
        req= {'sourceName': 'Cam1', 'sourceSettings': {'input': 'rtsp://admin:@192.168.1.110/1/h264major', 'is_local_file': False}, 'sourceType': 'ffmpeg_source'}
        print(req)
        req["sourceSettings"]["input"]="rtsp://admin:@192.168.1.110/mpeg4main"
        sett=ws.call(requests.SetSourceSettings(sourceSettings=req,sourceName='Cam1'))
        print("Devuelve")
        print(sett)
ws.disconnect()
    
