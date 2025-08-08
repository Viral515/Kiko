# Запуск игр в Steam
param(
    [string]$GameName,
    [string]$SteamPath = "C:\Program Files (x86)\Steam\steam.exe"
)

# Словарь игр с их Steam App ID
$games = @{
    "dota" = "570"
    "дота" = "570"
    "dota 2" = "570"
    "дота 2" = "570"
    "portal 2" = "620"
    "портал 2" = "620"
    "nightraign" = "2622380"
}

# Функция для поиска игры
function Find-Game {
    param([string]$Name)
    
    $normalizedName = $Name.ToLower().Trim()
    
    foreach ($game in $games.GetEnumerator()) {
        if ($game.Key -like "*$normalizedName*" -or $normalizedName -like "*$($game.Key)*") {
            return $game.Value
        }
    }
    return $null
}

# Функция для запуска игры
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

# Основная логика
if ($GameName) {
    $appId = Find-Game -Name $GameName
    
    if ($appId) {
        $success = Launch-SteamGame -AppId $appId
        if ($success) {
            Write-Host "Game '$GameName' is launching..."
        }
    } else {
        Write-Host "Game '$GameName' not found in list"
        Write-Host "Available games:"
        $games.GetEnumerator() | ForEach-Object {
            Write-Host "  - $($_.Key)"
        }
    }
} else {
    Write-Host "No game name specified"
    Write-Host "Usage: .\launch_game.ps1 -GameName 'game name'"
}