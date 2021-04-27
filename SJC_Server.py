#
#  SJC_Server - Proceso Gunicorn que recibe todas las peticiones y las encamina a las funciones correspondientes
#
import config
import requests as rq
import falcon
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
import json
import sys
import time
import os
import psutil
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)
logging.getLogger('googleapiclient.discovery').setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('%s' % config.SERVER.LOGFILE)
fh.setFormatter(formatter)
falcon_logger = logging.getLogger('gunicorn.error')

falcon_logger.addHandler(fh)
from obswebsocket import obsws, requests  # noqa: E402
from obsctl.obsctl import OBS_StopStreaming
from obsctl.obsctl import OBS_Escena
from obsctl.obsctl import OBS_Lista_Escenas
from obsctl.obsctl import OBS_StartStreaming
from obsctl.obsctl import OBS_SetCamUrl
from obsctl.obsctl import OBS_SetSyncOffset


from yt_functions.yt_functions import YT_Programa_Misa
from yt_functions.yt_functions import YT_Get_Transmisions
from yt_functions.yt_functions import YT_StartBroadcasting
from yt_functions.yt_functions import YT_StopBroadcasting
from yt_functions.yt_functions import YT_Get_Stream_Data
from yt_functions.yt_functions import YT_SetPublic
from yt_functions.yt_functions import YT_DeleteBroadcast
from yt_functions.yt_functions import YT_Code
from mqtt.mqtt_ctl import MQTT_Proyector
from mqtt.mqtt_ctl import MQTT_Audio
from OV_ctl.OV_ctl import OV_Move_to_preset
from player.Chrome import Play
from player.Chrome import Media_Stop


#
# Obtiene el nombre "canonico" de la fecha pasada desde la pagína web de los domincos
#
def get_title(fecha):
    
    url_domingo="https://www.dominicos.org/predicacion/homilia/%s/"
    url_diario="https://www.dominicos.org/predicacion/evangelio-del-dia/%s/"

    dia=fecha.strftime("%d-%m-%Y")
    falcon_logger.info("get_title %s" % dia)

    if (fecha.weekday() == 6): 
        url= url_domingo % dia
    else:
        url= url_diario % dia

    # print(url)
    r = rq.get(url)

    if (r.status_code != 200):
        return "Error al pedir la pagina. %s" % r.status_code 

    soup = BeautifulSoup(r.text, 'html.parser')
    scs=soup.find_all(name="script",type="application/ld+json")

    for s in scs:
        for t in s.contents: 
            j=json.loads(t,strict=False)
            if(j['@type']=="BreadcrumbList"):
                texto = j['itemListElement'][2]['item']['name']
                texto=texto.replace(", Año impar","")
                texto=texto.replace(", Año par","")
                texto=texto.replace("\r","")
                texto=texto.replace("\n","")
                return texto
    return("Error no encontado")

class StopStreaming:
    def on_get(self, req, resp):
        falcon_logger.info("StopStreaming 2.0")
        bid = req.get_param("bid", required=True)
        canal = req.get_param("canal", required=True)
        YT_SetPublic(bid,canal,"Private")
        Media_Stop()
        time.sleep(3)
        OV_Move_to_preset(0,"General")
        rc,msg=OBS_StopStreaming()
        rc,msg=YT_StopBroadcasting(bid,canal,"")

        datos = {
            'rc': rc,
            'msg': msg
        }
        falcon_logger.info("RC: %s MSG: %s" %(rc,msg))
        resp.media = datos


class Escena:
    def on_get(self, req, resp):
        scene = req.get_param("escena", required=False)
        falcon_logger.info("Cambia escena a: %s" % scene)
        rc,msg=OBS_Escena(scene)
        datos = {
            'rc': rc,
            'msg': msg,
            'Escena':  scene
        }
        falcon_logger.info("RC: %s MSG: %s" %(rc,msg))
        resp.media = datos

class Lista_Escenas:
    def on_get(self, req, resp):
        falcon_logger.info("Lista Escenas")
        rc,msg,lista_escenas=OBS_Lista_Escenas()
        datos = {
            'rc': rc,
            'msg': msg,
            'Escenas':  lista_escenas
        }
        falcon_logger.info("RC: %s MSG: %s" %(rc,msg))
        resp.media = datos

class StartStreaming:
    def on_get(self, req, resp):
        
        bid = req.get_param("bid", required=True)
        sid = req.get_param("sid", required=True)
        canal = req.get_param("canal", required=True)
          
        falcon_logger.info("StartStreaming bid:%s sid: %s" % (bid,sid))
        falcon_logger.info("Video URL: https://www.youtube.com/watch?v=%s" % bid)

        key,ingestion,stat=YT_Get_Stream_Data(sid,canal)
        falcon_logger.info("Streaming data OK")
        rc,msg =OBS_StartStreaming(key,ingestion)
        falcon_logger.info("Sttreaming Started")
        time.sleep(2)
        YT_SetPublic(bid,canal,"Public")
        falcon_logger.info("Canal en publico")
        datos = {
            'rc': rc,
            'msg': msg
        }
        falcon_logger.info("RC: %s MSG: %s" %(rc,msg))
        resp.media = datos

