::copy "C:\Users\gth\Google Drive\SW\VideoSubFinder_5.10_x64\Release_x64\TXTImages\*.jpeg" tmp\
::dir /B tmp\*.jpeg >JPEG.LIS
::FOR /F %%A IN (JPEG.LIS) DO (
::"C:\Program Files\Subtitle Edit\Tesseract302\Tesseract.exe" "tmp\%%A" "C:\Users\gth\Google Drive\SW\VideoSubFinder_5.10_x64\Release_x64\TXTResults\%%A"
::)
::pause
set USER=jmmm
set "FOLDERSW=C:\Users\%USER%\Google Drive\SW"
::set NAME=TheGreat1x10
::set NAME=TheVastOfNight2020Patterson
set NAME=TheBigamist1953Lupino
set EXTENS=mkv
::set EXTENS=mkv
::set EXTENS=mp4
set FILE=%NAME%.%EXTENS%
set FILEORIG=%NAME%ORIG.%EXTENS%
::set TRACKAUDIO=0
set TRACKAUDIO=1
::set TRACKAUDIO=2
set TRACKSUBT=0
::set TRACKSUBT=1
set FOLDER=summarized%NAME%
set FOLDER0=%FOLDER%\summarized0%NAME%
set FOLDER2=%FOLDER%\summarized2%NAME%
set FOLDER3=%FOLDER%\summarized3%NAME%
set FOLDER4=%FOLDER%\summarized4%NAME%
set THRESHOLD=0.15

::"%FOLDERSW%\ffmpeg.exe" -i "%FILE%" -vcodec libx264 -acodec aac -map "0:a:%TRACKAUDIO%" -map "0:v:0" -vf "subtitles=%NAME%.srt:force_style=Fontsize=12" -y "%FOLDER%\\%NAME%.mp4"
::pause
::mkdir %FOLDER%
::python "%FOLDERSW%\listPlot.py"
::pause

::call "%FOLDERSW%\bucle2summarize.bat" %NAME% %FOLDER% %FOLDER2% %FOLDER3% %USER% %THRESHOLD% %FOLDER0% 
::call "%FOLDERSW%\bucle3summarize.bat" %NAME% %FOLDER% %FOLDER2% %FOLDER3% %USER% %THRESHOLD% %FOLDER0% 
::call "%FOLDERSW%\bucle4summarize.bat" %NAME% %FOLDER% %FOLDER2% %FOLDER3% %USER% %THRESHOLD% %FOLDER0% %FOLDER4%
::"%FOLDERSW%\ffmpeg.exe" -i "%FILE%" -map "0:s:%TRACKSUBT%" -y "%NAME%.srt"

::"%FOLDERSW%\ffmpeg.exe" -i "%FILE%" -f ffmetadata %FOLDER%/%NAME%-METADATA.dep
::echo chaptersNum: >>%FOLDER%\%NAME%.log
::"%FOLDERSW%\grep.exe" "\[CHAPTER\]" %FOLDER%/%NAME%-METADATA.dep | "%FOLDERSW%\GnuWin32\bin\wc" -l >>%FOLDER%\%NAME%.log
::start "subtitulado%NAME%" "%FOLDERSW%\ffmpeg.exe" -i "%FILE%" -i %FOLDER%/%NAME%-METADATA.dep -map_metadata 1 -vcodec libx264 -acodec aac -map "0:a:%TRACKAUDIO%" -map "0:v:0" -vf "subtitles=%NAME%-ORIG.srt" -y "%NAME%.mp4"


::start "subtitulado%NAME%" "%FOLDERSW%\ffmpeg.exe" -i "%FILE%" -vcodec libx264 -acodec aac -map "0:a:%TRACKAUDIO%" -map "0:v:0" -vf "subtitles=%NAME%.srt" -y "%NAME%.mp4"

::"%FOLDERSW%\ffmpeg.exe" -i "%FILE%" -map "0:s:%TRACKSUBT%" -y "%NAME%.srt"
::"%FOLDERSW%\ffmpeg.exe" -i "%FILE%" -vcodec libx264 -acodec aac -map "0:a:%TRACKAUDIO%" -map "0:v:0" -vf "subtitles=%NAME%.srt" -y "%NAME%.mp4"

::"%FOLDERSW%\ffmpeg.exe" -i "%FILE%" -vcodec libx264 -acodec aac -map "0:a:%TRACKAUDIO%" -map "0:v:0" -y "%NAME%.mp4"
::"%FOLDERSW%\ffmpeg.exe" -i "%FILE%" -vcodec libx264 -acodec aac -map "0:a:%TRACKAUDIO%" -map "0:v:0" -max_muxing_queue_size 400 -y "%NAME%.mp4"
::"%FOLDERSW%\ffmpeg.exe" -i "%FILE%" -c:v mpeg4 -qscale:v 20 -c:a libmp3lame -qscale:a 20 -map "0:a:%TRACKAUDIO%" -map "0:v:0" -max_muxing_queue_size 400 -y "%NAME%-new.mp4"
::perl "%FOLDERSW%\lis2srt.pl" <%FOLDER%\%NAME%scenesORIG.lis >%FOLDER%\%NAME%scenesORIG.srt
::"%FOLDERSW%\ffmpeg.exe" -i "%FILE%" -vcodec libx264 -acodec aac -map "0:a:%TRACKAUDIO%" -map "0:v:0" -vf "subtitles=%NAME%ORIG.srt,scale=1280:-2" -y "%FOLDER%\\%NAME%-ORIG.mp4"

