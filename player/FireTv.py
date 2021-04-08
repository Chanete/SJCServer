import config
import logging
import os

logging.basicConfig(level=logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh = logging.FileHandler('%s' % config.SERVER.LOGFILE)
fh.setFormatter(formatter)
falcon_logger = logging.getLogger('gunicorn.error')


def Play(bid):
    falcon_logger.info("StartFireTv: BID %s" %(bid))
    rc=os.system("%s connect %s:5555" % (config.FIRE_TV.ADB_COMMAND,config.FIRE_TV.HOST))
    falcon_logger.info("FireTV CMD: Connect  RC: %s" % rc)

    rc=os.system("%s shell am force-stop org.videolan.vlc" % config.FIRE_TV.ADB_COMMAND)   
    falcon_logger.info("FireTV CMD: Stop Videolan  RC: %s" % rc)

    rc=os.system("%s shell input keyevent 3" % config.FIRE_TV.ADB_COMMAND)
    falcon_logger.info("FireTV CMD: Keyevent 3   RC: %s" % rc)

    cmd="%s shell am start -n org.videolan.vlc/org.videolan.vlc.gui.video.VideoPlayerActivity -e input-repeat 3 -a android.intent.action.VIEW -d  'https://youtu.be/%s'"  % (config.FIRE_TV.ADB_COMMAND, bid)
    rc=os.system(cmd)
    falcon_logger.info("FireTV CMD: %s  RC: %s" % (cmd,rc))