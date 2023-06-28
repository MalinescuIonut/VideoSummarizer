@echo off
::set USER=gth
set USER=jmmm
set "FOLDERSW=C:\Users\%USER%\Google Drive\SW"
::set "FOLDERPERL=C:\Perl64\bin"
set "FOLDERPERL=C:\Perl\bin"
set "FILE=ElDestinoSeDisculpa1944SaenzDeHeredia.srt"
::FILM
"%FOLDERPERL%\perl" "%FOLDERSW%\desolapaSRT.pl" < "%FILE%.SOLAPADO" > "%FILE%"
pause
