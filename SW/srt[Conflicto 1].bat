@echo off
set USER=gth
::set USER=jmmm
set "FOLDERSW=C:\Users\%USER%\Google Drive\SW"
::set "FOLDERPERL=C:\Perl64\bin\"
set "FOLDERPERL="
set "FILE=DonQuijoteCabalgaDeNuevo1973Gavaldon.srt"
::FILM
set H1=0
set M1=6
set S1=15.5
::SRT
set H2=0
set M2=6
set S2=28.0
::FILM
set H3=2
set M3=7
set S3=53.5
::SRT
set H4=2
set M4=8
set S4=42.0
::A1-(B2-delay)*NUMDEN=0
::A3-(B4-delay)*NUMDEN=0
::A1-A3-(B2-B4)*NUMDEN=0
::NUMDEN=(A1-A3)/(B2-B4)
::delay=B1-(A1/NUMDEN)
"%FOLDERPERL%perl" -e "$varA1=%H1%*3600+%M1%*60+%S1%;$varB2=%H2%*3600+%M2%*60+%S2%;$varA3=%H3%*3600+%M3%*60+%S3%;$varB4=%H4%*3600+%M4%*60+%S4%;$desajuste1=$varA1-$varB2;printf stdout \"###desajuste1=$desajuste1\n\"; $desajuste2=$varA3-$varB4; printf stdout \"###desajuste2=$desajuste2\n\";" >RESULT.dep
::type RESULT.dep
"%FOLDERPERL%perl" -e "$varA1=%H1%*3600+%M1%*60+%S1%; $varB2=%H2%*3600+%M2%*60+%S2%; $varA3=%H3%*3600+%M3%*60+%S3%; $varB4=%H4%*3600+%M4%*60+%S4%; $NUMDEN=($varA1-$varA3)/($varB2-$varB4); $delay=$varB2-$varA1/$NUMDEN; $desajuste1=$varA1-($varB2-$delay)*$NUMDEN; printf stdout \"#desajuste1=$desajuste1\n\"; $desajuste2=$varA3-($varB4-$delay)*$NUMDEN; printf stdout \"#desajuste2=$desajuste2\n\"; printf stdout \"\$DELAY=$delay;\n\";printf stdout \"\$NUM=$NUMDEN;\n\$DEN=1;\n\"; " >RESULT.dep
type RESULT.dep
::pause
type RESULT.dep > srtOLD.pl
type "%FOLDERSW%\srt.pl" >> srtOLD.pl
del RESULT.dep
::type srtOLD.pl
::pause

::set DELAY=0
::set NUM=1
::set DEN=1
::"%FOLDERPERL%\perl" srt.pl %DELAY% %NUM% %DEN% < %FILE%.old > %FILE%
"%FOLDERPERL%perl" srtOLD.pl < "%FILE%.old" > "%FILE%"
"%FOLDERPERL%perl" "%FOLDERSW%\srtNO.pl" < "%FILE%" > "%FILE%".srtNO
pause
del srtOLD.pl
