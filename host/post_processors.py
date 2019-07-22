import shutil
import glob
import os
from mp3_metadata   import set_metadata
from logger_helper  import log, log_errors

# Handlers/Post-process definition as functions
def save_metadata_to_file(params):
    file_name = params['file_name']
    info = params['info']

    # Set artist in metadata of mp3 file    
    set_metadata(file_name, info)


def move_mp3_file_to_custom_folder(params):
    file_name = params['file_name']  
    log.debug(file_name)
    log.debug(str(os.environ['YOUTUBE_DL_EXT_HOST_PATH']))
    # Move file to output folder
    shutil.move(file_name, str(os.environ['YOUTUBE_DL_EXT_HOST_PATH']) + file_name)
    log.info("Moved file to output folder")

class PostProcessor:
    def __init__(self, handlers):
        self.handlers = handlers
        self.params = None

    # NOTE: This needs to be called after the download is done
    @staticmethod
    def get_latest_mp3_filename():
        # Latest mp3 file in folder
        return max(glob.iglob('*.[Mm][Pp]3'), key=os.path.getctime)
    
    def set_params(self, params):
        self.params = params
        self.params['file_name'] = PostProcessor.get_latest_mp3_filename()

    @log_errors
    def run(self):
        for handler in self.handlers:
            log.debug(len(self.handlers))
            handler(self.params)

class PostProcessorBuilder:
    handlers_enabled = []
    recognized_handlers = {
        'move_mp3' : move_mp3_file_to_custom_folder, # Must always be last
        'set_metadata' : save_metadata_to_file
    }

    def __init__(self):
        pass

    @classmethod
    def set_enabled_post_process(cls, enabled_handlers_list = []):
        for handler_name in enabled_handlers_list:
            # If process is recognized
            if handler_name in PostProcessorBuilder.recognized_handlers:
                log.debug(handler_name)
                handler = PostProcessorBuilder.recognized_handlers[handler_name]
                PostProcessorBuilder.handlers_enabled.append(handler)
    
    @classmethod
    def build_post_processor(cls, params):
        proc = PostProcessor(PostProcessorBuilder.handlers_enabled)
        proc.set_params(params)
        return proc