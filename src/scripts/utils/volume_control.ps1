param(
    [string]$Action
)

function Send-VolumeKey {
    param([string]$Key)
    
    $obj = New-Object -ComObject WScript.Shell
    $obj.SendKeys($Key)
    Start-Sleep -Milliseconds 100
}

if ($Action -eq "mute") {
    Send-VolumeKey([char]173)
}
elseif ($Action -eq "unmute") {
    Send-VolumeKey([char]173)
}