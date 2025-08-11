param(
    [string]$AppId,
    [string]$SteamPath = "C:\Program Files (x86)\Steam\steam.exe"
)

function Launch-SteamGame {
    param([string]$AppId)
    
    if (Test-Path $SteamPath) {
        try {
            Start-Process -FilePath $SteamPath -ArgumentList "-applaunch $AppId"
            Write-Host "Launching game with App ID: $AppId"
            return $true
        } catch {
            Write-Host "Error launching game: $($_.Exception.Message)"
            return $false
        }
    } else {
        Write-Host "Steam not found at path: $SteamPath"
        return $false
    }
}

Launch-SteamGame -AppId $AppId