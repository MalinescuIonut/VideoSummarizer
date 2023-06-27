set NAME=%1
set FOLDER=%2
set FOLDER2=%3
set FOLDER3=%4
set USER=%5
set THRESHOLD=%6
set FOLDER0=%7
set FOLDER4=%8
set "FOLDERSW=C:\Users\%USER%\Google Drive\SW"

"%FOLDERSW%\ffmpeg.exe" -i "%FOLDER%\%NAME%.mpg" -filter_complex "select='gt(scene,%THRESHOLD%)',metadata=print:file=%NAME%scenesMPG.txt" -vsync vfr -y %NAME%dep.mpg 2> %FOLDER%\%NAME%scenesMPG.dep 
"%FOLDERSW%\grep.exe" "pts_time:" "%NAME%scenesMPG.txt" | "%FOLDERSW%\grep.exe" "pts_time:[0-9.]*" -o | "%FOLDERSW%\grep.exe" [0-9.]* -o | perl "%FOLDERSW%\scenes.pl" >%FOLDER%\%NAME%scenesMPG.lis

"%FOLDERSW%\ffmpeg.exe" -i "%FOLDER%\%NAME%.mp4" -filter_complex "select='gt(scene,%THRESHOLD%)',metadata=print:file=%NAME%scenesMP4.txt" -vsync vfr -y %NAME%dep.mp4 2> %FOLDER%\%NAME%scenesMP4.dep 
"%FOLDERSW%\grep.exe" "pts_time:" "%NAME%scenesMP4.txt" | "%FOLDERSW%\grep.exe" "pts_time:[0-9.]*" -o | "%FOLDERSW%\grep.exe" [0-9.]* -o | perl "%FOLDERSW%\scenes.pl" >%FOLDER%\%NAME%scenesMP4.lis

if exist %FOLDER%\%NAME%.mpg (
echo 10000.0 >> %FOLDER%\%NAME%scenesMPG.lis
goto SINAVI
)

if exist %FOLDER%\%NAME%.mp4 (
echo 10000.0 >> %FOLDER%\%NAME%scenesMP4.lis
goto SINAVI
)

"%FOLDERSW%\ffmpeg.exe" -i "%FOLDER%\%NAME%.avi" -filter_complex "select='gt(scene,%THRESHOLD%)',metadata=print:file=%NAME%scenesAVI.txt" -vsync vfr -y %NAME%dep.avi 2> %FOLDER%\%NAME%scenesAVI.dep 
"%FOLDERSW%\grep.exe" "pts_time:" "%NAME%scenesAVI.txt" | "%FOLDERSW%\grep.exe" "pts_time:[0-9.]*" -o | "%FOLDERSW%\grep.exe" [0-9.]* -o | perl "%FOLDERSW%\scenes.pl" >%FOLDER%\%NAME%scenesAVI.lis

if exist %FOLDER%\%NAME%.avi (
echo 10000.0 >> %FOLDER%\%NAME%scenesAVI.lis
goto SINAVI
)

"%FOLDERSW%\ffmpeg.exe" -i "%FOLDER%\%NAME%.mkv" -filter_complex "select='gt(scene,%THRESHOLD%)',metadata=print:file=%NAME%scenesMKV.txt" -vsync vfr -y %NAME%dep.mkv 2> %FOLDER%\%NAME%scenesMKV.dep 
"%FOLDERSW%\grep.exe" "pts_time:" "%NAME%scenesMKV.txt" | "%FOLDERSW%\grep.exe" "pts_time:[0-9.]*" -o | "%FOLDERSW%\grep.exe" [0-9.]* -o | perl "%FOLDERSW%\scenes.pl" >%FOLDER%\%NAME%scenesMKV.lis
if exist %FOLDER%\%NAME%.avi (
echo 10000.0 >> %FOLDER%\%NAME%scenesMKV.lis
goto SINAVI
)

:SINAVI
del %NAME%dep.avi %NAME%dep.mp4 %NAME%dep.mpg %NAME%dep.mkv
copy %NAME%scenes*.txt %FOLDER%\
del %NAME%scenes*.txt

FOR /F %%A IN (%FOLDER%\%NAME%scenesMP4.lis) DO (
"%FOLDERSW%\ffmpeg.exe" -ss %%A -i "%FOLDER%\%NAME%.mp4" -vf "drawtext=fontsize=10:fontcolor=yellow:box=1:boxcolor=black:x=(W-tw)/4:y=H-th-2: text='Time\: %%A'" -vframes 1 -vsync vfr -y "%FOLDER3%\%%A-%NAME%-SHOT.jpg"
)

FOR /F %%A IN (%FOLDER%\%NAME%scenesMPG.lis) DO (
"%FOLDERSW%\ffmpeg.exe" -ss %%A -i "%FOLDER%\%NAME%.mpg" -vf "drawtext=fontsize=10:fontcolor=yellow:box=1:boxcolor=black:x=(W-tw)/4:y=H-th-2: text='Time\: %%A'" -vframes 1 -vsync vfr -y "%FOLDER3%\%%A-%NAME%-SHOT.jpg"
)

FOR /F %%A IN (%FOLDER%\%NAME%scenesAVI.lis) DO (
"%FOLDERSW%\ffmpeg.exe" -ss %%A -i "%FOLDER%\%NAME%.avi" -vf "drawtext=fontsize=10:fontcolor=yellow:box=1:boxcolor=black:x=(W-tw)/4:y=H-th-2: text='Time\: %%A'" -vframes 1 -vsync vfr -y "%FOLDER3%\%%A-%NAME%-SHOT.jpg"
)

FOR /F %%A IN (%FOLDER%\%NAME%scenesMKV.lis) DO (
"%FOLDERSW%\ffmpeg.exe" -ss %%A -i "%FOLDER%\%NAME%.mkv" -vf "drawtext=fontsize=10:fontcolor=yellow:box=1:boxcolor=black:x=(W-tw)/4:y=H-th-2: text='Time\: %%A'" -vframes 1 -vsync vfr -y "%FOLDER3%\%%A-%NAME%-SHOT.jpg"
)

echo "escenasJPG" >>%FOLDER%\%NAME%.log
dir /b "%FOLDER3%\*.jpg" | "%FOLDERSW%\GnuWin32\bin\wc.exe" -l >>%FOLDER%\%NAME%.log

start "bucle4" call "%FOLDERSW%\bucle4summarize.bat" %NAME% %FOLDER% %FOLDER2% %FOLDER3% %USER% %THRESHOLD% %FOLDER0% %FOLDER4%

exit
