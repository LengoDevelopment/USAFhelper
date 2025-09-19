# Stop any python processes that are running from this project folder
Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.Path -like '*DiscordBot*' } | ForEach-Object {
    Write-Output "Stopping process $($_.Id) ($($_.Path))"
    Stop-Process -Id $_.Id -Force
}