class Programa_Misa:
    def on_get(self, req, resp):
        
        fecha = req.get_param("fecha", required=True)
        canal = req.get_param("canal", required=False)
        titulo = req.get_param("titulo", required=False)
        privacidad = req.get_param("privacidad", required=False)
        auto = req.get_param("auto", required=False)
        falcon_logger.info("Programar Misa %s %s %s %s" % (canal,fecha,titulo,auto))
        if (privacidad is None):
            privacidad="private"
        if (canal is None):
            canal="Interno"
        if (canal =="SJC"):
            privacidad="public"
        try:
            fechad = datetime.strptime(fecha, '%Y-%m-%d %H:%M')
        except: 
            datos= {'rc':1,'msg':"Error en formato de fecha %s" % fecha } 
            falcon_logger.info("RC: %s MSG: %s" %(rc,msg))
            resp.media = datos
            return
        print("Fecha %s" % fecha)
        if (titulo==None):
            titulo= get_title(fechad)
            titulo="Santa Misa, %s, Parroquia San Juan Crisóstomo, Madrid, %s %s" % (titulo,fechad.strftime("%d-%m-%Y"),fechad.strftime("%H:%M"))
        rc,msg,streamId,nombre_stream,desc_stream,broadcast_id,key,published=YT_Programa_Misa(titulo,privacidad,fecha,"2pfs-12tx-yfyv-w8rh-dm72",canal,"",auto=auto)
        datos = {
            'rc': rc,
            'msg': msg,
            'titulo' : titulo,
            'emision' : fechad.strftime("%d-%m-%Y %H:%M"),
            'publicado_el': published, 
            'streamId': streamId,
            'nombre_stream': nombre_stream,
            'desc_stream': desc_stream,
            'broadcast_id': broadcast_id, 
            'key':key
        }
        falcon_logger.info("RC: %s MSG: %s" %(rc,msg))
        resp.media = datos

class StartBroadcast:
    def on_get(self, req, resp):
        bid = req.get_param("bid", required=True)
        canal = req.get_param("canal", required=True)
        sid = req.get_param("sid", required=True)
        stat = req.get_param("stat", required=True)
        falcon_logger.info("StartBroadcast: %s %s %s %s" %(canal,bid,sid,stat))

        key,addr,stat= YT_Get_Stream_Data(sid,canal)
        rc,msg=YT_StartBroadcasting(bid,canal,stat,"")
        datos = {
            'rc': rc,
            'msg': msg
        }
        falcon_logger.info("RC: %s MSG: %s" %(rc,msg))
        resp.media = datos

class StopBroadcast:
    def on_get(self, req, resp):
        
        bid = req.get_param("bid", required=True)
        canal = req.get_param("canal", required=True)
        falcon_logger.info("StopBroadcast: %s %s %s %s" %(canal,bid))
        rc,msg=YT_StopBroadcasting(bid,canal,"")
        datos = {
            'rc': rc,
            'msg': msg
        }
        falcon_logger.info("RC: %s MSG: %s" %(rc,msg))
        rc,msg=OV_Move_to_preset(0,"General")
        resp.media = datos

class GetTransmissions:

    def on_get(self, req, resp):
        falcon_logger.info("GetTransmissions")
        rc,msg,items=YT_Get_Transmisions()
        datos = {
            'rc': rc,
            'msg': msg,
            'items' : items
        }
        falcon_logger.info("RC: %s MSG: %s" %(rc,msg))
        resp.media = datos
 

class CamPreset:
    def on_get(self, req, resp):
        
        pos = req.get_param("pos", required=True)
        falcon_logger.info("CamPreset: Mover a %s" %(pos))
        datos = {
            'rc': 0,
            'msg': "Movido a %s" %pos
        }
        falcon_logger.info("RC: %s MSG: %s" %(rc,msg))
        resp.media = datos

class DeleteBroadcast:
    def on_get(self, req, resp):
        bid = req.get_param("bid", required=False)
        canal = req.get_param("canal", required=False)
        falcon_logger.info("DeleteBroadcast: %s %s" %(canal,bid))
        rc,msg=YT_DeleteBroadcast(bid,canal)
        
        datos = {
            'rc': rc,
            'msg': msg
        }
        falcon_logger.info("RC: %s MSG: %s" %(rc,msg))
        resp.media = datos

class Audio:
    def on_get(self, req, resp):
        estado = req.get_param("Estado", required=False)
        falcon_logger.info("Audio: Estado: %s" %(estado))
        MQTT_Audio(estado)

class Proyector:
    def on_get(self, req, resp):
        estado = req.get_param("Estado", required=False)
        falcon_logger.info("Proyector: Estado: %s" %(estado))
        MQTT_Proyector(estado)

