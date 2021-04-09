import argparse
import logging
import sys
import zeroconf
import sys
import pychromecast
from pychromecast.controllers.youtube import YouTubeController

#logging.basicConfig(level=logging.DEBUG)
CAST_NAME = "Salón grande"

# Change to the video id of the YouTube video
# video id is the last part of the url http://youtube.com/watch?v=video_id
VIDEO_ID = "dQw4w9WgXcQ"

VIDEO_ID="8Zuav_UKCig"

print("i")
chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[CAST_NAME])
print("o")
if not chromecasts:
    print('No chromecast with name %s iscovered' % CAST_NAME)
    sys.exit(1)
browser.stop_discovery()
cast = chromecasts[0]
print(cast)
# Start socket client's worker thread and wait for initial status update
cast.wait()
print("Creo")
yt = YouTubeController()
print("handler")
cast.register_handler(yt)
print("Play")
yt.play_video(VIDEO_ID)
print("fin")