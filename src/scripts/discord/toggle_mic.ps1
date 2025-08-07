# Переключает микрофон в Discord через горячую клавишу
param([string]$Action)
# Discord: Ctrl+Shift+M — мут/анмьют микрофона
$wshell = New-Object -ComObject wscript.shell
$wshell.SendKeys('^(+m)')  # Ctrl+Shift+M