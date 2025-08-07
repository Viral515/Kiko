# Получаем запрос из аргумента
param([string]$Query)

if (-not $Query) {
    Write-Host "❌ Нет запроса для поиска"
    exit 1
}

# Кодируем запрос для URL
Add-Type -AssemblyName System.Web
$encodedQuery = [System.Web.HttpUtility]::UrlEncode($Query)

# Формируем URL
$url = "https://yandex.ru/search/?text=$encodedQuery"

# Открываем
Start-Process $url

Write-Host "✅ Поиск: $Query"