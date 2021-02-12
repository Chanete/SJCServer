class SERVER:
    PORT = 8000
    LOGFILE = '/var/log/SJC_Server/SJC_Server.log'
    DATABASE_TABLES = ['tb_users', 'tb_groups']
    ROOT_PATH = '/SJC'

class MQTT:
    HOST = "192.168.1.246"
    PORT = 1836
    AUDIO_TOPIC = "cmnd/power/audio"
    VIDEO_TOPIC ="broadlink/record"

class YT:
    STORAGE = "/home/chano/SJC/%s-oauth2_ARO.json"
    SECRETS ="/home/chano/SJC/client_secret_ARO.json"

class OBS:
    HOST = "localhost"
    PORT = 4444
    PASSWORD = "secret"

class FIRE_TV:
    HOST = "192.168.1.95"
    ADB_COMMAND = "adb"

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
