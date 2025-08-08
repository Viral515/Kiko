@echo off
echo Отключение автозапуска Kiko Voice Assistant...

REM Удаляем ярлык из папки автозагрузки
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT_PATH=%STARTUP_FOLDER%\Kiko Voice Assistant.lnk"

if exist "%SHORTCUT_PATH%" (
    del "%SHORTCUT_PATH%"
    echo ✅ Автозапуск отключен!
) else (
    echo ℹ️ Автозапуск не был настроен
)

pause
