set USER=gth
set "FOLDERSW=C:\Users\%USER%\Google Drive\SW"
::"C:\Users\adjc\AppData\Local\Programs\Python\Python36-32\python.exe" simplifySubtitles.py <test.srt >video_new.srt
::"python.exe" "%FOLDERSW%\srtTiempos.py" >fileTpos.py
::type fileTpos.py
SET FICH=ImitationOfLife1959Sirk
::SET FICH=Tootsie1982Pollack
:: se preprocesa el fichero de subtítulos UTF8
perl "%FOLDERSW%\inScene.pl" %FICH%scenesMP4.lis <%FICH%.orig.srt >%FICH%.srt

"%FOLDERSW%\GnuWin32\bin\grep.exe" "frame=" %FICH%shotsORIG.dep | "%FOLDERSW%\GnuWin32\bin\egrep.exe" -o "time\=[0-9]*\:[0-9]*\:[0-9]*\.[0-9]*" | "%FOLDERSW%\GnuWin32\bin\egrep.exe" -o "[0-9]*\:[0-9]*\:[0-9]*\.[0-9]*" >%FICH%shotsORIG.lis
perl "%FOLDERSW%\inShot.pl" %FICH%shotsORIG.lis <%FICH%.orig.srt >%FICH%.srt"
pause
::"python.exe" "%FOLDERSW%\simplifySubtitles.py" 
::pause
