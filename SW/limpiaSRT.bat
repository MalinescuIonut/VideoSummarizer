@echo off
set USER=gth
::set USER=jmmm
set "FOLDERSW=C:\Users\%USER%\Google Drive\SW"
set "FOLDERPERL=C:\Perl64\bin"
set "FILE=LaFemmeInfidele1969Chabrol.srt"
::FILM
::"%FOLDERPERL%\perl" "%FOLDERSW%\limpiaSRT.pl" < "%FILE%.old" > "%FILE%"
"%FOLDERPERL%\perl" "%FOLDERSW%\srtNO.pl" < "%FILE%.old" > "%FILE%"
pause
