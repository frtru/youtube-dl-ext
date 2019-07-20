import struct
import sys
#import threading
#import queue
import json
import os
import shutil
import glob
import time

import youtube_dl
try:
    import eyed3
    mp3library = eyed3
except ImportError:
    print
    mp3library = None

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

def process_request():
    with open("log.txt", "a") as myfile:

      try:
          # Read the message length (first 4 bytes).
          text_length_bytes = sys.stdin.read(4)
          #myfile.write("text_length_bytes = sys.stdin.read(4) : " + str(text_length_bytes) + '\n')
  
          # Unpack message length as 4 byte integer.
          text_length = struct.unpack('i', bytes(text_length_bytes, 'utf-8'))[0]
          #myfile.write("text_length = struct.unpack('i', bytes(text_length_bytes, 'utf-8'))[0] : " + str(text_length) + "\n")

          # Read the text (JSON object) of the message.
          text = sys.stdin.read(text_length)
          #myfile.write("text = sys.stdin.read(text_length) : " + str(text) + "\n")
          
          #TODO: convert text JSON format to URL string
          json_text = json.loads(text)
          myfile.write(json_text["text"] + "\n")
          
          # Return the URL
          return json_text["text"]

      except Exception as e:
          myfile.write("Error: " + str(e) + "\n")
        

def launch(video_url):
    # Download video and set correct name
    info = get_info(video_url)
    options = get_download_options(info)
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_url])

    # Set artist in metadata of mp3 file    
    file_name = max(glob.iglob('*.[Mm][Pp]3'), key=os.path.getctime) # Latest mp3 file in folder
    set_metadata(file_name, info)

    # Move file to output folder
    shutil.move(file_name, "C:/Dev/youtube-dl-ext/host/" + file_name)

# Helper function that sends a message to the webapp.
def send_message(message):
    text = unicode('{"text": "' + message + '"}', "utf-8")
    # Write message size.
    sys.stdout.write(struct.pack('I', len(text)))
    # Write the message itself.
    sys.stdout.write(text)
    sys.stdout.flush()

def Main():
    #send_message('test')
    # Wait for message from chrome extension
    video_url = process_request()
    #print(video_url)

    # Launch process on queue content
    launch('https://www.youtube.com/watch?v=SFU1GeGFpzY')
    send_message(video_url)

if __name__ == '__main__':
  Main()