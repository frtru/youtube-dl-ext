from logger_helper import log

try:
    from mutagen.easyid3 import EasyID3

    def set_metadata(file_name, video_info):
        log.info("Setting metadata for " + file_name)
        audio = EasyID3(file_name)
        audio['artist'] = video_info['artist']
        audio['album'] = video_info['album']
        audio['title'] = video_info['track']
        audio.save()
        log.info("Saved metadata to file")

except ImportError:
    log.warning('EasyID3 couldn\'t be imported. Won\'t be able to add metadata to files.')
    def set_metadata(file_name, video_info):
        pass

    