"%FOLDERSW%\ffmpeg.exe" -i "%FILE%" -vcodec libx264 -acodec aac -map "0:a:%TRACKAUDIO%" -map "0:v:0" -vf "subtitles=%NAME%ORIG.srt,scale=720:-2" -y "%FOLDER%\\%NAME%-ORIG.mp4"
::"%FOLDERSW%\ffmpeg.exe" -i "%FILE%" -af "silencedetect=n=-50dB:d=0.5,ametadata=print:file=%NAME%_SILENCE.dep" -y "%NAME%_SILENCE.mp3"
::del %NAME%_SILENCE.mp3
::"%FOLDERSW%\grep.exe" -v "silence_duration" "%NAME%_SILENCE.dep" | "%FOLDERSW%\grep.exe" "silence_[a-z]*=[0-9.]*" -o | "%FOLDERSW%\grep.exe" [0-9.]* -o >%FOLDER%\%NAME%_SILENCE.lis
::perl "%FOLDERSW%\lis2srt.pl" 2 SILENCE < %FOLDER%\%NAME%_SILENCE.lis >%FOLDER%\%NAME%_SILENCE.srt
::del %NAME%_SILENCE.dep
::echo silenceNum*2: >>%FOLDER%\%NAME%.log
::"%FOLDERSW%\GnuWin32\bin\wc" -l %FOLDER%\%NAME%_SILENCE.lis >>%FOLDER%\%NAME%.log
::"%FOLDERSW%\ffmpeg.exe" -i "%FILE%" -vf "blackdetect=d=0.1:pix_th=.1,metadata=print:file=%NAME%_BLACK.dep" -y "%NAME%_BLACK.%EXTENS%"
::del %NAME%_BLACK.%EXTENS%
::"%FOLDERSW%\grep.exe" "black" "%NAME%_BLACK.dep" | "%FOLDERSW%\grep.exe" "black_[a-z]*=[0-9.]*" -o | "%FOLDERSW%\grep.exe" [0-9.]* -o >%FOLDER%\%NAME%_BLACK.lis
::perl "%FOLDERSW%\lis2srt.pl" 2 BLACK < %FOLDER%\%NAME%_BLACK.lis >%FOLDER%\%NAME%_BLACK.srt
::del %NAME%_BLACK.dep
::echo blackNum*2: >>%FOLDER%\%NAME%.log
::"%FOLDERSW%\GnuWin32\bin\wc" -l %FOLDER%\%NAME%_BLACK.lis >>%FOLDER%\%NAME%.log
::echo 10000.0 >> %FOLDER%\%NAME%scenesORIG.lis
::perl "%FOLDERSW%\inScene.pl" %FOLDER%\%NAME%scenesORIG.lis <%FOLDER%\"%NAME%ORIG.srt" >%FOLDER%\"%NAME%.srt.dep"

::perl "%FOLDERSW%\subtitulos.pl" 100000 0 <%FOLDER%\"%NAME%.srt.dep" >%FOLDER%\%NAME%srt.lis
::perl "%FOLDERSW%\lis2srt.pl" 1 SHOT <%FOLDER%\%NAME%scenesORIG.lis >%FOLDER%\%NAME%scenesORIG.srt
::copy "%FOLDER%\%NAME%.srt.dep" "%FOLDER%\%NAME%.srt"

::python "%FOLDERSW%\PySceneDetect\scenedetect.py" -i goldeneye.mp4 -o output_dir detect-content -t 27 list-scenes save-images split-video
::python "%FOLDERSW%\PySceneDetect\scenedetect.py" -i CabezaDePerro2006Amodeo.avi -o output_dir detect-content -t 27 list-scenes save-images split-video
::pause
::"%FOLDERSW%\ffmpeg.exe" -i "%FILE%" -y "%NAME%.mp3"
::python "%FOLDERSW%\ina_speech_segmenter.py" -i "%NAME%.mp3" -g true -o . -b "%FOLDERSW%\ffmpeg.exe"
::dir /b /o:d "%FOLDER0%\*.jpg" | "%FOLDERSW%\GnuWin32\bin\tail" -1 | "%FOLDERSW%\grep.exe" -o [0-9]*. | "%FOLDERSW%\grep.exe" -o [0-9]* >NUMSECS.dep
::set /p NUMSECS=<NUMSECS.dep
::set /A NUMSECS=NUMSECS+10
::FOR /L %%A IN (1,10,%NUMSECS%) DO echo %%A
::del NUMSECS.dep

pause
