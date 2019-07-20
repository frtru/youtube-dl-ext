Can download a video and save the audio to a mp3 file, edit its metadata when available on your local disk. Used conjointly with the google play music daemon on that specific folder enables the user to upload the said music file on google play. Furthermore, the phone application enables the user to download any changes or new files being pushed on your account.

TLDR: In one click, you can download the audio of a youtube video on your cell phone.

**NOTES**
- Only windows compatible at the moment. Need to develop an install shell script for unix/linux systems.
- Most of the code is python and is located in the host folder.
- I just realized there are javascript bindings for youtube-dl which would have been much easier to develop than using a native app in python and also more portable because the code would be directly embedded in the browser instead of having to register the host app as well.
- Will create a queue/threading to handle all upcoming requests and not terminate the app when it is done after one request.
