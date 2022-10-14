@echo off
COLOR 3
title Control.py
for /f "delims=: tokens=*" %%A in ('findstr /b ::: "%~f0"') do @echo(%%A
echo;
setlocal EnableDelayedExpansion
for /f %%a in ('copy /Z "%~f0" nul') do set "CR=%%a"
for /L %%n in (3 -1 1) do (
  <nul set /P "=[CONTROL] The required Dependencies will be installed in [%%n] seconds!CR!"
  ping -n 2 localhost > nul
)

cls
pip install -r requirements.txt
cls
for /f "delims=: tokens=*" %%A in ('findstr /b ::: "%~f0"') do @echo(%%A
call :bluePrint [CONTROL] - developed by Swe4r
echo;
call :bluePrint [CONTROL] - Installed dependencies successfully!

echo;
echo press any key to exit...
pause > nul

exit

:bluePrint
powershell -Command Write-Host "%*" -foreground "Red"


:::					   _____          __           __
:::					  / ___/__  ___  / /________  / /
:::					 / /__/ _ \/ _ \/ __/ __/ _ \/ / 
:::					 \___/\___/_//_/\__/_/  \___/_/     
:::	                                  
:::		  		     |==================================|
:::




