import discord
from discord import app_commands
from flask import Flask
from threading import Thread
import os
import asyncio
import aiohttp
from dotenv import load_dotenv

# Load environment variables from a local .env file (if present)
load_dotenv()

# ------------------------------
# Bot Setup
# ------------------------------
intents = discord.Intents.default()
intents.message_content = True  # needed for message content in DMs if you use them

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        GUILD_ID = 123456789012345678  # replace with your server ID
await self.tree.sync(guild=discord.Object(id=GUILD_ID))

        # Use ASCII-only startup messages to avoid Windows console encoding errors
        print("Synced all slash commands.")

client = MyClient()

# ------------------------------
# Slash Commands
# ------------------------------

@client.event
async def on_ready():
    # ASCII-only message to avoid UnicodeEncodeError on Windows consoles
    print(f"Logged in as {client.user}")
    await client.change_presence(activity=discord.Game(name="Helping USAF"))

# Hello
@client.tree.command(name="hello", description="Say hello to the bot")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.mention} 👋")

# Ping
@client.tree.command(name="ping", description="Get the bot's latency")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! 🏓\nLatency: {round(client.latency*1000)}ms")

# Owner
@client.tree.command(name="owner", description="Get the bot owner")
async def owner(interaction: discord.Interaction):
    await interaction.response.send_message("<@891615297071624212> is the owner of this bot!")

# Announce
@client.tree.command(name="announce", description="Send an announcement")
@app_commands.describe(title="The announcement title", content="The announcement content")
async def announce(interaction: discord.Interaction, title: str, content: str):
    embed = discord.Embed(title=title, description=content, color=discord.Color.green())
    await interaction.response.send_message(embed=embed)

# Info
@client.tree.command(name="info", description="Get info about the server or bot")
async def info(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title="Server Info", color=discord.Color.purple())
    embed.add_field(name="Server Name", value=guild.name, inline=False)
    embed.add_field(name="Server ID", value=guild.id, inline=False)
    embed.add_field(name="Member Count", value=guild.member_count, inline=False)
    embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.display_avatar.url)
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="ready", description="Tell a user they have to respond to a ticket within 24 hours.")
async def ready(interaction: discord.Interaction):
    embed = discord.Embed(title="Ticket Update", description="You have 24 hours to respond to this ticket before it is closed.", color=discord.Color.orange())
    embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.display_avatar.url)
    await interaction.response.send_message(embed=embed)

# Commands list (embed)
@client.tree.command(name="commands", description="List all available commands and usage")
async def commands(interaction: discord.Interaction):
    embed = discord.Embed(title="Command List", color=discord.Color.blue())
    embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.display_avatar.url)

    # Add commands as inline fields for a compact layout
    embed.add_field(name="/hello", value="Say hello to the bot", inline=True)
    embed.add_field(name="/ping", value="Get the bot's latency", inline=True)
    embed.add_field(name="/owner", value="Get the bot owner", inline=True)
    embed.add_field(name="/announce", value="<title> <content> — Send an announcement embed", inline=True)
    embed.add_field(name="/info", value="Get server info (name, id, member count)", inline=True)
    embed.add_field(name="/ready", value="Ticket update: 24 hours to respond", inline=True)
    embed.add_field(name="/dm", value="<user> <content> — Send a DM to a user", inline=True)
    embed.add_field(name="/shutdown", value="Shut down the bot (owner only)", inline=True)

    await interaction.response.send_message(embed=embed, ephemeral=True)

# DM Command
@client.tree.command(name="dm", description="Send a direct message to a user")
@app_commands.describe(user="User to DM", content="Message content")
async def dm(interaction: discord.Interaction, user: discord.User, content: str):
    try:
        await user.send(content)
        await interaction.response.send_message(f"✅ DM sent to {user.mention}", ephemeral=True)
    except:
        await interaction.response.send_message(f"❌ Could not send DM to {user.mention}", ephemeral=True)

# Shutdown (Owner only)
@client.tree.command(name="shutdown", description="Shut down the bot (owner only)")
async def shutdown(interaction: discord.Interaction):
    if interaction.user.id != 891615297071624212:  # replace with your Discord ID
        await interaction.response.send_message("❌ You are not allowed to use this command.", ephemeral=True)
        return
    await interaction.response.send_message("Shutting down...")
    await client.close()


