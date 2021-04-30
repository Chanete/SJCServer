#!/usr/bin/python3
import config
import httplib2
import os
import sys
import time
import arrow
from datetime import datetime
from datetime import timedelta
from dateutil import tz

import requests
from bs4 import BeautifulSoup
import json
import zulu


from chrome.Logon import auth
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import Credentials
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
from dateutil.parser import * 
#from google_auth_oauthlib.flow import InstalledAppFlow

import logging
#from dateutil import parser  

#Cargar datos de usuario
with open(config.YT.SECRETS) as json_file:
    oa_data = json.load(json_file)
redirect_uri=oa_data["web"]["redirect_uris"][0]


falcon_logger = logging.getLogger('gunicorn.error')

# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets


# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("\r", ""),
        ("\n", ""),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s


class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    
def YT_Code(canal,code):
      falcon_logger.error("Recibido codigo %s del canal %s " % (code,canal))
      rc=0
      msg="OK"
      falcon_logger.error("Creando flow")
      flow= OAuth2WebServerFlow(client_id=oa_data["web"]["client_id"],
              client_secret=oa_data["web"]["client_secret"],
              scope =YOUTUBE_READ_WRITE_SCOPE,
              redirect_uri=redirect_uri,
              state=canal,
              login_hint=config.YT.CANALES[canal][0])
      falcon_logger.error("Flow: Step 2. Solicitud de token")    
      credentials=flow.step2_exchange(code=code)
      falcon_logger.error("Token OK, guardando fichero.")
      storage = Storage(config.YT.STORAGE % canal)
      credentials = storage.put(credentials) 
      falcon_logger.error("Proceso terminado. Credenciales guardadas.")
      return rc,msg

def get_authenticated_service(canal,args):
  logging.basicConfig(level=logging.INFO)
  logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)
  logging.getLogger('googleapiclient.discovery').setLevel(logging.ERROR)
  
  falcon_logger.info("Abriendo canal %s" %canal) 
  storage = Storage(config.YT.STORAGE % canal)
  credentials = storage.get() 
  
  if credentials is None or credentials.invalid:
      falcon_logger.error("Credenciales de %s incorrectas. Gestionando renovación. V2" % canal)
      flow= OAuth2WebServerFlow(client_id=oa_data["web"]["client_id"],
              client_secret=oa_data["web"]["client_secret"],
              scope =YOUTUBE_READ_WRITE_SCOPE,
              redirect_uri=redirect_uri,
              state=canal,
              login_hint=config.YT.CANALES[canal][0],
              prompt="consent ")
      falcon_logger.info(flow.step1_get_authorize_url()) 
#      auth(flow.step1_get_authorize_url(),canal)
      return 99,flow.step1_get_authorize_url()
      falcon_logger.info("Flow terminado. Espero 2s para recargar credenciales...")
      time.sleep(2)
      credentials = storage.get() 


  try:
      http_check=credentials.authorize(httplib2.Http())
      chk=credentials.refresh(http_check)
  except: 
    falcon_logger.error("Error de credenciales. Inicio flujo Autj")
    flow= OAuth2WebServerFlow(client_id=oa_data["web"]["client_id"],
            client_secret=oa_data["web"]["client_secret"],
            scope =YOUTUBE_READ_WRITE_SCOPE,
            redirect_uri=redirect_uri,
            state=canal,
            login_hint=config.YT.CANALES[canal][0],
            prompt="consent ")
    falcon_logger.info(flow.step1_get_authorize_url()) 
#    auth(flow.step1_get_authorize_url(),canal)



  return 0,build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,cache_discovery=False,
    http=http_check)


def Conecta_Canal(canal,args):
      rc,yt=get_authenticated_service(canal,args) 
      if (rc==99):
            msg=yt
            yt=None
            falcon_logger.info("Error en conexion  al canal %s. URL: %s" % (canal,msg) )
      else:
        falcon_logger.info("Canal %s conectado." % canal )
        msg="OK"
      return rc,msg,yt

# Create a liveBroadcast resource and set its title, scheduled start time,
# scheduled end time, and privacy status.
def insert_broadcast(youtube, titulo,inicio, fin,privacidad,auto=""):

  falcon_logger.info("Insert Broadcast: %s Fin: %s" % (inicio,fin))
  insert_broadcast_response = youtube.liveBroadcasts().insert(
    part="snippet,status,contentDetails",
    body=dict(
      snippet=dict(
        title=titulo,
        scheduledStartTime=inicio,
        scheduledEndTime=fin,
        description=auto
      ),
      status=dict(  
        privacyStatus=privacidad,
        selfDeclaredMadeForKids="no"
      ),
      contentDetails=dict(
                    enableAutoStart=True,
                    latencyPreference ="ultraLow",
       ),
    )
  ).execute()
  
  snippet = insert_broadcast_response["snippet"]

  falcon_logger.info( "Broadcast '%s' with title '%s' was published at '%s'." % (
    insert_broadcast_response["id"], snippet["title"], snippet["publishedAt"]))
  return insert_broadcast_response["id"],snippet["publishedAt"]

