import paho.mqtt.client
import time
import sys  
import os
import time
import logging

MQTT_HOST="192.168.1.248"
MQTT_PORT=1883
test="test/"
test=""
falcon_logger = logging.getLogger('gunicorn.error')
client = paho.mqtt.client.Client(client_id='SJCWebApp-Mqtt', clean_session=True)

def MQTT_Proyector(estado): 
    global test
    falcon_logger.error("Enviando mensaje MQTT %sbroadlink/replay proyectoron" % test )
    try:
        client.connect(host=MQTT_HOST, port=MQTT_PORT)
        client.publish("%sbroadlink/record" % test,"proyectoron" )
        if (estado=="OFF"):
            time.sleep(1)
            client.publish("%sbroadlink/record" % test,"proyectoron" )
            falcon_logger.error("Enviando mensaje MQTT %sbroadlink/replay proyectoron" % test )
        client.disconnect()
    except:
        return 9,"Error de conexion"
    return 0,"ok"

def MQTT_Audio(estado): 
    global test
    falcon_logger.error("Enviando mensaje MQTT %scmnd/audio/power %s" % (test,estado ))
    try:
        client.connect(host=MQTT_HOST, port=MQTT_PORT)
        client.publish("%scmnd/audio/POWER" % test, estado)
        client.disconnect()
    except: 
        return 9,"Error de conexion"
    return 0,"ok"