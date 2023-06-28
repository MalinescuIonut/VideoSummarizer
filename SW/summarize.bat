::@echo OFF
::si el AVI tiene subtítulos ya sobreimpresos, se puede generar un SRT con formato ANSI para que falle la sobreimpresión de subtítulos
::bucle0: I-frames
::bucle1: frames subtitulados
::bucle2: frames cada 10 segundos
::bucle3: 1 frame por plano
::bucle4: frames subtitulados + I-frames + 1 frame por plano - redundantes
set FONTSRT=10
set NAME=%1
set EXTENS=%2
set TRACKSUBT=%3
set TRACKAUDIO=%4
set FOLDER=summarized%NAME%
set FOLDER0=%FOLDER%\summarized0%NAME%
set FOLDER2=%FOLDER%\summarized2%NAME%
set FOLDER3=%FOLDER%\summarized3%NAME%
set FOLDER4=%FOLDER%\summarized4%NAME%
set USER=%5
set THRESHOLD=%6
mkdir %FOLDER%
mkdir %FOLDER0%
mkdir %FOLDER2%
mkdir %FOLDER3%
mkdir %FOLDER4%
set "FOLDERSW=C:\Users\%USER%\Google Drive\SW"
set FILE=%NAME%.%EXTENS%

echo titulo: %NAME% >%FOLDER%\%NAME%.log
pause
::goto YA

::si existe el fichero de subtitulos, no se extrae del fichero de vídeo
del "%NAME%.tmp"
"%FOLDERSW%\GnuWin32\bin\wc" -l <"%NAME%.srt" >"%NAME%.tmp"
if exist "%NAME%.tmp" (
set /p TAM=<"%NAME%.tmp"
) else (
set TAM=0
)
del "%NAME%.tmp"

echo TAM SRT: %TAM%
IF /I "%TAM%" GEQ "1" (
copy "%NAME%.srt" "%FOLDER%\%NAME%.srt"
copy "%NAME%.srt" "%NAME%-ORIG.srt"
) else (
::"%FOLDERSW%\ffmpeg.exe" -sub_charenc -i "%FILE%" -map "0:s:%TRACKSUBT%" -y "%FOLDER%\%NAME%.srt"
"%FOLDERSW%\ffmpeg.exe" -i "%FILE%" -map "0:s:%TRACKSUBT%" -y "%FOLDER%\%NAME%.srt"
)
copy "%FOLDER%\%NAME%.srt" "%FOLDER%\%NAME%ORIG.srt"
copy "%FOLDER%\%NAME%.srt" "%NAME%.srt"
::goto YA
::pause
"%FOLDERSW%\ffmpeg.exe" -i "%FILE%" -y "%FOLDER%\%NAME%.mp3"
python "%FOLDERSW%\ina_speech_segmenter.py" -i "%FOLDER%\%NAME%.mp3" -g true -o . -b "%FOLDERSW%\ffmpeg.exe"
::pause
copy "%NAME%.csv" "%FOLDER%\%NAME%.csv"
perl "%FOLDERSW%\label2srt.pl" <"%FOLDER%\%NAME%.csv" >"%FOLDER%\%NAME%-SEGMENTATION.srt" 
::pause

"%FOLDERSW%\ffmpeg.exe" -i "%FILE%" -af "silencedetect=n=-50dB:d=0.5,ametadata=print:file=%NAME%_SILENCE.dep" -map "0:a:%TRACKAUDIO%" -y "%NAME%_SILENCE.mp3"
del %NAME%_SILENCE.mp3
mkdir %FOLDER%
"%FOLDERSW%\grep.exe" -v "silence_duration" "%NAME%_SILENCE.dep" | "%FOLDERSW%\grep.exe" "silence_[a-z]*=[0-9.]*" -o | "%FOLDERSW%\grep.exe" [0-9.]* -o >%FOLDER%\%NAME%_SILENCE.lis
perl "%FOLDERSW%\lis2srt.pl" 2 SILENCE < %FOLDER%\%NAME%_SILENCE.lis >%FOLDER%\%NAME%_SILENCE.srt
del %NAME%_SILENCE.dep
"%FOLDERSW%\ffmpeg.exe" -i "%FILE%" -vf "blackdetect=d=0.1:pix_th=.1,metadata=print:file=%NAME%_BLACK.dep" -y "%NAME%_BLACK.%EXTENS%"
del %NAME%_BLACK.%EXTENS%
"%FOLDERSW%\grep.exe" "black" "%NAME%_BLACK.dep" | "%FOLDERSW%\grep.exe" "black_[a-z]*=[0-9.]*" -o | "%FOLDERSW%\grep.exe" [0-9.]* -o >%FOLDER%\%NAME%_BLACK.lis
perl "%FOLDERSW%\lis2srt.pl" 2 BLACK < %FOLDER%\%NAME%_BLACK.lis >%FOLDER%\%NAME%_BLACK.srt
del %NAME%_BLACK.dep

