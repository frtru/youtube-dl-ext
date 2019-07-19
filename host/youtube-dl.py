from __future__ import unicode_literals

import struct
import sys
import threading
import queue
import os
import glob

import youtube_dl
try:
    import eyed3
    mp3library = eyed3
except ImportError:
    print
    mp3library = None

def get_info(video_url):
    return youtube_dl.YoutubeDL({}).extract_info(video_url, download=False)

def get_download_options(info):
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }
    if info['track'] != None:
        options['outtmpl'] = '%(track)s.%(ext)s'
    return options

def set_metadata(file_name, video_info):
    if mp3library != None:
        audiofile = mp3library.load(file_name)
        audiofile.tag.artist = video_info['artist']
        audiofile.tag.album = video_info['album']
        audiofile.tag.title = video_info['track']
        audiofile.tag.save()

def Main():
  # while(1):
  #   # Unpack message length as 4 byte integer.
  #   text_length = struct.unpack('i', text_length_bytes)[0]

  #   # Read the text (JSON object) of the message.
  #   text = sys.stdin.read(text_length).decode('utf-8')
  #   print(text)

    # TODO: Extract url from text
    video_url = 'https://www.youtube.com/watch?v=SFU1GeGFpzY'

    # Download video and set correct name
    info = get_info(video_url)
    options = get_download_options(info)
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_url])

    # Set artist in metadata of mp3 file    
    file_name = max(glob.iglob('*.[Mm][Pp]3'), key=os.path.getctime) # Latest mp3 file in folder
    set_metadata(file_name, info)

if __name__ == '__main__':
  Main()