@echo off
set USER=gth
set "FOLDERSW=C:\Users\%USER%\Google Drive\SW"
set "FOLDERPERL=C:\Perl64\bin"
set "FILE=HistoriasExtraordinarias2008Llinas.srt"
::FILM
"%FOLDERPERL%\perl" "%FOLDERSW%\renumeraSRT.pl" < "%FILE%.SINNUM" > "%FILE%"
pause
