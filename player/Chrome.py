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