"%FOLDERSW%\ffmpeg.exe" -i "%FILE%" -filter_complex "select='gt(scene,0.4)',metadata=print:file=%NAME%sequenceORIG.dep" -vsync vfr -y dep%FILE% 2> %FOLDER%\%NAME%sequenceORIG.dep
del dep%FILE%
type %FOLDER%\%NAME%sequenceORIG.dep
"%FOLDERSW%\grep.exe" "pts_time:" "%NAME%sequenceORIG.dep" | "%FOLDERSW%\grep.exe" "pts_time:[0-9.]*" -o | "%FOLDERSW%\grep.exe" [0-9.]* -o >%FOLDER%\%NAME%sequenceORIG.lis
copy %NAME%sequenceORIG.dep %FOLDER%\
del %NAME%sequenceORIG.dep


"%FOLDERSW%\ffmpeg.exe" -i "%FILE%" -filter_complex "select='gt(scene,%THRESHOLD%)',metadata=print:file=%NAME%scenesORIG.dep" -vsync vfr -y dep%FILE% 2> %FOLDER%\%NAME%shotsORIG.dep 
del dep%FILE%
type %FOLDER%\%NAME%shotsORIG.dep
"%FOLDERSW%\grep.exe" "pts_time:" "%NAME%scenesORIG.dep" | "%FOLDERSW%\grep.exe" "pts_time:[0-9.]*" -o | "%FOLDERSW%\grep.exe" [0-9.]* -o >%FOLDER%\%NAME%scenesORIG.lis
echo 10000.0 >> %FOLDER%\%NAME%scenesORIG.lis
perl "%FOLDERSW%\inScene.pl" %FOLDER%\%NAME%scenesORIG.lis <%FOLDER%\"%NAME%.srt" >%FOLDER%\"%NAME%.srt.dep"
perl "%FOLDERSW%\subtitulos.pl" 100000 0 <%FOLDER%\"%NAME%.srt.dep" >%FOLDER%\%NAME%srt.lis
perl "%FOLDERSW%\lis2srt.pl" 1 SHOT <%FOLDER%\%NAME%scenesORIG.lis >%FOLDER%\%NAME%scenesORIG.srt
copy "%FOLDER%\%NAME%.srt.dep" "%FOLDER%\%NAME%.srt"
::pause
"%FOLDERSW%\ffmpeg.exe" -i "%FILE%" -vcodec libx264 -acodec aac -map "0:a:%TRACKAUDIO%" -map "0:v:0" -vf "subtitles=%NAME%.srt" -y "%FOLDER%\\%NAME%ORIG.mp4"
"%FOLDERSW%\ffmpeg.exe" -i "%FILE%" -vcodec libx264 -acodec aac -map "0:a:%TRACKAUDIO%" -map "0:v:0" -vf "subtitles=%NAME%.srt,scale=720:-2" -y "%FOLDER%\\%NAME%-ORIG.mp4"
::pause
copy "%FOLDER%\%NAME%.srt" "%NAME%.srt"
::si existe el fichero MP4, se procesa de manera diferente
del "%NAME%.tmp"
del %NAME%scenesORIG.dep
"%FOLDERSW%\GnuWin32\bin\wc" -c <"%FOLDER%\\%NAME%.mp4" >"%NAME%.tmp"
if exist "%NAME%.tmp" (
set /p TAM=<"%NAME%.tmp"
) else (
set TAM=0
)
del "%NAME%.tmp"

