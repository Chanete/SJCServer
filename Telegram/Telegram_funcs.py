#!/usr/bin/python3
# Version V0
import sys
sys.path.append('/home/sjc/SJCServer')
import config
from  telegram_send import send as Telegram_send
import logging
logging.basicConfig(level=logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh = logging.FileHandler('%s' % config.SERVER.LOGFILE)
fh.setFormatter(formatter)
falcon_logger = logging.getLogger('gunicorn.error')
falcon_logger.addHandler(fh)


def TG_Send(messages): 

    try:
        Telegram_send(messages=messages)
    except Exception as ex:
        e=str(ex)
        falcon_logger.error("Error %s al enviar el mensaje Telegram" % e)