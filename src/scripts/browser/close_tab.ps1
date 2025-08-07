# scripts/browser/close_tab.ps1
# Активирует любое окно OperaGX и закрывает вкладку

$operaKeywords = @("Opera", "OperaGX", "Opera GX", "Opera Browser")

$found = $false

foreach ($keyword in $operaKeywords) {
    # Ищем процесс с открытым окном, содержащим ключевое слово
    $window = Get-Process | Where-Object {
        $_.MainWindowTitle -like "*$keyword*" -and $_.MainWindowTitle -ne ""
    } | Select-Object -First 1

    if ($window) {
        try {
            # Активируем окно через COM
            [Microsoft.VisualBasic.Interaction]::AppActivate($window.Id)
            Start-Sleep -Milliseconds 300
            $found = $true
            break
        } catch {
            # Игнорируем ошибку, пробуем следующий ключ
        }
    }
}

if (-not $found) {
    Write-Host "Window not found"
    exit 1
}

# Отправляем Ctrl+W
$wshell = New-Object -ComObject wscript.shell
$wshell.SendKeys('^w')

Write-Host "Browser tab closed"