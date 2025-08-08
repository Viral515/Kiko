# Управление громкостью системы
param(
    [string]$Action
)

# Функция для отправки горячих клавиш
function Send-VolumeKey {
    param([string]$Key)
    
    $obj = New-Object -ComObject WScript.Shell
    $obj.SendKeys($Key)
    Start-Sleep -Milliseconds 100
}

# Основная логика
if ($Action -eq "mute") {
    Send-VolumeKey([char]173)
    Write-Host "Звук системы переключен"
}
elseif ($Action -eq "unmute") {
    Send-VolumeKey([char]173)
    Write-Host "Звук системы переключен"
}
elseif ($Action -eq "up") {
    Send-VolumeKey([char]175)
    Write-Host "Громкость увеличена"
}
elseif ($Action -eq "down") {
    Send-VolumeKey([char]174)
    Write-Host "Громкость уменьшена"
}
else {
    Write-Host "Неизвестное действие: $Action"
    Write-Host "Доступные действия: mute, unmute, up, down"
}