set USER=gth
set "FOLDERSW=C:\Users\%USER%\Google Drive\SW"
set TIPO=%1
set FILM=%2
mkdir "%TIPO%\%FILM%"
"%FOLDERSW%\bash-win32\wget64.exe" --no-check-certificate -O "%TIPO%\%FILM%\index.html" "https://shots.filmschoolrejects.com/%TIPO%/%FILM%" 
del tmp.bat
perl "%FOLDERSW%\extraeShots.pl" "%TIPO%\%FILM%" < "%TIPO%\%FILM%\index.html" >tmp.bat
call tmp.bat
"%FOLDERSW%\bash-win32\wget64.exe" --no-check-certificate -O "%TIPO%\%FILM%\index2.html" "https://shots.filmschoolrejects.com/%TIPO%/%FILM%/page/2/" 
del tmp.bat
perl "%FOLDERSW%\extraeShots.pl" "%TIPO%\%FILM%" < "%TIPO%\%FILM%\index2.html" >tmp.bat
call tmp.bat
"%FOLDERSW%\bash-win32\wget64.exe" --no-check-certificate -O "%TIPO%\%FILM%\index3.html" "https://shots.filmschoolrejects.com/%TIPO%/%FILM%/page/3/" 
del tmp.bat
perl "%FOLDERSW%\extraeShots.pl" "%TIPO%\%FILM%" < "%TIPO%\%FILM%\index3.html" >tmp.bat
call tmp.bat
"%FOLDERSW%\bash-win32\wget64.exe" --no-check-certificate -O "%TIPO%\%FILM%\index4.html" "https://shots.filmschoolrejects.com/%TIPO%/%FILM%/page/4/" 
del tmp.bat
perl "%FOLDERSW%\extraeShots.pl" "%TIPO%\%FILM%" < "%TIPO%\%FILM%\index4.html" >tmp.bat
call tmp.bat
"%FOLDERSW%\bash-win32\wget64.exe" --no-check-certificate -O "%TIPO%\%FILM%\index5.html" "https://shots.filmschoolrejects.com/%TIPO%/%FILM%/page/5/" 
del tmp.bat
perl "%FOLDERSW%\extraeShots.pl" "%TIPO%\%FILM%" < "%TIPO%\%FILM%\index5.html" >tmp.bat
call tmp.bat
"%FOLDERSW%\bash-win32\wget64.exe" --no-check-certificate -O "%TIPO%\%FILM%\index6.html" "https://shots.filmschoolrejects.com/%TIPO%/%FILM%/page/6/" 
del tmp.bat
perl "%FOLDERSW%\extraeShots.pl" "%TIPO%\%FILM%" < "%TIPO%\%FILM%\index6.html" >tmp.bat
call tmp.bat
"%FOLDERSW%\bash-win32\wget64.exe" --no-check-certificate -O "%TIPO%\%FILM%\index7.html" "https://shots.filmschoolrejects.com/%TIPO%/%FILM%/page/7/" 
del tmp.bat
perl "%FOLDERSW%\extraeShots.pl" "%TIPO%\%FILM%" < "%TIPO%\%FILM%\index7.html" >tmp.bat
call tmp.bat
"%FOLDERSW%\bash-win32\wget64.exe" --no-check-certificate -O "%TIPO%\%FILM%\index8.html" "https://shots.filmschoolrejects.com/%TIPO%/%FILM%/page/8/" 
del tmp.bat
perl "%FOLDERSW%\extraeShots.pl" "%TIPO%\%FILM%" < "%TIPO%\%FILM%\index8.html" >tmp.bat
call tmp.bat
"%FOLDERSW%\bash-win32\wget64.exe" --no-check-certificate -O "%TIPO%\%FILM%\index9.html" "https://shots.filmschoolrejects.com/%TIPO%/%FILM%/page/9/" 
del tmp.bat
perl "%FOLDERSW%\extraeShots.pl" "%TIPO%\%FILM%" < "%TIPO%\%FILM%\index9.html" >tmp.bat
call tmp.bat
"%FOLDERSW%\bash-win32\wget64.exe" --no-check-certificate -O "%TIPO%\%FILM%\index10.html" "https://shots.filmschoolrejects.com/%TIPO%/%FILM%/page/10/" 
del tmp.bat
perl "%FOLDERSW%\extraeShots.pl" "%TIPO%\%FILM%" < "%TIPO%\%FILM%\index10.html" >tmp.bat
call tmp.bat

