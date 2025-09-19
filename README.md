# USAFhelper Discord Bot

Quick setup and run instructions for development.

Prerequisites
- Python 3.10+ and virtualenv
- VS Code (recommended)

Setup
1. Create and activate a virtual environment in the project root (optional if you already have `venv`):

```powershell
python -m venv venv
.\venv\Scripts\Activate
pip install -r .\requirements.txt
```

2. Copy ` .env` (already present) and add your bot token:

```
DISCORD_TOKEN=YOUR_REAL_TOKEN_HERE
RUN_FLASK=false
```

Run from VS Code (interactive)
- Use the Run view and start the "Run bot.py" configuration. VS Code will load variables from `.env`.

Run in background (simple)
- Use the provided PowerShell helper to start the bot and write logs to `logs/bot.log`:

```powershell
./run_bot.ps1
```

Stopping the background bot
- Find and kill the python process, or use Task Manager.

Security
- Keep `.env` out of source control. Do not commit your token.
- Regenerate your token in the Discord Developer Portal if it leaks.

Troubleshooting
- If you see `401 Unauthorized`, your token is incorrect or revoked.
- Check `logs/bot.log` for the background run.

