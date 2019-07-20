import struct
import sys
import threading
import queue
import json
import os
import shutil
import glob
import time
import datetime
import logging
import re
import contextlib

def supress_stdout(func):
    def wrapper(*a, **ka):
        with open(os.devnull, 'w') as devnull:
            with contextlib.redirect_stdout(devnull):
                func(*a, **ka)
    return wrapper

# Logger configuration
logger = logging.getLogger('youtube-dl-ext')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("../logs/" + re.sub('-|:| ', '_', str(datetime.datetime.now())) + ".log")
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

import youtube_dl
try:
    import eyed3
except ImportError:
    logger.warning('eyed3 couldn\'t be imported. Won\'t be able to add metadata to files.')

    
if sys.platform == "win32":
    import msvcrt
    msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)


def get_info(video_url):
    return youtube_dl.YoutubeDL({}).extract_info(video_url, download=False)

def get_download_options(info):
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'logger': logger
    }
    if info['track'] != None:
        options['outtmpl'] = '%(track)s.%(ext)s'
    return options

def set_metadata(file_name, video_info):
    if eyed3 != None:
        audiofile = eyed3.load(file_name)
        audiofile.tag.artist = video_info['artist']
        audiofile.tag.album = video_info['album']
        audiofile.tag.title = video_info['track']
        audiofile.tag.save()

def process_request():
    try:
        # Read the message length (first 4 bytes).
        text_length_bytes = sys.stdin.read(4)

        # Unpack message length as 4 byte integer.
        text_length = struct.unpack('i', bytes(text_length_bytes, 'utf-8'))[0]

        # Read the text (JSON object) of the message.
        text = sys.stdin.read(text_length)
        
        #TODO: convert text JSON format to URL string
        json_text = json.loads(text)
        
        # Return the URL
        return str(json_text["text"])
    except Exception as e:
        logger.error(str(e))
        
@supress_stdout
def launch(video_url):
    # Download video and set correct name
    logger.info("Launching process on url : " + video_url)
    info = get_info(video_url)
    
    options = get_download_options(info)
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_url])

    # Set artist in metadata of mp3 file    
    file_name = max(glob.iglob('*.[Mm][Pp]3'), key=os.path.getctime) # Latest mp3 file in folder
    set_metadata(file_name, info)

    # Move file to output folder
    shutil.move(file_name, "E:/music/" + file_name)

# Helper function that sends a message to the webapp.
def send_message(message):
    text = unicode('{"text": "' + message + '"}', "utf-8")
    # Write message size.
    sys.stdout.write(struct.pack('I', len(text))) # TODO: Fix issue here
    # Write the message itself.
    sys.stdout.write(text)
    sys.stdout.flush()

def Main():
    # Wait for message from chrome extension
    video_url = str(process_request())
    # Launch process on queue content
    launch(video_url)

if __name__ == '__main__':
  Main()