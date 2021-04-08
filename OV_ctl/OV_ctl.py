#
#  onvif - Modulo de control ONVIF de la camara
#
from onvif import ONVIFCamera
import config

def OV_Move_to_preset(preset,plano):
    try:
        mycam = ONVIFCamera(config.CAMARA.HOST,config.CAMARA.PORT, config.CAMARA.USER,config.CAMARA.PASSWORD) 
        ptz = mycam.create_ptz_service()
        ptz.GotoPreset({"ProfileToken": "MainStream", "PresetToken": preset} )
        rc=0
        msg="Ok - Camara movida a %s %s " % (preset,plano)
    
    except  Exception as e:
        rc=9
        msg="Error al conectar con camara %s " % str(e)
    return rc,msg
