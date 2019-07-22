:: Deletes the entry created by install_host_app.bat
REG DELETE "HKCU\Software\Google\Chrome\NativeMessagingHosts\youtubedl" /f
REG DELETE "HKLM\Software\Google\Chrome\NativeMessagingHosts\youtubedl" /f
REG DELETE "HKCU\Environment" /F /V YOUTUBE_DL_EXT_HOST_PATH