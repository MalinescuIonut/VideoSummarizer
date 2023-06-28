set NAME=%1
set FOLDER=%2
set FOLDER2=%3
set FOLDER3=%4
set USER=%5
set THRESHOLD=%6
set FOLDER0=%7
set FOLDER4=%8
set "FOLDERSW=C:\Users\%USER%\Google Drive\SW"

perl "%FOLDERSW%\subtitulos.pl" 100000 1 <%FOLDER%\"%NAME%.srt" >"%FOLDER%\%NAME%srtMP4.lis"
type "%FOLDER%\%NAME%srtMP4.lis" >tmp.lis
type "%FOLDER%\%NAME%scenesMP4.lis" >>tmp.lis

echo copy %FOLDER%\\*.jpg %FOLDER4%\\ >"%FOLDER%\copiar4.bat"
perl "%FOLDERSW%\conSubtitulos.pl" "%FOLDER%\%NAME%srtMP4.lis" "%FOLDER3%" "%FOLDER4%" <"%FOLDER%\%NAME%scenesMP4.lis" >>"%FOLDER%\copiar4.bat"
perl "%FOLDERSW%\conSubtitulos.pl" tmp.lis "%FOLDER0%" "%FOLDER4%" <"%FOLDER%\%NAME%iframesMP4.lis" >>"%FOLDER%\copiar4.bat"

del tmp.lis
mkdir "%FOLDER4%"
call "%FOLDER%\copiar4.bat"
echo subtitulados+I-frames+1framePorPlanoEscena-redundantesJPG: >> "%FOLDER%\%NAME%.log"
dir /b "%FOLDER4%\*.jpg" | "%FOLDERSW%\GnuWin32\bin\wc.exe" -l >> "%FOLDER%\%NAME%.log"

del "%FOLDER%\%NAME%.mp4"

pause A MANO: conda activate tf
python "%FOLDERSW%\ina_speech_segmenter.py" -i "%FOLDER%/%NAME%.mp3" -g true -o . -b "%FOLDERSW%\ffmpeg.exe"
pause
perl "%FOLDERSW%\label2srt.pl" <"%NAME%.csv" >"%FOLDER%/%NAME%-SEGMENTATION.srt" 
::pause
perl "%FOLDERSW%\srt2script.pl" "%NAME%" %EXTENS% <"%FOLDER%\%NAME%-SEGMENTATION.srt" >"%FOLDER%/%NAME%-SEGMENTATION.bat"

exit
