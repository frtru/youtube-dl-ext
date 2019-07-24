import threading
import queue
import os
import youtube_dl
from post_processors import PostProcessorBuilder, PostProcessor
from chrome_extension_messages import *
from mp3_metadata import set_metadata
from logger_helper import log, log_errors
from decorators import supress_stdout

if sys.platform == "win32":
    import msvcrt
    msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)


def yt_download(options, videos):
    youtube_dl.YoutubeDL(options).download(videos)


def yt_get_info(video_url):
    return youtube_dl.YoutubeDL({}).extract_info(video_url, download=False)


def yt_get_download_options(info):
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a'
        }, {
            'key': 'FFmpegMetadata'
        }],
        'logger': log
    }
    if info['track'] is not None:
        options['outtmpl'] = '%(track)s.%(ext)s'
    else:
        options['outtmpl'] = '%(title)s.%(ext)s'
    return options


def process_queue_thread(q):
    while not q.empty():
        url = q.get()
        if url is not None:
            launch(url)
        else:
            break
    q.task_done()


@supress_stdout
@log_errors
def launch(video_url):
    log.info("Launching process on url : " + video_url)
    # Getting the metadata from the video on youtube
    info = yt_get_info(video_url)
    # Deducing the options based on the information available in the metadata
    options = yt_get_download_options(info)
    # Actually download the file(s)
    yt_download(options, [video_url])

    # Package parameters into a map to pass to the post-processor
    params = {
        'info': info,
        'options': options,
        'video_url': video_url
    }
    # Apply other tasks
    pp = PostProcessorBuilder.build(params)
    pp.run()


@log_errors
def Main():
    PostProcessorBuilder.set_enabled_post_process(sys.argv)
    q = queue.Queue()
    while True:
        # Wait for message from chrome extension
        video_url = wait_and_decode_message()
        q.put(video_url.split("&list", 1)[0])
        # ',' is needed in the following arguments to make it iterable
        threading.Thread(target=process_queue_thread, args=(q,)).start()

if __name__ == '__main__':
    Main()
