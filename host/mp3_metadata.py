from logger_helper import log, log_errors
from mutagen.easyid3 import EasyID3


@log_errors
def set_metadata(file_name, video_info):
    log.info("Setting metadata for " + file_name)
    audio = EasyID3(file_name)
    if video_info.get('artist') is not None:
        audio['artist'] = video_info['artist']
    if video_info.get('album') is not None:
        audio['album'] = video_info['album']
    if video_info.get('track') is not None:
        audio['track'] = video_info['track']
    audio.save()
    log.info("Saved metadata to file")
