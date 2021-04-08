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

for resource in resp.getSources():
    nombre=resource["name"]
    print("\n\n %s \n\n" % nombre)
    sett = ws.call(requests.GetSyncOffset(nombre))
    print(sett)

    if (nombre=="Fuente de vídeo VLC"):
        print("\n\n Resource")
        print(resource)
        sett=ws.call(requests.GetSourceSettings(nombre))
#        print("\n\n Settings \n",sett,"\n\n")


        """
        req= {'sourceName': nombre,
              'sourceType': 'vlc_source', 
              'sourceSettings':
        """
        settings= {'playlist': \
                    [ 
                        {'hidden': False, 
                        'selected': False,
                        'value': "rtsp://192.168.1.110:554/1/h264major"
                        }
                    ]
                   }
 

        print("\n\ Pido: \n")
        print(sett)
        sett=ws.call(requests.SetSourceSettings(sourceSettings=settings,sourceName=nombre,sourceType='vlc_source'))
        print("\n\nDevuelve\n")
        print(sett)
       
ws.disconnect()
    
