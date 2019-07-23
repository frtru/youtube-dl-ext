import sys
import json
import struct
from logger_helper import log, log_errors


@log_errors
def wait_and_decode_message():
        # Read the message length (first 4 bytes).
        text_length_bytes = sys.stdin.read(4)
        # Unpack message length as 4 byte integer.
        text_length = struct.unpack('i', bytes(text_length_bytes, 'utf-8'))[0]
        # Read the text (JSON object) of the message.
        text = sys.stdin.read(text_length)
        # Convert text JSON format to URL string
        json_text = json.loads(text)
        # Return the URL
        return json_text['text']


# Helper function that sends a message to the webapp.
@log_errors
def send_message(message):
    text = unicode('{"text": "' + message + '"}', "utf-8")
    # Write message size.
    sys.stdout.write(struct.pack('I', len(text)))  # TODO: Fix issue here
    # Write the message itself.
    sys.stdout.write(text)
    sys.stdout.flush()
