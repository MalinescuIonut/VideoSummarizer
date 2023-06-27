set NAME=%1
set FOLDER=%2
set FOLDER2=%3
set FOLDER3=%4
set USER=%5
set THRESHOLD=%6
set FOLDER0=%7
set FOLDER4=%8
set "FOLDERSW=C:\Users\%USER%\Google Drive\SW"

dir /b /o:d "%FOLDER0%\*.jpg" | "%FOLDERSW%\GnuWin32\bin\tail" -1 | "%FOLDERSW%\grep.exe" -o [0-9]*. | "%FOLDERSW%\grep.exe" -o [0-9]* >NUMSECS.dep
set /p NUMSECS=<NUMSECS.dep
set /A NUMSECS=NUMSECS+10
del NUMSECS.dep

if exist %FOLDER%\%NAME%.mp4 (
goto CONMP4
) else (
goto SINMP4
)
:CONMP4
FOR /L %%A IN (1,10,%NUMSECS%) DO "%FOLDERSW%\ffmpeg.exe" -ss %%A -i "%FOLDER%\%NAME%.mp4" -vf "drawtext=fontsize=10:fontcolor=yellow:box=1:boxcolor=black:x=(W-tw)/4:y=H-th-2: text='Time\: %%A'" -vframes 1 -vsync vfr -y "%FOLDER2%\%%A-%NAME%-TIME.jpg"

:SINMP4
if exist %FOLDER%\%NAME%.mpg (
goto CONMPG
) else (
goto SINMPG
)
:CONMPG

FOR /L %%A IN (1,10,%NUMSECS%) DO "%FOLDERSW%\ffmpeg.exe" -ss %%A -i "%FOLDER%\%NAME%.mpg" -vf "drawtext=fontsize=10:fontcolor=yellow:box=1:boxcolor=black:x=(W-tw)/4:y=H-th-2: text='Time\: %%A'" -vframes 1 -vsync vfr -y "%FOLDER2%\%%A-%NAME%-TIME.jpg"

:SINMPG
del "%NAME%.tmp"
dir /b "%FOLDER2%\*.jpg" | "%FOLDERSW%\GnuWin32\bin\wc" -l >"%NAME%.tmp"
if exist "%NAME%.tmp" (
set /p TAM=<"%NAME%.tmp"
) else (
set TAM=0
)
del "%NAME%.tmp"

echo TAM MPG: %TAM%
IF /I "%TAM%" GEQ "10" (
echo OK SINAVI
goto SINAVI
) else (
echo OK CONAVI
)

if exist %FOLDER%\%NAME%.avi (
goto CONAVI
) else (
goto SINAVI
)
:CONAVI
FOR /L %%A IN (1,10,%NUMSECS%) DO "%FOLDERSW%\ffmpeg.exe" -ss %%A -i "%FOLDER%\%NAME%.avi" -vf "drawtext=fontsize=10:fontcolor=yellow:box=1:boxcolor=black:x=(W-tw)/4:y=H-th-2: text='Time\: %%A'" -vframes 1 -vsync vfr -y "%FOLDER2%\%%A-%NAME%-TIME.jpg"

:SINAVI

if exist %FOLDER%\%NAME%.avi (
goto CONMKV
) else (
goto SINMKV
)
:CONMKV
FOR /L %%A IN (1,10,%NUMSECS%) DO "%FOLDERSW%\ffmpeg.exe" -ss %%A -i "%FOLDER%\%NAME%.mkv" -vf "drawtext=fontsize=10:fontcolor=yellow:box=1:boxcolor=black:x=(W-tw)/4:y=H-th-2: text='Time\: %%A'" -vframes 1 -vsync vfr -y "%FOLDER2%\%%A-%NAME%-TIME.jpg"

:SINMKV

::"%FOLDER%\ffmpeg.exe" -ss %%A -i "%FILE%" -filter_complex "[0:s]scale=1280:576[sub];[0:v][sub]overlay[v]" -map "[v]" -vframes 1 -vsync vfr "%FOLDER%\out%%A.jpg"
echo "segundos/10" >>%FOLDER%\%NAME%.log
dir /b "%FOLDER2%\*.jpg" | "%FOLDERSW%\GnuWin32\bin\wc.exe" -l >>%FOLDER%\%NAME%.log

start "bucle3" call "%FOLDERSW%\bucle3summarize.bat" %NAME% %FOLDER% %FOLDER2% %FOLDER3% %USER% %THRESHOLD% %FOLDER0% %FOLDER4%
exit