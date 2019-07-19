from __future__ import unicode_literals

import struct
import sys
import threading
import queue

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

def Main():
  # while(1):
  #   # Unpack message length as 4 byte integer.
  #   text_length = struct.unpack('i', text_length_bytes)[0]

  #   # Read the text (JSON object) of the message.
  #   text = sys.stdin.read(text_length).decode('utf-8')
  #   print(text)

    # TODO: Extract url from text
    video_url = 'https://www.youtube.com/watch?v=nCBASt507WA'

    # Download video and set correct name
    info = get_info(video_url)
    options = get_download_options(info)

    print('yes')
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_url])

    # Set artist in metadata of mp3 file
    if mp3library != None:
        mp3library.load()

if __name__ == '__main__':
  Main()