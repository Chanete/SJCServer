#!/usr/bin/python3
# Version V0
import sys
sys.path.append('/home/sjc/SJCServer/')
import config
from yt_functions.yt_functions import get_authenticated_service
from oauth2client.tools import argparser
import logging 
from  telegram_send import send as TG_Send
import time

logging.basicConfig(level=logging.INFO)
logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)
logging.getLogger('googleapiclient.discovery').setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('%s' % config.SERVER.CHECKER_LOG)
fh.setFormatter(formatter)
falcon_logger = logging.getLogger('gunicorn.error')

falcon_logger.addHandler(fh)

falcon_logger.info("Iniciando verificacion") 



for canal in config.YT.CANALES.keys():
    falcon_logger.info("Comprobando canal %s " % canal) 
    rc,youtube = get_authenticated_service(canal,"") 
    if (rc == 0):
        falcon_logger.info("Canal Youtube %s OK" %canal) 
    else: 
        falcon_logger.info("Error en canal Youtube %s (%s) url: %s" % (canal,rc,youtube) )
        TG_Send(messages=["Error %s al verificar canal %s" % (rc,canal),youtube])
        time.sleep(10)
