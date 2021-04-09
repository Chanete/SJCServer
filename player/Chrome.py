import config
import argparse
import logging
import sys
import zeroconf
import sys
import pychromecast
from pychromecast.controllers.youtube import YouTubeController
import logging 
import time

logging.basicConfig(level=logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh = logging.FileHandler('%s' % config.SERVER.LOGFILE)
fh.setFormatter(formatter)
falcon_logger = logging.getLogger('gunicorn.error')


def Play(bid):

    falcon_logger.info("Arrancando Chromecast BID %s" %(bid))
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[config.CHROMECAST.NAME])

    if not chromecasts:
        msg="No encuentro el chromecast con nombre %s" % config.CHROMECAST.NAME
        falcon_logger.info(msg)
        return 9,msg

    browser.stop_discovery()
    cast = chromecasts[0]
#    print(cast)
    cast.wait()
    mc = cast.media_controller
    falcon_logger.info("Arrancando Youtube Controller")
    yt = YouTubeController()
    cast.register_handler(yt)
    retry=6
    while (retry):
        yt.play_video(bid)
        if (mc.status.player_is_playing):
            break
        falcon_logger.info("No arranca, espero")
        time.sleep(2)
        retry-=1

    falcon_logger.info("Chromecast Terminado")

def Media_Stop():
    falcon_logger.info("Parando Cast")
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[config.CHROMECAST.NAME])

    if not chromecasts:
        msg="No encuentro el chromecast con nombre %s" % config.CHROMECAST.NAME
        falcon_logger.info(msg)
        return 9,msg

    cast = chromecasts[0]
    cast.wait()
    mc = cast.media_controller
    falcon_logger.info("Arrancando Stadnby")
    yt = YouTubeController()
    cast.register_handler(yt)
    retry=6
    while (retry):
        yt.play_video("9m6bfFWPIVE")
        if (mc.status.player_is_playing):
            break
        falcon_logger.info("No arranca, espero")
        time.sleep(2)
        retry-=1

    