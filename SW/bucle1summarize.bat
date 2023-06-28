set NAME=%1
set FOLDER=%2
set FOLDER2=%3
set FOLDER3=%4
set USER=%5
set THRESHOLD=%6
set FOLDER0=%7
set FOLDER4=%8

set "FOLDERSW=C:\Users\%USER%\Google Drive\SW"

if exist %FOLDER%\%NAME%.mp4 (
echo hay mp4
::pause
goto CONMP4
)

if exist %FOLDER%\%NAME%.mpg (
echo hay mpg
goto CONMPG
)

if exist %FOLDER%\%NAME%.avi (
echo hay avi
goto CONAVI
)

if exist %FOLDER%\%NAME%.mkv (
echo hay mkv
goto CONMKV
)


:CONMP4
FOR /F %%A IN (%FOLDER%\%NAME%srt.lis) DO (
"%FOLDERSW%\ffmpeg.exe" -ss %%A -i "%FOLDER%\%NAME%.mp4" -vf "drawtext=fontsize=10:fontcolor=yellow:box=1:boxcolor=black:x=(W-tw)/4:y=H-th-2: text='Time\: %%A'" -vframes 1 -vsync vfr -y "%FOLDER%\%%A-%NAME%-SRT.jpg"
)
goto FIN

:CONMPG
FOR /F %%A IN (%FOLDER%\%NAME%srt.lis) DO (
"%FOLDERSW%\ffmpeg.exe" -ss %%A -i "%FOLDER%\%NAME%.mpg" -vf "drawtext=fontsize=10:fontcolor=yellow:box=1:boxcolor=black:x=(W-tw)/4:y=H-th-2: text='Time\: %%A'" -vframes 1 -vsync vfr -y "%FOLDER%\%%A-%NAME%-SRT.jpg"
)
goto FIN

:CONAVI
FOR /F %%A IN (%FOLDER%\%NAME%srt.lis) DO (
"%FOLDERSW%\ffmpeg.exe" -ss %%A -i "%FOLDER%\%NAME%.avi" -vf "drawtext=fontsize=10:fontcolor=yellow:box=1:boxcolor=black:x=(W-tw)/4:y=H-th-2: text='Time\: %%A'" -vframes 1 -vsync vfr -y "%FOLDER%\%%A-%NAME%-SRT.jpg"
)
goto FIN

:CONMKV
FOR /F %%A IN (%FOLDER%\%NAME%srt.lis) DO (
"%FOLDERSW%\ffmpeg.exe" -ss %%A -i "%FOLDER%\%NAME%.mkv" -vf "drawtext=fontsize=10:fontcolor=yellow:box=1:boxcolor=black:x=(W-tw)/4:y=H-th-2: text='Time\: %%A'" -vframes 1 -vsync vfr -y "%FOLDER%\%%A-%NAME%-SRT.jpg"
)
goto FIN

:FIN


echo subtitulosJPG: >>%FOLDER%\%NAME%.log
dir /b "%FOLDER%\*.jpg" | "%FOLDERSW%\GnuWin32\bin\wc.exe" -l >>%FOLDER%\%NAME%.log

start "bucle2" call "%FOLDERSW%\bucle2summarize.bat" %NAME% %FOLDER% %FOLDER2% %FOLDER3% %USER% %THRESHOLD% %FOLDER0% %FOLDER4%

exit
