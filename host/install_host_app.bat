:: Change HKCU to HKLM if you want to install globally.
:: %~dp0 is the directory containing this bat script and ends with a backslash.
REG ADD "HKCU\Software\Google\Chrome\NativeMessagingHosts\youtubedl" /ve /t REG_SZ /d "%~dp0manifest.json" /f
REG ADD "HKLM\Software\Google\Chrome\NativeMessagingHosts\youtubedl" /ve /t REG_SZ /d "%~dp0manifest.json" /f

:: MY_PATH must be edited to reflect the correct path on your system
setx YOUTUBE_DL_EXT_HOST_PATH "MY_PATH"