# Create a liveStream resource and set its title, format, and ingestion type.
# This resource describes the content that you are transmitting to YouTube.
def insert_stream(youtube, stream_title):
  insert_stream_response = youtube.liveStreams().insert(
    part="snippet,cdn",
    body=dict(
      snippet=dict(
        title=stream_title
      ),
      cdn=dict(
        ingestionType="rtmp",
        resolution="variable",
        frameRate="variable"
      )
    )
  ).execute()
  snippet = insert_stream_response["snippet"]




  falcon_logger.info( "Stream '%s' with title '%s' was inserted." % (
    insert_stream_response["id"], snippet["title"]))
  return 0,"OK",insert_stream_response["id"],snippet["title"],snippet["description"]


def YT_SetPublic( bid,canal,privacy="Public"):
    rc,msg,youtube = Conecta_Canal(canal,"")
    bdy = dict(
                  status=dict(
                      privacyStatus=privacy,
                      selfDeclaredMadeForKids="no"
                  ),
                id=bid 
              )  

    try:
      falcon_logger.info(bdy)
      request = youtube.liveBroadcasts().update(part="status",body=bdy)
      response = request.execute()
      falcon_logger.info("Canal  %s puesto en %s " % (canal,privacy) )
    except HttpError as e:
      err_data=json.loads(e.content)
      msg=err_data["error"]["message"]
      falcon_logger.info("SetPublic Error: %s" % msg )





  # Create a liveStream resource and set its title, format, and ingestion type.
# This resource describes the content that you are transmitting to YouTube.
def update_stream(youtube, id,key):
    request = youtube.liveStreams().update(
        part="snippet,cdn",
        body={
          "cdn": {
            "ingestionInfo": {
              "streamName": "%s" % key
            }
          },
          "id": "%s" % id,
          "snippet": {
            "title": "Updated streamy stream title",
            "description": "This stream is like a cold, swiftly flowing mountain stream, but with video instead of cold, swiftly flowing water."
          }
        }
    )
    response = request.execute()


# Call the API's thumbnails.set method to upload the thumbnail image and
# associate it with the appropriate video.
def upload_thumbnail(youtube, video_id, file):
  youtube.thumbnails().set(
    videoId=video_id,
    media_body=file
  ).execute()


def get_streamid_data(youtube,sid):
      
  falcon_logger.info("get data SID %s " %sid)    
  request = youtube.liveStreams().list(
        part="cdn,status",
        id=sid
  )
  response = request.execute()

  try:
    stat=response["items"][0]["status"]["streamStatus"]

  except:
    stat="No hay"
  falcon_logger.info("Stat %s" % stat)


  items=response["items"][0]["cdn"]["ingestionInfo"]

#  falcon_logger.info(sid,items["streamName"],items["ingestionAddress"])
  return items["streamName"],items["ingestionAddress"],stat




def get_streamid(youtube,texto):
  request = youtube.liveStreams().list(
        part="snippet,cdn,contentDetails,status",
        mine=True
  )
  response = request.execute()
  items=response["items"]
  streamId=""
  for k in items:
    streamId=k["id"]
    title=k["snippet"]["title"]
    desc=k["snippet"]["description"]

    if (title.startswith(texto)):
      falcon_logger.info("Encontrado Stream: %s %s %s\n" % (streamId,title,desc) )
      return(0,"OK",streamId,title,desc)

  if (streamId==""):
    falcon_logger.info("No hay stream (*AUTO*)")
    return(1,"No hay stream *AUTO*)","Error","Error")
  return 0,"OK",streamId,title,desc





# Delete Broadcast
def delete_broadcast(youtube, broadcast_id ):
      
  try:
    youtube.liveBroadcasts().delete(
      id=broadcast_id
    ).execute()
  except HttpError as e:
    err_data=json.loads(e.content)
    msg=err_data["error"]["message"]
    falcon_logger.info("get err %s" % msg )
    if (msg=="Live broadcast not found"):
          return 9, "Emision no encontrada (%s)"  % broadcast_id
    return 1, "Error en Peticion Youtube (%s) %s" % (e.resp.status, json.dumps(err_data, indent=4, sort_keys=True))
  return 0,"Ok"


