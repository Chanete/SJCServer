#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config
import sys
import time
import os
import psutil

import logging
logging.getLogger('gunicorn.error')
logging.basicConfig(level=logging.INFO)
falcon_logger = logging.getLogger('gunicorn.error')
from obswebsocket import obsws, requests  # noqa: E402

host = "localhost"
port = 4444
password = "secret"

def Mata_Proceso(proceso):
    for p in psutil.process_iter():
    #            falcon_logger.info(p.name())
        if proceso in p.name() or proceso in ' '.join(p.cmdline()):
            falcon_logger.info(" Matando %s..." % proceso)
            p.terminate()
            p.wait()
    

def OBS_SetCamUrl(url):
    falcon_logger.info("Configurando camara OBS en %s" % url)
    ws = obsws(host, port, password)
    try:
        ws.connect()
    except:
        return 1,"Error de Conexion - ¿OBS Parado?)"

    settings= {'playlist': \
                [ 
                    {'hidden': False, 
                    'selected': False,
                    'value': url
                    }
                ]
                }
    ws.call(requests.SetSourceSettings(sourceSettings=settings,sourceName=config.OBS.SOURCE_NAME,sourceType=config.OBS.SOURCE_TYPE))
    falcon_logger.info("Camara configurada.")
    ws.disconnect()

def OBS_SetSyncOffset():
    falcon_logger.info("Configurando Sync Offset de %s en %s nanonesgundos" % (config.OBS.AUDIO_SOURCE,config.OBS.AUDIO_SYNC))
    ws = obsws(host, port, password)
    try:
        ws.connect()
    except:
        return 1,"Error de Conexion - ¿OBS Parado?)"

    ws.call(requests.SetSyncOffset(source=config.OBS.AUDIO_SOURCE,offset=config.OBS.AUDIO_SYNC))
    falcon_logger.info("Sync Offset configurado..")
    ws.disconnect()


def OBS_StopStreaming():
    ws = obsws(host, port, password)
    try:
        ws.connect()
    except:
        return 1,"Error de Conexion - ¿OBS Parado?)"
    falcon_logger.info("Parando Streaming")
    ws.call(requests.StopStreaming())
    ws.disconnect()
    falcon_logger.info("Streaming Parado")
#    Mata_Proceso("obs")
#    falcon_logger.info("OBS Matado")
    return 0,"Ok"


def OBS_Escena(Escena):
    falcon_logger.info("Cambiando a escena: %s" % Escena)
    ws = obsws(host, port, password)
    try:
        ws.connect()
    except:
        return 1,"Error de Conexion - ¿OBS Parado?)"

    ws.call(requests.SetCurrentScene(Escena))
    ws.disconnect()
    return 0,"Ok"


def OBS_Lista_Escenas():
    falcon_logger.info("Lista Escenas")
    ws = obsws(host, port, password)
    lista=[]
    try:
        ws.connect()
    except:
        return 1,"Error de Conexion - ¿OBS Parado?)", lista
    scenes = ws.call(requests.GetSceneList())
    for s in scenes.getScenes():
        falcon_logger.info(s['name'])
        lista.append(s['name'])
    ws.disconnect()
    return 0,"OK",lista


def OBS_StartStreaming(key,ingestion):
    """Handles GET requests"""
    falcon_logger.info("OBS_StartStreaming")
    falcon_logger.info("Key: %s Ingestion: %s" % (key,ingestion))
    OBS_SetCamUrl(config.OBS.CAM_URL)
    ws = obsws(host, port, password)
    try:
        ws.connect()
    except:
        return 1,"Error de Conexion - ¿OBS Parado? - StartStreaming)"

    falcon_logger.info("Inicio Streaming")

    stream_settings = {
        "server":ingestion,
        "key":key,
        "use_auth":False
    }
    stream = {
        "settings":stream_settings,
        "type":"rtmp_custom"
    }

    rc=ws.call(requests.StartStreaming(stream))
    falcon_logger.info(rc)
    ws.disconnect()
    return 0,"Ok"