echo TAM MP4: %TAM%
IF /I "%TAM%" GEQ "1" (
echo "ya había MP4"
) else (
::"%FOLDERSW%\ffmpeg.exe" -i "%FILE%" -vcodec libx264 -acodec aac -map "0:a:%TRACKAUDIO%" -map "0:v:0" -vf "subtitles=%NAME%.srt" -max_muxing_queue_size 400 -y "%FOLDER%\\%NAME%.mp4"
"%FOLDERSW%\ffmpeg.exe" -i "%FILE%" -vcodec libx264 -acodec aac -map "0:a:%TRACKAUDIO%" -map "0:v:0" -vf "subtitles=%NAME%.srt:force_style=Fontsize=%FONTSRT%" -y "%FOLDER%\\%NAME%.mp4"

)
::pause
:YA

del "%NAME%.tmp"
"%FOLDERSW%\GnuWin32\bin\wc" -c <"%FOLDER%\\%NAME%.mp4" >"%NAME%.tmp"
if exist "%NAME%.tmp" (
set /p TAM=<"%NAME%.tmp"
) else (
set TAM=0
)
del "%NAME%.tmp"

echo TAM MP4: %TAM%
::pause
if /I "%TAM%" GEQ "1" (
echo OK MP4
goto SINAVI
) else (
pause
del "%FOLDER%\\%NAME%.mp4"
"%FOLDERSW%\ffmpeg.exe" -i "%FILE%" -vf "subtitles=%NAME%.srt,drawtext=fontsize=%FONTSRT%" -y "%FOLDER%\\%NAME%.mpg"
)
pause
del "%NAME%.tmp"
"%FOLDERSW%\GnuWin32\bin\wc" -c <"%FOLDER%\\%NAME%.mpg" >"%NAME%.tmp"
if exist "%NAME%.tmp" (
set /p TAM=<"%NAME%.tmp"
) else (
set TAM=0
)
del "%NAME%.tmp"

echo TAM MPG: %TAM%
IF /I "%TAM%" GEQ "1" (
echo OK MPG
) else (
del "%FOLDER%\\%NAME%.mpg"
copy "%FILE%" "%FOLDER%\\"
echo OK SIN SUBTITULOS
pause
)
:SINAVI
echo subtitulosNum: >>%FOLDER%\%NAME%.log
"%FOLDERSW%\GnuWin32\bin\grep.exe" -P "\d+\:\d+" %NAME%.srt | "%FOLDERSW%\GnuWin32\bin\wc.exe" -l  >>%FOLDER%\%NAME%.log
echo subtitulosWord: >>%FOLDER%\%NAME%.log
"%FOLDERSW%\GnuWin32\bin\grep.exe" -v -P "^\d" %NAME%.srt | "%FOLDERSW%\GnuWin32\bin\wc.exe" -w  >>%FOLDER%\%NAME%.log
::pause
start "bucle0" call "%FOLDERSW%\bucle0summarize.bat" %NAME% %FOLDER% %FOLDER2% %FOLDER3% %USER% %THRESHOLD% %FOLDER0% %FOLDER4%

"%FOLDERSW%\ffmpeg.exe" -i "%FILE%" -f ffmetadata %FOLDER%/%NAME%-METADATA.dep
echo chaptersNum: >>%FOLDER%\%NAME%.log
"%FOLDERSW%\grep.exe" "\[CHAPTER\]" %FOLDER%/%NAME%-METADATA.dep | "%FOLDERSW%\GnuWin32\bin\wc" -l >>%FOLDER%\%NAME%.log

echo silenceNum*2: >>%FOLDER%\%NAME%.log
"%FOLDERSW%\GnuWin32\bin\wc" -l %FOLDER%\%NAME%_SILENCE.lis >>%FOLDER%\%NAME%.log

echo blackNum*2: >>%FOLDER%\%NAME%.log
"%FOLDERSW%\GnuWin32\bin\wc" -l %FOLDER%\%NAME%_BLACK.lis >>%FOLDER%\%NAME%.log

exit
