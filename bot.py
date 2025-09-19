import discord
from discord import app_commands
from flask import Flask
from threading import Thread
import os
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
        await self.tree.sync()
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