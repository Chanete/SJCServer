#!/usr/bin/python3
# Versio V0
import sys
sys.path.append('/home/sjc/SJCServer')
import config
from yt_functions.yt_functions import YT_Get_Transmisions
from yt_functions.yt_functions import YT_SetPublic
from yt_functions.yt_functions import YT_Get_Stream_Data
from yt_functions.yt_functions import YT_StopBroadcasting
from obsctl.obsctl import OBS_StartStreaming
from obsctl.obsctl import OBS_StopStreaming
from mqtt.mqtt_ctl import MQTT_Proyector
from mqtt.mqtt_ctl import MQTT_Audio
from OV_ctl.OV_ctl import OV_Move_to_preset
from player.Chrome import Play
from player.Chrome import Media_Stop
from obsctl.obsctl import OBS_Escena
from player.Chrome import Play

from datetime import datetime

import sys
import time
import logging
from  telegram_send import send as TG_Send

logging.basicConfig(level=logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh = logging.FileHandler('%s' % config.SERVER.LOGFILE)
fh.setFormatter(formatter)
falcon_logger = logging.getLogger('gunicorn.error')
falcon_logger.addHandler(fh)


# obtener lista de transmisiones
rc,msg,items=YT_Get_Transmisions()
if (rc != 0):
    if (rc == 99):
                falcon_logger.info("Error credenciales YouTube")
                TG_Send(messages=["Errir en credenciales YouTube para parar sala"])
                sys.exit(12)
    falcon_logger.info("Error al obtener transmisiones %s - %s" % (r,msg))
b=datetime.now().timestamp()
flag=True
for t in items:
    fecha=t["Fecha_Sched"]
    titulo=t["titulo"]
    bid=t["broadcast_id"]
    sid=t["streamId"]
    canal=t["Canal"]
    status=t["status"]
    if (status=="live"):
            falcon_logger.info("Parando transmision %s. " % titulo)
            TG_Send(messages=["Parando transmision %s. " % titulo])
            MQTT_Audio("OFF")            
            MQTT_Proyector("OFF")
            YT_SetPublic(bid,canal,"Private")
            Media_Stop()
            time.sleep(3)
            OV_Move_to_preset(1,"General")
            rc,msg=OBS_StopStreaming()
            rc,msg=YT_StopBroadcasting(bid,canal,"")
            falcon_logger.info("Transmision terminada. Todo apagado. ")
            TG_Send(messages=["Transmision terminada. Todo apagado. "])
            break; 
