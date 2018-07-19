@echo off
TITLE SQL Daemon
:start
set restarted=0
for /f "tokens=*" %%a in ('tasklist /FI "WINDOWTITLE eq 1modbusToLocal.py" ^| find /I "python.exe" /c') do set result=%%a
if %result%==0 (
  start 1modbusToLocal.py
  echo 1modbusToLocal.py restarted
  set restarted=1
)
for /f "tokens=*" %%a in ('tasklist /FI "WINDOWTITLE eq 2syncToCloud.py" ^| find /I "python.exe" /c') do set result=%%a
if %result%==0 (
  start 2syncToCloud.py
  echo 2syncToCloud.py restarted
  set restarted=1
)
if %restarted%==0 echo Both scripts up
timeout /t 15 /nobreak
GOTO :start