class Sala:
    def on_get(self, req, resp):
        estado = req.get_param("Estado", required=False)
        falcon_logger.info("Proyector: Estado: %s" % estado)
        rc=9
        msg="Estado desconcido (%s) Tiene que ser ON o OFF" % estado 
        if (estado=="ON"): 
            MQTT_Audio("ON")            
            MQTT_Proyector("ON")
            rc=0
            msg="Sala Enecendida..."
        if (estado=="OFF"): 
            MQTT_Audio("OFF")            
            MQTT_Proyector("OFF")
            rc=0
            msg="Sala apagada..."
        datos = {
            'rc': rc,
            'msg': msg
        }
        falcon_logger.info("RC: 0 MSG: %s" % msg)
        resp.media = datos

class StartFireTV:
    def on_get(self, req, resp):
        bid = req.get_param("bid", required=False)
        Play(bid)



class Move_to_Preset:
    def on_get(self, req, resp):
        plano = req.get_param("plano", required=False)
        falcon_logger.info("Move_to_Preset: Mover a %s" %(plano))


        if plano in config.CAMARA.PLANOS:
            planod=config.CAMARA.PLANOS[plano]
            v=config.CAMARA.PLANOS[plano][0]
            escena=config.CAMARA.PLANOS[plano][1]
            rc,msg=OV_Move_to_preset(v,plano)
            rc,msg=OBS_Escena(escena) 
            """
            try:
                mycam = ONVIFCamera(config.CAMARA.HOST,config.CAMARA.PORT, config.CAMARA.USER,config.CAMARA.PASSWORD) 
                ptz = mycam.create_ptz_service()
                xx=ptz.GotoPreset({"ProfileToken": "MainStream", "PresetToken": v} )
                rc=0
                msg="Ok - Movida camara a %s %s " % (plano,v)
            
            except  Exception as e:
                falcon_logger.info("Error conexion a camara: %s" % str(e))
                rc=9
                msg="Error al conectar con camara %s " % str(e)

            
            """
        else:
            rc=8
            msg="No existe el preset %s" % plano 

        datos = {
            'rc': rc,
            'msg': msg
            }
        falcon_logger.info("RC: %s MSG: %s" %(rc,msg))
        resp.media = datos

class OARedir:
    def on_get(self, req, resp):
        state = req.get_param("state", required=False)
        code = req.get_param("code", required=False)
        rc,msg=YT_Code(state,code)
        datos = {
             'rc': rc,
             'msg': msg
        }
        falcon_logger.info("Code de canal %s terminado" % state)
        if (rc==0):
            resp.content_type="text/html"
            resp.body="<html><script> window.close()</script>Todo OK</html>"
            resp.status = falcon.HTTP_200
        else:
            resp.media = datos

class Get_Liturgical_Date:
    def on_get(self, req, resp):
        fecha = req.get_param("fecha", required=False)
        falcon_logger.info("Get_Liturgical_Date: Fecha: %s" % fecha)
        fechad = datetime.strptime(fecha, '%Y-%m-%d')
        titulo= get_title(fechad)
        datos = {
            'fecha': fecha.strftime("%d-%m-%Y"),
            'titulo': titulo
        }
        falcon_logger.info("RC: %s MSG: %s" %(rc,msg))
        resp.media = datos
#
#
#  Inicio del servidor REST
#
#


logging.basicConfig(level=logging.INFO)
logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)
logging.getLogger('googleapiclient.discovery').setLevel(logging.ERROR)


#OBS_SetCamUrl(config.OBS.CAM_URL)
#OBS_SetSyncOffset()
#YT_Init()
falcon_logger.info("Iniciando servicio v2.01")

api = falcon.API()
api.req_options.auto_parse_form_urlencoded=True
api.add_route("%s/LiturgicalDay" % config.SERVER.ROOT_PATH, Get_Liturgical_Date())
api.add_route("%s/StartStreaming" % config.SERVER.ROOT_PATH, StartStreaming())
api.add_route("%s/StopStreaming" % config.SERVER.ROOT_PATH, StopStreaming())
api.add_route("%s/Escena" % config.SERVER.ROOT_PATH, Escena())
api.add_route("%s/Lista_Escenas" % config.SERVER.ROOT_PATH, Lista_Escenas())
api.add_route("%s/Programa_Misa" % config.SERVER.ROOT_PATH, Programa_Misa())
api.add_route("%s/StartBroadcast" % config.SERVER.ROOT_PATH, StartBroadcast())
api.add_route("%s/StopBroadcast" % config.SERVER.ROOT_PATH, StopBroadcast())
api.add_route("%s/GetTransmissions" % config.SERVER.ROOT_PATH, GetTransmissions())
api.add_route("%s/CamPreset" % config.SERVER.ROOT_PATH, GetTransmissions())
api.add_route("%s/MovetoPreset" % config.SERVER.ROOT_PATH, Move_to_Preset())
api.add_route("%s/DeleteBroadcast" % config.SERVER.ROOT_PATH, DeleteBroadcast())
api.add_route("%s/StartFireTV" % config.SERVER.ROOT_PATH, StartFireTV())
api.add_route("%s/Sala" % config.SERVER.ROOT_PATH, Sala())
api.add_route("%s/Proyector" % config.SERVER.ROOT_PATH, Proyector())
api.add_route("%s/Audio" % config.SERVER.ROOT_PATH, Audio())
api.add_route("%s/OARedir" % config.SERVER.ROOT_PATH, OARedir())
