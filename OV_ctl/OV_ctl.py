#
#  onvif - Modulo de control ONVIF de la camara
#
from onvif import ONVIFCamera
import config
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)
logging.getLogger('googleapiclient.discovery').setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('%s' % config.SERVER.LOGFILE)
fh.setFormatter(formatter)
falcon_logger = logging.getLogger('gunicorn.error')

falcon_logger.addHandler(fh)

def OV_Move_to_preset(preset,plano):
    falcon_logger.info("Move to Preset %s - %s " % (preset,plano))
    try:
        mycam = ONVIFCamera(config.CAMARA.HOST,config.CAMARA.PORT, config.CAMARA.USER,config.CAMARA.PASSWORD) 
        ptz = mycam.create_ptz_service()
        ptz.GotoPreset({"ProfileToken": "MainStream", "PresetToken": preset} )
        rc=0
        msg="Ok - Camara movida a %s %s " % (preset,plano)
    
    except  Exception as e:
        rc=9
        msg="Error al conectar con camara %s " % str(e)
    falcon_logger.info("RC: %s - %s " % (rc,msg))
    return rc,msg
