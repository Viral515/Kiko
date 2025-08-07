# Открывает URL в браузере
param([string]$Url)
if ($Url) {
    Start-Process $Url
}