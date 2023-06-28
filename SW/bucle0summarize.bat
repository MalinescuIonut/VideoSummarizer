set NAME=%1
set FOLDER=%2
set FOLDER2=%3
set FOLDER3=%4
set USER=%5
set THRESHOLD=%6
set FOLDER0=%7
set FOLDER4=%8

set "FOLDERSW=C:\Users\%USER%\Google Drive\SW"

"%FOLDERSW%\ffmpeg.exe" -i "%FOLDER%\%NAME%.mp4" -filter_complex "select='eq(pict_type,PICT_TYPE_I)'" -vsync vfr -y %NAME%dep.avi 2> %FOLDER%\%NAME%iframesMP4.dep 
"%FOLDERSW%\grep.exe" "frame=" "%FOLDER%\%NAME%iframesMP4.dep" | "%FOLDERSW%\grep.exe" "time=[0-9]*\:[0-9]*\:[0-9.]*" -o | "%FOLDERSW%\grep.exe" "[0-9]*\:[0-9]*\:[0-9.]*" -o | perl "%FOLDERSW%\iframes.pl" >%FOLDER%\%NAME%iframesMP4.lis

"%FOLDERSW%\ffmpeg.exe" -i "%FOLDER%\%NAME%.mpg" -filter_complex "select='eq(pict_type,PICT_TYPE_I)'" -vsync vfr -y %NAME%dep.avi 2> %FOLDER%\%NAME%iframesMPG.dep 
"%FOLDERSW%\grep.exe" "frame=" "%FOLDER%\%NAME%iframesMPG.dep" | "%FOLDERSW%\grep.exe" "time=[0-9]*\:[0-9]*\:[0-9.]*" -o | "%FOLDERSW%\grep.exe" "[0-9]*\:[0-9]*\:[0-9.]*" -o | perl "%FOLDERSW%\iframes.pl" >%FOLDER%\%NAME%iframesMPG.lis

if exist %FOLDER%\%NAME%.mp4 (
echo hay mp4
::pause
goto SINAVI
)

if exist %FOLDER%\%NAME%.mpg (
echo hay mpg
goto SINAVI
)

"%FOLDERSW%\ffmpeg.exe" -i "%FOLDER%\%NAME%.avi" -filter_complex "select='eq(pict_type,PICT_TYPE_I)'" -vsync vfr -y %NAME%dep.avi 2> %FOLDER%\%NAME%iframesAVI.dep 
"%FOLDERSW%\grep.exe" "frame=" "%FOLDER%\%NAME%iframesAVI.dep" | "%FOLDERSW%\grep.exe" "time=[0-9]*\:[0-9]*\:[0-9.]*" -o | "%FOLDERSW%\grep.exe" "[0-9]*\:[0-9]*\:[0-9.]*" -o | perl "%FOLDERSW%\iframes.pl" >%FOLDER%\%NAME%iframesAVI.lis

"%FOLDERSW%\ffmpeg.exe" -i "%FOLDER%\%NAME%.mkv" -filter_complex "select='eq(pict_type,PICT_TYPE_I)'" -vsync vfr -y %NAME%dep.mkv 2> %FOLDER%\%NAME%iframesMKV.dep 
"%FOLDERSW%\grep.exe" "frame=" "%FOLDER%\%NAME%iframesMKV.dep" | "%FOLDERSW%\grep.exe" "time=[0-9]*\:[0-9]*\:[0-9.]*" -o | "%FOLDERSW%\grep.exe" "[0-9]*\:[0-9]*\:[0-9.]*" -o | perl "%FOLDERSW%\iframes.pl" >%FOLDER%\%NAME%iframesMKV.lis

:SINAVI
::copy *.jpg %FOLDER0%\
::del *.jpg
del %NAME%dep.avi %NAME%dep.mp4 %NAME%dep.mpg %NAME%dep.mkv
copy %NAME%iframes*.txt %FOLDER%\
del %NAME%iframes*.txt

FOR /F %%A IN (%FOLDER%\%NAME%iframesAVI.lis) DO (
"%FOLDERSW%\ffmpeg.exe" -ss %%A -i "%FOLDER%\%NAME%.avi" -vf "drawtext=fontsize=10:fontcolor=yellow:box=1:boxcolor=black:x=(W-tw)/4:y=H-th-2: text='Time\: %%A'" -vframes 1 -vsync vfr -y "%FOLDER0%\%%A-%NAME%-IFRAME.jpg"
)

FOR /F %%A IN (%FOLDER%\%NAME%iframesMKV.lis) DO (
"%FOLDERSW%\ffmpeg.exe" -ss %%A -i "%FOLDER%\%NAME%.mkv" -vf "drawtext=fontsize=10:fontcolor=yellow:box=1:boxcolor=black:x=(W-tw)/4:y=H-th-2: text='Time\: %%A'" -vframes 1 -vsync vfr -y "%FOLDER0%\%%A-%NAME%-IFRAME.jpg"
)

FOR /F %%A IN (%FOLDER%\%NAME%iframesMPG.lis) DO (
"%FOLDERSW%\ffmpeg.exe" -ss %%A -i "%FOLDER%\%NAME%.mpg" -vf "drawtext=fontsize=10:fontcolor=yellow:box=1:boxcolor=black:x=(W-tw)/4:y=H-th-2: text='Time\: %%A'" -vframes 1 -vsync vfr -y "%FOLDER0%\%%A-%NAME%-IFRAME.jpg"
)

FOR /F %%A IN (%FOLDER%\%NAME%iframesMP4.lis) DO (
"%FOLDERSW%\ffmpeg.exe" -ss %%A -i "%FOLDER%\%NAME%.mp4" -vf "drawtext=fontsize=10:fontcolor=yellow:box=1:boxcolor=black:x=(W-tw)/4:y=H-th-2: text='Time\: %%A'" -vframes 1 -vsync vfr -y "%FOLDER0%\%%A-%NAME%-IFRAME.jpg"
)

echo IFRAMES: >>%FOLDER%\%NAME%.log
dir /b "%FOLDER0%\*.jpg" | "%FOLDERSW%\GnuWin32\bin\wc.exe" -l >>%FOLDER%\%NAME%.log
::pause
start "bucle1" call "%FOLDERSW%\bucle1summarize.bat" %NAME% %FOLDER% %FOLDER2% %FOLDER3% %USER% %THRESHOLD% %FOLDER0% %FOLDER4%

exit

::"C:\Users\gth\Google Drive\SW\ffmpeg.exe" -i "summarizedTempestadSobreAsia1928\TempestadSobreAsia1928.avi" -filter_complex "select='eq(pict_type,PICT_TYPE_I)',metadata=print:file=TempestadSobreAsia1928iframesAVI.txt" -vsync vfr -y TempestadSobreAsia1928dep.avi   2>summarizedTempestadSobreAsia1928\TempestadSobreAsia1928iframesAVI.dep

::"C:\Users\gth\Google Drive\SW\ffmpeg.exe" -ss 0.65 -i "summarizedTempestadSobreAsia1928\TempestadSobreAsia1928.avi" -vf "drawtext=fontsize=10:fontcolor=yellow:box=1:boxcolor=black:x=(W-tw)/4:y=H-th-2: text='Time\: 00:53:07.43'" -vframes 1 -vsync vfr -y "summarized0TempestadSobreAsia1928\00:53:07.43-TempestadSobreAsia1928.jpg" 
