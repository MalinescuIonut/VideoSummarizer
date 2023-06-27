set USER=gth
set "FOLDERSW=C:\Users\%USER%\Google Drive\SW"
goto ATAJO
mkdir shotTypes
FOR /F %%A IN (shotTypes.lis) DO (
echo %%A
call "%FOLDERSW%\downloadLoop.bat" shotTypes %%A 
)
::pause

:ATAJO
mkdir cinematographers
FOR /F %%A IN (cinematographers.lis) DO (
echo %%A
call "%FOLDERSW%\downloadLoop.bat" cinematographers %%A 
)

mkdir directors
FOR /F %%A IN (directors.lis) DO (
echo %%A
call "%FOLDERSW%\downloadLoop.bat" directors %%A 
)