def YT_DeleteBroadcast(bid,canal):
    rc,msg,youtube = Conecta_Canal(canal,"")   # Conecta y autentica el API de Google
    rc,msg = delete_broadcast(youtube,bid)
    return rc,msg 


# Bind the broadcast to the video stream. By doing so, you link the video that
# you will transmit to YouTube to the broadcast that the video is for.
def bind_broadcast(youtube, broadcast_id, stream_id):
  bind_broadcast_response = youtube.liveBroadcasts().bind(
    part="id,contentDetails",
    id=broadcast_id,
    streamId=stream_id
  ).execute()

  falcon_logger.info ("Broadcast '%s' was bound to stream '%s'." % (
    bind_broadcast_response["id"],
    bind_broadcast_response["contentDetails"]["boundStreamId"]))
  return     bind_broadcast_response["contentDetails"]["boundStreamId"] 


def YT_Get_Stream_Data(sid,canal):
    rc,msg,youtube = Conecta_Canal(canal,"")   # Conecta y autentica el API de Google
    key,addr,stat=get_streamid_data(youtube,sid)
    falcon_logger.info("Returninf from YT_Get_Stream_Data")
    return key,addr,stat

def utc2local(utc):
    epoch = time.mktime(utc.timetuple())
    offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
    return utc + offset

def load_list(items,resp,youtube,canal):
  for k in items:
    bid=k["id"]
    sid=k["contentDetails"]["boundStreamId"]
#    key,addr=get_streamid_data(youtube,sid)
    key="xx"
    addr="xx"
    title=k["snippet"]["title"]
    desc=k["snippet"]["description"]
    pub=k["snippet"]["publishedAt"]
    try:
      sched=k["snippet"]["scheduledStartTime"]
      sdate=zulu.parse(sched,default_tz ='UTC') 
      sched=utc2local(sdate.naive)
#    sdate= parser.parse(sched)
      schedt=sched.strftime("%Y-%m-%d %H:%M")
      print(schedt)
    except: 
      schedt="Error fecha"  
    stat=(k["status"]["lifeCycleStatus"])
    print()
    resp.append({"broadcast_id":bid,"titulo":title,"desc":desc,"Fecha_pub":pub,"Fecha_Sched":schedt,"Canal":canal,"streamId":sid,"key":key,"ingestionAddr":addr,"status":stat})


def YT_Get_Transmisions():
  falcon_logger.info("Get Transmisions")
  resp=list()
  rc,msg,youtube = Conecta_Canal("Interno","")   # Conecta y autentica el API de Google
  if (rc==99):
        falcon_logger.info("Peticion de transmisiones cancelada")
        return rc,msg,[]
  rc,msg,items = Get_Transmisions(youtube)
  load_list(items,resp,youtube,"Interno")
  rc,msg,items = Get_Transmisions(youtube,tipo="active")
  load_list(items,resp,youtube,"Interno")

  rc,msg,youtube = Conecta_Canal("SJC","")   # Conecta y autentica el API de Google
  if (rc==99):
        falcon_logger.info("Peticion de transmisiones cancelada")
        return rc,msg,[]

  rc,msg,items = Get_Transmisions(youtube)
  load_list(items,resp,youtube,"SJC")

  rc,msg,items = Get_Transmisions(youtube,tipo="active")
  load_list(items,resp,youtube,"SJC")
  falcon_logger.info("Peticion de transmisiones completada")
  return rc,msg,resp
        

def Get_Transmisions(youtube,tipo="upcoming"):


  pageToken=1                                   # Pueden ser varias paginas y hay que llamar varias veces.
  items= list()
  while(pageToken):
    if (pageToken==1):                          # Si es la primera página, no poner next-token
      falcon_logger.info("Solicitando lista de transmisiones a YouTube")
      request = youtube.liveBroadcasts().list(
                part="snippet,contentDetails,status",
                broadcastStatus=tipo
      )
    else:                                       # Es una segunda llamaad-> añadir token 
      request = youtube.liveBroadcasts().list(
          part="snippet,contentDetails,status",
          pageToken=pageToken,
          broadcastStatus=tipo
      )


    response = request.execute()                # Ejecutar la peticióm

    if 'nextPageToken' in response.keys():      # ver en la respuesta si hay mas pagina y preparar futuras llamadas
          pageToken=response["nextPageToken"]
    else:
          pageToken=0

    items.extend(response["items"])
    for i in items:
      falcon_logger.info("--- %s %s ---" % ( i["snippet"]["title"],i["id"]))

  return 0,"OK",items


