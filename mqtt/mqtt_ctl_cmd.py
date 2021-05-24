
import config
import time
import sys  
import os
import time
import logging
import requests


test="test/"
test=""

falcon_logger = logging.getLogger('gunicorn.error')
estado_proyector= "Ukn"
mosquitto_cmd="mosquitto_pub -h %s -p %s -t %s -m %s"


def Estado_Proyector():
    get_status_url="http://%s/cm?cmnd=status 10"
    falcon_logger.info("Solicitando estado del proyector.")
    url= get_status_url % config.MQTT.VIDEO_STAT_HOST
    try:
        r = requests.get(url)
    except: 
         falcon_logger.error("Error al conectar al Power meter %s" % config.MQTT.VIDEO_STAT_HOST)
         return "Ukn"
    if (r.status_code != 200):
        falcon_logger.error("Error %s al solicitar el estado del proyector" % r.status.code)
        return "Ukn"
    datos=r.json()
    consumo=datos["StatusSNS"]["ENERGY"]["ApparentPower"]
    if (consumo > int(config.MQTT.UMBRAL_ON)):
        estado_proyector="ON"
    else:
        estado_proyector="OFF"
    falcon_logger.info("Solicitando estado del proyector finalizada. Esta %s." % estado_proyector)
    return estado_proyector

def Estado_Audio():
    get_status_url="http://%s/cm?cmnd=status"
    falcon_logger.info("Solicitando estado del Audio.")
    url= get_status_url % config.MQTT.AUDIO_STAT_HOST
    try:
        r = requests.get(url)
    except: 
        falcon_logger.error("Error al conectar al Control Audio %s" % config.MQTT.AUDIO_STAT_HOST)
        return "Ukn"
    if (r.status_code != 200):
        falcon_logger.error("Error %s al solicitar el estado del audio" % r.status.code)
        return "Ukn"
    datos=r.json()
    estado=datos["Status"]["Power"]
    if (estado == 1 ):
        estado_audio="ON"
    else:
        estado_audio="OFF"
    falcon_logger.info("Solicitando estado del audio finalizada. Esta %s" % estado_audio)
    return estado_audio

def MQTT_Proyector(estado): 
    global test
    falcon_logger.info("Solicitando cambio estado proyector a %s" % estado)

    if (config.MQTT.POWER_CHECK):
        cur_stat=Estado_Proyector()
        if (estado == cur_stat):
            falcon_logger.info("El protector ya esta en %s. No hago nada" % estado)
            return estado
    else:
        falcon_logger.info("Power Control desactivado")

    falcon_logger.info("Enviando mensaje MQTT %sbroadlink/replay proyectoron" % test )
    cmd = mosquitto_cmd % (config.MQTT.HOST,config.MQTT.PORT,"broadlink/record","proyectoron")

    falcon_logger.info("Ejecutando %s" % cmd)
    rc = os.system(cmd)
    if (rc != 0):
        falcon_logger.info("Error %s al ejecutar mosquitto_pub")
    if (estado=="OFF"):
        falcon_logger.info("Ejecutando %s para off" % cmd)
        time.sleep(1)
        os.system(cmd)

    
    return 0,"ok"

def MQTT_Audio(estado): 
    global test


    if (config.MQTT.POWER_CHECK):
        cur_stat=Estado_Audio()
        if (estado == cur_stat):
            falcon_logger.error("El Audio ya esta en %s. No hago nada" % estado)
            return estado
    else:
         falcon_logger.error("Power Control desactivado")
         

        
    cmd = mosquitto_cmd % (config.MQTT.HOST,config.MQTT.PORT,"cmnd/audio/POWER",estado)
    falcon_logger.info("Ejecutando %s" % cmd)
    rc=os.system(cmd)
    if (rc != 0):
        falcon_logger.info("Error %s al ejecutar mosquitto_pub")

    return 0,"ok"

# Init and Subscribe MQTT



def on_connect(client, userdata, flags, rc):
    falcon_logger.warning('Conexion a MQTT server establecida (%s)' % client._client_id)
    gclient.subscribe(topic='tele/%s/#' % config.MQTT.POWER_TOPIC, qos=2)     


def on_message(client, userdata, message):
    falcon_logger.debug('Mensaje recibido topic: %s payload: %s' % (message.topic,message.payload.decode('utf-8')))
    t=message.topic.split("/")
 

