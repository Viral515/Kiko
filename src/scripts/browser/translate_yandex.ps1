# Получаем запрос из аргумента
param([string]$Query)

if (-not $Query) {
    Write-Host "❌ Нет текста для перевода"
    exit 1
}

# Кодируем
Add-Type -AssemblyName System.Web
$encodedQuery = [System.Web.HttpUtility]::UrlEncode($Query)

# Формируем URL
$url = "https://translate.yandex.ru/?text=$encodedQuery"

# Открываем
Start-Process $url

Write-Host "✅ Перевод: $Query"