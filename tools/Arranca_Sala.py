#!/usr/bin/python3
# Versio V0
import sys
sys.path.append('/home/sjc/SJCServer')
import config
from yt_functions.yt_functions import YT_Get_Transmisions
from yt_functions.yt_functions import YT_SetPublic
from yt_functions.yt_functions import YT_Get_Stream_Data
from obsctl.obsctl import OBS_StartStreaming
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
    dt=datetime. strptime(fecha, '%Y-%m-%d %H:%M').timestamp()
    r=(dt-b)/60
    if (r < 20) and (r > 0):
        flag=False
        break

if (flag):
    falcon_logger.info("No hay transmisiones en los proximos 20 min")
    TG_Send(messages=["No hay transmisiones en los proximos 20 min"])
    sys.exit(12)


sala=True; 
if (len(sys.argv)>1):
    parm=sys.argv[1]
    if (parm=="NOSALA"):
        falcon_logger.info("No se activará la sala de abajo")
        TG_Send(messages=["No se activará la sala de abajo"])
        sala=False

falcon_logger.info("Vamos a emitir %s a las %s en el canal %s" % (titulo,fecha,canal))
TG_Send(messages=["Vamos a emitir %s a las %s en el canal %s" % (titulo,fecha,canal)])
falcon_logger.info("Obteniendo key e ingestion addr")
key,ingestion,stat=YT_Get_Stream_Data(sid,canal)
falcon_logger.info("Key: %s Ingestion %s" % (key,ingestion))
falcon_logger.info("Streaming data OK")
rc,msg =OBS_StartStreaming(key,ingestion)
falcon_logger.info("Streaming Started")
if (rc != 0):
    falcon_logger.info("Error al arrancar Streaming rc: %s - %s" % (rc,msg))
    TG_Send(messages=["Error al arrancar Streaming rc: %s - %s" % (rc,msg)])
    sys.exit(12)
YT_SetPublic(bid,canal,"Public")
falcon_logger.info("Canal en publico")
TG_Send(messages=["Emitiendo...."])
time.sleep(2)
falcon_logger.info("Escena espera")
OBS_Escena("Waiting")
time.sleep(15)
if (sala):
    falcon_logger.info("Encendiendo sala")
    MQTT_Audio("ON")            
    MQTT_Proyector("ON")
    Play(bid)
    TG_Send(messages=["Sala encendida"])
b=datetime.now().timestamp()
dt=dt-(60*5)
r=(dt-b)/60
while (r > 0):
    time.sleep(30)
    b=datetime.now().timestamp()
    r=(dt-b)/60
    falcon_logger.info("Quedan %0.2f para poner plano general" % r)
    TG_Send(messages=["Quedan %0.2f para poner plano general" % r])

OBS_Escena("Escena")
falcon_logger.info("Todo terminado")
TG_Send(messages=["Escena general activada. Emision en curso"])