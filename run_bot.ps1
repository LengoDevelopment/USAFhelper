# Start the bot in the background and log output to logs/bot.log
$logDir = Join-Path $PSScriptRoot 'logs'
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }
$outFile = Join-Path $logDir 'bot.log'
$errFile = Join-Path $logDir 'bot.err.log'
$python = Join-Path $PSScriptRoot 'venv\Scripts\python.exe'
$script = Join-Path $PSScriptRoot 'bot.py'

try {
	$proc = Start-Process -FilePath $python -ArgumentList "`"$script`"" -NoNewWindow -RedirectStandardOutput $outFile -RedirectStandardError $errFile -PassThru -ErrorAction Stop
	Write-Output "Started bot (PID $($proc.Id)); stdout -> $outFile, stderr -> $errFile"
} catch {
	Write-Output "Failed to start bot: $($_.Exception.Message)"
}
