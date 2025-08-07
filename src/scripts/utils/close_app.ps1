# scripts/utils/close_app.ps1
param(
    [string]$AppName
)

# 1. Закрытие по имени процесса (например, calc.exe, notepad.exe)
$process = Get-Process -Name $AppName -ErrorAction SilentlyContinue
if ($process) {
    $process | Stop-Process -Force
    Write-Host "Process named '$AppName' closed."
    exit 0
}

# 2. Закрытие по части заголовка окна (для UWP и других)
$windows = Get-Process | Where-Object {
    $_.MainWindowTitle -ne "" -and $_.MainWindowTitle -like "*$AppName*"
}

if ($windows) {
    $windows | Stop-Process -Force
    Write-Host "Window named '$AppName', closed."
    exit 0
}

Write-Host "App named '$AppName' not found."
exit 1