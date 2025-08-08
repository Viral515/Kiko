@echo off
echo Настройка автозапуска Kiko Voice Assistant...

REM Создаем ярлык в папке автозагрузки
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SCRIPT_PATH=%~dp0start_kiko_hidden.vbs"

REM Создаем ярлык
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%STARTUP_FOLDER%\Kiko Voice Assistant.lnk'); $Shortcut.TargetPath = 'wscript.exe'; $Shortcut.Arguments = '\"%SCRIPT_PATH%\"'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Description = 'Kiko Voice Assistant'; $Shortcut.Save()"

echo ✅ Автозапуск настроен!
echo Иконка появится в трее при следующем запуске Windows
pause
