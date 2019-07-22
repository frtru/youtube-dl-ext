from logger_helper import log

try:
    import eyed3
    def set_metadata(file_name, video_info):
        log.info("Setting metadata for " + file_name)
        audiofile = eyed3.load(file_name)
        audiofile.tag.artist = video_info['artist']
        audiofile.tag.album = video_info['album']
        audiofile.tag.title = video_info['track']
        audiofile.tag.save()
        log.info("Saved metadata to file")

except ImportError:
    log.warning('eyed3 couldn\'t be imported. Won\'t be able to add metadata to files.')
    def set_metadata(file_name, video_info):
        pass

    