def hay_conflicto(youtube,f_inicio):
 # Busco todos los eventos upcoming por si hay conflicto (ya esta programado)
  rc,msg,items=Get_Transmisions(youtube)
#  falcon_logger.info(f_inicio)
  for k in items:
    vid=k["id"]
    title=k["snippet"]["title"]
    desc=k["snippet"]["description"]
    pub=k["snippet"]["publishedAt"]
    sched=k["snippet"]["scheduledStartTime"]

    f_sched = datetime. strptime(sched, '%Y-%m-%dT%H:%M:%SZ')
    dif=abs((f_sched-f_inicio).total_seconds())
#    falcon_logger.info("Title: %s Sched: %s dif %s" % (title,sched,dif))
    if (dif < 600):
          falcon_logger.info("%s %s %s %s %s" % (vid,title,desc,pub,sched))
          falcon_logger.info("Hay un evento (%s) programado que entra en conflicto con este. Esta programado a las %s" %(title,sched))
          return 1
  #  falcon_logger.info("%s %s %s %s %s" % (vid,title,desc,pub,sched))
  return 0
    

def get_title(fecha):
    url_domingo="https://www.dominicos.org/predicacion/homilia/%s/"
    url_diario="https://www.dominicos.org/predicacion/evangelio-del-dia/%s/"

    dia=fecha.strftime("%d-%m-%Y")

    if (fecha.weekday() == 6): 
        url= url_domingo % dia
    else:
        url= url_diario % dia

    falcon_logger.info(url)
    r = requests.get(url)

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
                return texto
    return("Error no encontado")
#
#  Iniciar transmision YT
#
def YT_StartBroadcasting(broadcastid,canal,stat,args):
  rc,msg,youtube = Conecta_Canal(canal,args)   # Conecta y autentica el API de Google
  request = youtube.liveBroadcasts().transition(
  broadcastStatus="live",
  id=broadcastid,
  part="snippet,status"
  )
  try: 
    response = request.execute()
  except HttpError as e:
    falcon_logger.info("ENtro error")
    err_data=json.loads(e.content)
    falcon_logger.info("load err")
    msg=err_data["error"]["message"]
    falcon_logger.info("get err %s" % msg )
    if (msg=="Stream is inactive"):
          falcon_logger.info("Salgo por error")
          return 2,"Streaming inactivo"
    if (msg=="Invalid transition"):
          falcon_logger.info("Transicion Erronea")
          return 2,"Transicion erronea"
    if (msg=="redundantTransition"):
          falcon_logger.info("Redundant")
          return 2,"Ya esta en emision"
          
    falcon_logger.info("Error:",err_data["error"]["message"])
    return 1, "Error en Peticion Youtube (%s) %s" % (e.resp.status, json.dumps(err_data, indent=4, sort_keys=True))
  return 0,"Ok"


def YT_StopBroadcasting(broadcastid,canal,args):
      
  rc,msg,youtube = Conecta_Canal(canal,args)   # Conecta y autentica el API de Google
  request = youtube.liveBroadcasts().transition(
    broadcastStatus="complete",
    id=broadcastid,
    part="snippet,status"
    )
  try: 
    response = request.execute()
  except HttpError as e:
    err_data=json.loads(e.content)
    return 1, "Error en Peticion Youtube (%s) %s" % (e.resp.status, json.dumps(err_data, indent=4, sort_keys=True))
  return 0,"Ok"
#
#
#
def YT_Programa_Misa(titulo,privacidad,inicio,key,canal,args,auto=""):

  logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)
  logging.getLogger('googleapiclient.discovery').setLevel(logging.ERROR)
  falcon_logger.info("%s - %s - %s - %s - %s" % (titulo,privacidad,inicio,key,canal))
  try:
#     f_inicio = datetime. strptime(inicio, '%Y-%m-%d %H:%M')   # Validar que es una fecha correcta.
     f_inicio = parse(inicio)
  except ValueError:
    msg= "La fecha de inicio es incorrecta: (%s)\n" % inicio
    return 1,msg,"","","","","",""

#  inicio=f_inicio-timedelta(minutes=5)    # Inicio real de la grabacion 5 minutos antes.
  inicio=f_inicio                         # Inicio real de la grabacion sin adelantos. 
  fin=inicio+timedelta(minutes=60)        # Fin real de la grabacion un hora despues de inicio

  if (inicio < datetime.now()):           # Si el inicio es anterior a ahora, no continuar. 
        msg="Hora de inicio incorrecta. No se puede programar con menos de 5 minutos de adeanto. "
        return 2,msg,"","","","","","" 

  rc,msg,youtube = Conecta_Canal(canal, "")   # Conecta y autentica el API de Google

  falcon_logger.info("Chk conf rc: %s" % rc)

  if (rc != 0):
        falcon_logger.info ("%s %s" %(rc,msg))
        return rc,msg,"","","","","",""

