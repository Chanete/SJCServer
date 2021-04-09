class SERVER:
    PORT = 8000
    IP = "192.168.1.248"
    LOGFILE = '/var/log/SJCServer/SJCServer.log'
    DATABASE_TABLES = ['tb_users', 'tb_groups']
    ROOT_PATH = '/SJC'

class MQTT:
    HOST = "localhost"
    PORT = 1836
    AUDIO_TOPIC = "cmnd/power/audio"
    VIDEO_TOPIC ="broadlink/record"

class YT:
    STORAGE = "/home/sjc/SJCServer/creds/%s-oauth2.json"
    SECRETS ="/home/sjc/SJCServer/creds/client_secrets.json"
    CANALES = {"SJC":["externoSjc@gmail.com","2de01ad4"],
               "Interno":["internoSjc@gmail.com","2de01ad4"]}
#    CANALES = {"SJC":["parroquiasjc.yt@gmail.com","SJC@2de01ad4"],
#               "Interno":["misadiarosjc@gmail.com","SJCDiario"]}

class OBS:
    HOST = "localhost"
    PORT = 4444
    PASSWORD = "secret"
    CAM_URL = "rtsp://192.168.1.110:554/1/h264major"
    SOURCE_TYPE = "vlc_source"
    SOURCE_NAME = "Fuente de vídeo VLC"
    AUDIO_SOURCE = "Mic/Aux"
    AUDIO_SYNC = 1000 
    IMAGEN_COMUNION = "/home/sjc/tst/APP/resources/Comunion_obs.jpeg"

class FIRE_TV:
    HOST = "192.168.1.95"
    ADB_COMMAND = "adb"

class RASPI:
    HOST = "192.168.1.109"
    USER = "pi"


class CAMARA:
    HOST="192.168.1.110" 
    PORT=8999
    USER="admin"
    PASSWORD=""
    PLANOS={"General":  [1,"Escena"],
            "Altar":    [2,"Escena"],
            "Virgen":   [3,"Escena"],
            "Puertas":  [4,"Escena"],
            "Gral_Corto": [5,"Escena"],
            "Ninio":    [6,"Escena"],
            "Comunion": [7,"Comunion"]
            }   
