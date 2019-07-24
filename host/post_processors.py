import shutil
import glob
import os
from mp3_metadata import set_metadata
from logger_helper import log, log_errors


# Handlers/Post-process definition as functions
def save_metadata_to_file(params):
    if params.get('file_name') is None or params.get('info') is None:
        log.error('Cannot fetch music file to save metadata. \'file_name\' or '
                  '\'info\' is None. file_name=' +
                  str(params.get('file_name')))
        return
    file_name = params['file_name']
    info = params['info']

    # Set artist in metadata of mp3 file
    set_metadata(file_name, info)


def move_music_file_to_custom_folder(params):
    if params.get('file_name') is None:
        log.error('Cannot fetch music file to save metadata. file_name=' +
                  str(params.get('file_name')))
        return
    file_name = params['file_name']
    # Move file to output folder
    output_location = str(os.environ['YOUTUBE_DL_EXT_HOST_PATH']) + file_name
    shutil.move(file_name, output_location)
    log.info("Moved file to " + output_location)


class PostProcessor:
    def __init__(self, handlers):
        self.handlers = handlers
        self.params = None

    # NOTE: This needs to be called after the download is done
    @staticmethod
    def get_latest_music_filename():
        # Latest music file in folder
        try:
            return max(glob.iglob('*.[Mm][Pp4][Aa3]'), key=os.path.getctime)
        except ValueError:
            return None

    def set_params(self, params):
        self.params = params
        self.params['file_name'] = PostProcessor.get_latest_music_filename()

    @log_errors
    def run(self):
        for handler in self.handlers:
            handler(self.params)


class PostProcessorBuilder:
    handlers_enabled = []
    recognized_handlers = {
        # 'move_to_output_folder' must always be last
        'move_to_output_folder': move_music_file_to_custom_folder,
        'set_metadata': save_metadata_to_file
    }

    def __init__(self):
        pass

    @classmethod
    def set_enabled_post_process(cls, enabled_handlers_list=[]):
        for handler_name in enabled_handlers_list:
            # If process is recognized
            if handler_name in PostProcessorBuilder.recognized_handlers:
                handler = PostProcessorBuilder.recognized_handlers[
                    handler_name]
                PostProcessorBuilder.handlers_enabled.append(handler)

    @classmethod
    def build(cls, params):
        proc = PostProcessor(PostProcessorBuilder.handlers_enabled)
        proc.set_params(params)
        return proc