# Render logs (owner only)
@client.tree.command(name="renderlogs", description="Fetch recent Render logs (owner only)")
async def renderlogs(interaction: discord.Interaction, lines: int = 200):
    OWNER_ID = 891615297071624212
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("You are not allowed to use this command.", ephemeral=True)
        return

    api_key = os.getenv("RENDER_API_KEY")
    service_id = os.getenv("RENDER_SERVICE_ID")
    if not api_key or not service_id:
        await interaction.response.send_message(
            "Render API key or Service ID not configured. Please set RENDER_API_KEY and RENDER_SERVICE_ID in the environment.",
            ephemeral=True
        )
        return

    # Limit lines
    try:
        lines = max(1, min(1000, int(lines)))
    except Exception:
        lines = 200

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Render logs endpoint (use service logs endpoint)
    url = f"https://api.render.com/v1/services/{service_id}/logs?limit={lines}"

    await interaction.response.defer(ephemeral=True)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=20) as resp:
                body = await resp.text()
                if resp.status != 200:
                    embed = discord.Embed(title="Render logs — error", description=f"Failed to fetch logs: HTTP {resp.status}\n{body[:900]}", color=discord.Color.red())
                    await interaction.followup.send(embed=embed, ephemeral=True)
                    return

                # Try to parse JSON, fallback to raw text
                logs_text = None
                try:
                    data = await resp.json()
                    if isinstance(data, dict) and "logs" in data and isinstance(data["logs"], str):
                        logs_text = data["logs"]
                    elif isinstance(data, dict) and "events" in data and isinstance(data["events"], list):
                        logs_text = "\n".join(str(e.get("message", e)) for e in data["events"][-lines:])
                    elif isinstance(data, list):
                        logs_text = "\n".join(str(x) for x in data[-lines:])
                    else:
                        logs_text = str(data)
                except Exception:
                    logs_text = body

                max_chars = 3800
                if len(logs_text) > max_chars:
                    truncated = "[...truncated...]\n" + logs_text[-max_chars:]
                else:
                    truncated = logs_text

                embed = discord.Embed(title="Render logs (recent)", color=discord.Color.blue())
                embed.add_field(name=f"Last {lines} lines (truncated)", value=f"```txt\n{truncated}\n```" if truncated.strip() else "(no logs)", inline=False)
                dashboard_url = f"https://dashboard.render.com/web/service/{service_id}"
                embed.set_footer(text="Click dashboard link for full logs", icon_url=interaction.user.display_avatar.url)
                embed.url = dashboard_url

                await interaction.followup.send(embed=embed, ephemeral=True)
    except asyncio.TimeoutError:
        await interaction.followup.send("Request timed out fetching Render logs.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"Unexpected error: {type(e).__name__} - {e}", ephemeral=True)


# Admin help (owner only)
@client.tree.command(name="adminhelp", description="Admin instructions for Render and bot configuration")
async def adminhelp(interaction: discord.Interaction):
    OWNER_ID = 891615297071624212
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("You are not allowed to use this command.", ephemeral=True)
        return

    embed = discord.Embed(title="Admin: Deploy & Render Help", color=discord.Color.gold())
    embed.add_field(name="Set environment variables (Render)", value=(
        "1) Open your service on Render → Environment.\n"
        "2) Add `DISCORD_TOKEN` = your bot token (secret).\n"
        "3) Add `RENDER_API_KEY` = your Render API key (secret).\n"
        "4) Add `RENDER_SERVICE_ID` = your service id.\n"
    ), inline=False)

    embed.add_field(name="How to get Render values", value=(
        "- RENDER_API_KEY: Render → Account → API Keys → Create Key.\n"
        "- RENDER_SERVICE_ID: Render → open the service → Settings → Service ID (copy).\n"
    ), inline=False)

    embed.add_field(name="Using /renderlogs", value=(
        "- Run `/renderlogs lines:50` to fetch recent logs (owner only).\n"
        "- Output is ephemeral and truncated; visit the dashboard link for full logs.\n"
    ), inline=False)

    embed.add_field(name="Security", value=(
        "- Never commit secrets to the repo. Add .env to .gitignore.\n"
        "- Rotate your Discord token if ever exposed.\n"
    ), inline=False)

    embed.set_footer(text="Admin help — keep these values secret")
    await interaction.response.send_message(embed=embed, ephemeral=True)

# ------------------------------
# Flask keep-alive (optional)
# ------------------------------
app = Flask("")

@app.route("/")
def home():
    return "Bot is alive!"

def run_flask():
    app.run(host="0.0.0.0", port=3000)

if os.getenv("RUN_FLASK", "false").lower() == "true":
    t = Thread(target=run_flask)
    t.start()

# ------------------------------
# Run Bot
# ------------------------------
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    print("❌ No Discord token found! Make sure DISCORD_TOKEN is set.")
else:
    # Safe diagnostic (do not print the token itself)
    try:
        # Safe diagnostic: do not print the token itself (only its length)
        print(f"Discord token loaded (length {len(TOKEN)}). Starting client...")
    except Exception:
        print("Discord token loaded. Starting client...")
    try:
        client.run(TOKEN)
    except Exception as e:
        # Print exception type and message but never the token
        print(f"❌ Failed to start client: {type(e).__name__} - {e}")