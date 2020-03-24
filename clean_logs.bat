@echo Delete log files? [y/n]
@set /p x=
@if /i %x%==y del /f /s /q *.log
pause