set USER=jmmm
set "FOLDERSW=C:\Users\%USER%\Google Drive\SW"
set NAME=00046
::set NAME=00001
::set EXTENS=mkv
::set EXTENS=avi
::set EXTENS=mp4
set EXTENS=MTS
set FILE=%NAME%.%EXTENS%
set FILEORIG=%NAME%ORIG.%EXTENS%
set TRACKAUDIO=0
::set TRACKAUDIO=1
::set TRACKAUDIO=2
set TRACKSUBT=0
::set TRACKSUBT=1
set FOLDER=summarized%NAME%
set FOLDER0=%FOLDER%\summarized0%NAME%
set FOLDER2=%FOLDER%\summarized2%NAME%
set FOLDER3=%FOLDER%\summarized3%NAME%

set FOLDER4=%FOLDER%\summarized4%NAME%
set THRESHOLD=0.15

::pause A MANO conda activate tf
::conda deactivate
goto ATAJO:
::goto ATAJO3:
::pause A MANO conda activate tf
::conda activate tf
::goto ATAJOMP3 

mkdir %FOLDER%
::"%FOLDERSW%\ffmpeg.exe" -i "%FILE%" -af "silencedetect=n=-50dB:d=0.5,ametadata=print:file=%NAME%_SILENCE.dep" -map "0:a:%TRACKAUDIO%" -y "%NAME%_SILENCE.mp3"
::del %NAME%_SILENCE.mp3
::"%FOLDERSW%\grep.exe" -v "silence_duration" "%NAME%_SILENCE.dep" | "%FOLDERSW%\grep.exe" "silence_[a-z]*=[0-9.]*" -o | "%FOLDERSW%\grep.exe" [0-9.]* -o >%FOLDER%\%NAME%_SILENCE.lis
::perl "%FOLDERSW%\lis2srt.pl" 2 SILENCE < %FOLDER%\%NAME%_SILENCE.lis >%FOLDER%\%NAME%_SILENCE.srt
::del %NAME%_SILENCE.dep

"%FOLDERSW%\ffmpeg.exe" -i "%FILE%" -map "0:a:%TRACKAUDIO%" -ac 2 -y "%FOLDER%/%NAME%.mp3"
::pause
:ATAJOMP3
python "%FOLDERSW%\ina_speech_segmenter.py" -i "%FOLDER%/%NAME%.mp3" -g true -o . -b "%FOLDERSW%\ffmpeg.exe"
::pause
:ATAJO3
move %NAME%.csv %FOLDER%\
perl "%FOLDERSW%\label2srt.pl" <"%FOLDER%\%NAME%.csv" >"%FOLDER%/%NAME%-SEGMENTATION.srt" 
::pause
perl "%FOLDERSW%\srt2script.pl" "%NAME%" %EXTENS% <"%FOLDER%\%NAME%-SEGMENTATION.srt" >"%FOLDER%/%NAME%-SEGMENTATION.bat"
::pause
call "%FOLDER%/%NAME%-SEGMENTATION.bat"
"C:\Program Files (x86)\Notepad++\notepad++" "%FOLDERSW%\recoSubtitula.bat"
pause A MANO conda deactivate

:ATAJO
del subtitulos.srt
python "%FOLDERSW%\reco.py" %NAME%
pause
copy subtitulos.srt %FOLDER%\%NAME%.srt.old
perl "%FOLDERSW%\limpiaSRT.pl" <%FOLDER%\%NAME%.srt.old >%FOLDER%\%NAME%.srt

"C:\Program Files (x86)\Notepad++\notepad++" "%FOLDERSW%\recoSubtitula.bat" "%FOLDERSW%\summarizeEjemplo.bat"
pause
