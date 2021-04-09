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

devices, browser = pychromecast.discovery.discover_chromecasts()
# Shut down discovery
browser.stop_discovery()

print(f"Discovered {len(devices)} device(s):")

for device in devices:
    if device.friendly_name == CAST_NAME:
        cast=device
    print(f"  {device}")

chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[args.cast])
if not chromecasts:
    print('No chromecast with name "{}" discovered'.format(args.cast))
    sys.exit(1)

cast = chromecasts[0]
print(cast)
# Start socket client's worker thread and wait for initial status update
cast.wait()

yt = YouTubeController()
cast.register_handler(yt)
yt.play_video(VIDEO_ID)

# Shut down discovery
browser.stop_discovery()