# Запускает приложение
param([string]$App)
if ($App) {
    Start-Process $App
}