#  os.system("whoami")
  if (hay_conflicto(youtube,f_inicio)):       # Ver si hay algo mas programado a esa hora. 
      return 3,"Hay otra emision en conflicto","","","","","",""  

  if len(titulo) > 97: 
    titulo = (titulo[:97] + '...') 
  titulo=normalize(titulo)                                        # Quitar Tildes
  falcon_logger.info("Todo correcto, programando evento YouTube\b")
  falcon_logger.info("El titulo de la emision es: %s \n" % titulo )
  falcon_logger.info("Hora de inicio solicitada: %s Inicio real: %s \n" % (f_inicio,inicio))
  falcon_logger.info("Hora fin: %s \n" % fin)
  falcon_logger.info("El evento es %s\n" % privacidad)
  falcon_logger.info("La clave de emision es: %s\n" % key)
  
  #
  # Generar Evento. 
  #

  try: 
    displace=1+time.localtime().tm_isdst
    displace=displace*-1
    falcon_logger.info("Creando Broadcast")
    arr_inicio=arrow.get(inicio.strftime("%Y-%m-%dT%H:%M:00"))
    arr_inicio.replace(tzinfo='GMT-1') 
    arr_fin=arrow.get(fin.strftime("%Y-%m-%dT%H:%M:00"))
    arr_fin.replace(tzinfo='GMT-1')
    arr_inicio=arr_inicio.shift(hours=displace)
    arr_fin=arr_fin.shift(hours=displace)
    print(arr_inicio,arr_fin)
#    broadcast_id,published = insert_broadcast(youtube, titulo,inicio.strftime("%Y-%m-%dT%H:%M:00 %Z"),fin.strftime("%Y-%m-%dT%H:%M:00 %Z"),privacidad,auto=auto)
    broadcast_id,published = insert_broadcast(youtube, titulo,arr_inicio.isoformat(),arr_fin.isoformat(),privacidad,auto=auto)
    falcon_logger.info("Obteniendo Stream")
#   rc,msg,streamId,nombre_stream,desc_stream=get_streamid(youtube,"(*AUTO*)")
    rc,msg,streamId,nombre_stream,desc_stream=insert_stream(youtube,"(S)%s" % broadcast_id) 

#    falcon_logger.info("Creando THumb")
#    upload_thumbnail(youtube,broadcast_id,"/home/sjc/misas/Virgen.jpg")
#    falcon_logger.info("Actulizando  Stream")
#    update_stream(youtube, streamId,key)
    falcon_logger.info("Binding")
    bind_broadcast(youtube, broadcast_id, streamId)
  except HttpError as e:
    err_data=json.loads(e.content)
    return 1, "Error en Peticion Youtube %s (%s)" % (e.resp.status, json.dumps(err_data, indent=4, sort_keys=True)),"","","","","",""
  return 0,"ok",streamId,nombre_stream,desc_stream,broadcast_id,key,published


#
#
#
#    MAIN
#
#
#

if __name__ == "__main__":
      
# Definir los argumentos que recibie el programa      
  argparser.add_argument("--titulo", help="Titulo de la emision",    default="Emisión San Juan Crisostomo")
  argparser.add_argument("--privacidad", help="Privacidad (public o private)",    default="private")
  argparser.add_argument("--inicio", help="Hora de inicio", required=True)
  argparser.add_argument("--canal", help="Canal de emision (Interno o SJC)", required=True)
  args = argparser.parse_args()
  key="2pfs-12tx-yfyv-w8rh-dm72"    # Definir clave de emision

  f_inicio = datetime. strptime(args.inicio, '%Y-%m-%d %H:%M')   # Validar que es una fecha correcta.
  inicio=f_inicio-timedelta(minutes=5)
  canal=args.canal
  if (args.titulo=="Emisión San Juan Crisostomo"):    # Ver si nos han pasado un titulo especifico
        falcon_logger.info("NO hay titulo, voy a buscar el del dia. ") # Si no, ir a la web de los Agustinos para ver el nombre del dia. 
        titulo="Santa Misa, %s, Parroquia San Juan Crisóstomo, Madrid, %s" % (get_title(inicio),inicio.strftime("%d-%m-%Y"))
        titulo=titulo.replace("\r","")
        titulo=titulo.replace("\n","")
  else:
        titulo=args.titulo
  

  YT_Programa_Misa(titulo,args.privacidad,args.inicio,key,canal,"")

  
