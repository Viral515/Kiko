# Управление микрофоном в Discord (упрощенная версия)
param(
    [string]$Action
)

# Функция для отправки горячих клавиш
function Send-Hotkey {
    param([string]$Keys)
    
    $wshell = New-Object -ComObject wscript.shell
    $wshell.SendKeys($Keys)
    Write-Host "Sent hotkey: $Keys"
}

# Функция для активации Discord (улучшенная)
function Activate-Discord {
    $discordProcesses = Get-Process | Where-Object {
        $_.ProcessName -like "*Discord*"
    }
    
    Write-Host "Found Discord processes: $($discordProcesses.Count)"
    
    if ($discordProcesses) {
        $process = $discordProcesses[0]
        Write-Host "Using process: $($process.ProcessName)"
        
        $hwnd = $process.MainWindowHandle
        Write-Host "Window handle: $hwnd"
        
        if ($hwnd -ne [IntPtr]::Zero) {
            Add-Type -TypeDefinition @"
                using System;
                using System.Runtime.InteropServices;
                public class Win32 {
                    [DllImport("user32.dll")]
                    public static extern bool SetForegroundWindow(IntPtr hWnd);
                    [DllImport("user32.dll")]
                    public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
                    [DllImport("user32.dll")]
                    public static extern bool BringWindowToTop(IntPtr hWnd);
                }
"@
            # Пробуем несколько способов активации
            [Win32]::ShowWindow($hwnd, 9)  # SW_RESTORE
            [Win32]::SetForegroundWindow($hwnd)
            [Win32]::BringWindowToTop($hwnd)
            
            Write-Host "Discord window activation completed"
            return $true
        } else {
            Write-Host "Invalid window handle"
            return $false
        }
    } else {
        Write-Host "No Discord processes found"
        return $false
    }
}

# Функция для выполнения Discord действия
function Execute-DiscordAction {
    param(
        [string]$Action,
        [string]$Hotkey,
        [string]$Description
    )
    
    Write-Host "Starting $Description for action: $Action"
    
    if (Activate-Discord) {
        Start-Sleep -Milliseconds 300
        Write-Host "Sending $Hotkey..."
        Send-Hotkey($Hotkey)
        Start-Sleep -Milliseconds 100
        Write-Host "$Description completed successfully"
    } else {
        Write-Host "Failed to activate Discord window"
    }
}

# Основная логика
if ($Action -eq "toggle") {
    Execute-DiscordAction -Action $Action -Hotkey "^(+m)" -Description "Microphone toggle"
}
elseif ($Action -eq "disconnect") {
    Execute-DiscordAction -Action $Action -Hotkey "^(+l)" -Description "Call disconnect"
}
else {
    Write-Host "Unknown action: $Action"
    Write-Host "Available actions: toggle, disconnect"
}