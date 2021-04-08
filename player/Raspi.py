import config
import logging
import subprocess
import youtube_dl
import os

logging.basicConfig(level=logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh = logging.FileHandler('%s' % config.SERVER.LOGFILE)
fh.setFormatter(formatter)
falcon_logger = logging.getLogger('gunicorn.error')


def Play(bid):
    falcon_logger.info("Raspi Player Enabled 1")
    url="https://youtu.be/%s" % bid 
    ydl_opts = {
        '-f': "best"
    }

    falcon_logger.info("Reproduciendo %s" % url)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            print("pido")
            out=ydl.extract_info(url,download=False)
            print("vuelvo")
        except Exception as ex:
            e=str(ex)
            print("Error ",e)
            if "ERROR:" in e:
                if "Private video" in e:
                    falcon_logger.info("%s es privado" % url )
                    return 9,"Video Privado"
                if "This live event will begin in" in e:
                    falcon_logger.info("No ha comenzado la emision")
                    return 8,"No ha comenzado la emisión"

                falcon_logger.info("----->Error")
                falcon_logger.info(str(e))

    form=out["formats"]
    x=0

    for f in form: 
        if x < f["width"]: 
            x=f["width"]
            best_url=f["url"]
#        print("Formato %s url  %s %s " % (f["format_id"],f["width"],f["height"]))
#        for k in f.keys():
#            print(k)
    falcon_logger.info("Video URL: %s" % best_url)
    cmd="ssh %s@%s 'pkill omxplayer; omxplayer -o hdmi %s ; /home/pi/fondo.sh' &" % (config.RASPI.USER,config.RASPI.HOST,best_url)
    
    os.system(cmd)
    falcon_logger.info("Comando enviado...")
