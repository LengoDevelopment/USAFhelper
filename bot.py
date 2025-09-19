import discord
from discord.ext import commands
from flask import Flask, request
from threading import Thread
import os, sys

# Enable message content intent
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await bot.change_presence(
        activity=discord.Game(name="Created by SightedHavoc")
    )

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention} 👋")

@bot.command()
async def ping(ctx):
    await ctx.message.delete()
    await ctx.send(f"Pong! 🏓 \nLatency: {round(bot.latency * 1000)}ms")

@bot.command()
async def owner(ctx):
    await ctx.send(f"<@891615297071624212> is the owner of me!")

@bot.command()
async def say(ctx, *, message):
    await ctx.message.delete()
    message = message.replace("%%", "@everyone")
    await ctx.send(message)

@bot.command()
async def cmds(ctx):
    await ctx.message.delete()

    embed = discord.Embed(
        title="Bot Commands",
        description="""`!hello` -> Pings and greets the user that used the command.

`!ping` -> Gives you the latency that the bot is running on.

`!owner` -> Informs you of the owner.

`!say [Message]` -> Allows you to make the bot say something.

`!ad` -> Sends the USAF ad.

`!rawad` -> Sends the direct copy-and-paste style version of the USAF ad.
""",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

@bot.command()
async def cinfo(ctx):
    await ctx.message.delete()
    await ctx.send(f"Channel: <#{ctx.channel.id}>\nServer: {ctx.guild.name}\nUsage: <@{ctx.author.id}>")

@bot.command()
async def info(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        title="Bot Commands",
        description="`!hello`\n> Says hello to the user who initially ran the command.\n\n"
                    "`!ping`\n> Gives the latency of the bot.\n\n"
                    "`!owner`\n> Informs you of the bot owner.\n\n"
                    "`!say [MSG]`\n> Makes the bot say something. Use %% to mention @everyone!\n\n"
                    "`!ad`\n> Posts our ad for USAF.\n\n"
                    "`!rawad`\n> Posts our ad with a easy copy and paste meathod!\n\n"
                    "`!shutdown`\n> Allows the owner to shut the bot down.",
        color=discord.Color.yellow()
    )
    await ctx.send(embed=embed)

@bot.command()
async def ready(ctx, member: discord.Member):
    await ctx.message.delete()
    await ctx.send(f"{member.mention}, please read the ticket closure information below:")

    embed = discord.Embed(
        title="Ticket Closure",
        description="Greetings, we are going to close this ticket in `24 hours`. "
                    "Please, ensure that you inform us if we can help you with anything else, "
                    "failure to do so will result in the ticket being closed.\n\n"
                    "*Thank you,*\nUSAF Support",
        color=discord.Color.yellow()
    )
    await ctx.send(embed=embed)

@bot.command()
async def ad(ctx):
    await ctx.message.delete()
    await ctx.send(f"""# 📢 ATTENTION RECRUITS & LEADERS 📢

🇺🇸 The United States Armed Forces is gearing up for our next big chapter — our Roblox military game is in development and YOU can be part of it!

💥 We’re recruiting for ALL positions! 💥

🛡 Moderators – Keep the community safe & strong
🏛 Presidential Cabinet Members – Lead our nation to glory
🎖 Officers & Enlisted Members – Join divisions, train, and rise through the ranks

🎯 Why join now?

* | Be a founding member before the game launches!

* | Help shape the future of our divisions & government

* | Early members get priority roles & special recognition

⚠ NOTE: Everything is subject to change as we grow — this is your chance to be here from day one!

📅 Enlist today, serve tomorrow, lead forever.
🔗https://discord.gg/JRKhxy8fQ9""")

@bot.command()
async def rawad(ctx):
    await ctx.message.delete()
    await ctx.send(f"""```# 📢 ATTENTION RECRUITS & LEADERS 📢

🇺🇸 The United States Armed Forces is gearing up for our next big chapter — our Roblox military game is in development and YOU can be part of it!

💥 We’re recruiting for ALL positions! 💥

🛡 Moderators – Keep the community safe & strong
🏛 Presidential Cabinet Members – Lead our nation to glory
🎖 Officers & Enlisted Members – Join divisions, train, and rise through the ranks

🎯 Why join now?

* | Be a founding member before the game launches!

* | Help shape the future of our divisions & government

* | Early members get priority roles & special recognition

⚠ NOTE: Everything is subject to change as we grow — this is your chance to be here from day one!

📅 Enlist today, serve tomorrow, lead forever.
🔗https://discord.gg/JRKhxy8fQ9```""")

@bot.command()
@commands.is_owner()
async def emma(ctx):
    await ctx.message.delete()
    await ctx.send(f"Reasons why <@891615297071624212> loves Emma:")

    embed = discord.Embed(
        title="Emma's Love List",
        description="> 1. Smile\n> 2. Eyes\n> 3. Laugh\n> 4. Empathy\n> 5. Generosity\n"
                    "> 6. Jokes\n> 7. Sarcasm\n> 8. Communication\n> 9. Giving\n"
                    "> 10. Forgiveness\n> 11. Clingy\n> 12. Love Language = Physical Touch\n> 13. Overall Personality",
        color=discord.Color.pink()
    )
    await ctx.send(embed=embed)

# ------------------------------
# Clean Shutdown
# ------------------------------
@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("👋 Shutting down...")

    # Shut down Discord bot
    await bot.close()

@shutdown.error
async def shutdown_error(ctx, error):
    print("Imporper Permissions Raised")
    if isinstance(error, commands.NotOwner):
        await ctx.send("> 🚫 You don’t have permission to use this command.")

    # Shut down Flask server if running
    func = request.environ.get("werkzeug.server.shutdown")
    if func:
        func()

    # Kill the script completely
    sys.exit(0)

@bot.command()
async def say(ctx, member: discord.Member, *, message):
    """
    DMs a mentioned user and notifies the channel.
    Usage: !say @user Your message here
    """
    await ctx.message.delete()  # Remove the command message

    try:
        # Send DM to the mentioned member
        await member.send(message)
        # Notify in the channel
        await ctx.send(f"✅ DM sent to {member.mention}", delete_after=5)
    except discord.Forbidden:
        # Cannot DM the user (privacy settings)
        await ctx.send(f"❌ Could not DM {member.mention}. They might have DMs disabled.", delete_after=5)



@bot.event
async def on_command_error(ctx, error):
    await ctx.message.delete()
    if hasattr(ctx.command, "on_error"):
        return

    # Command not found
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"❌ `{ctx.message.content}` is not a valid command.", delete_after=5)
        return

    # Missing required arguments
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing argument: `{error.param.name}` for command `{ctx.command}`.", delete_after=5)
        return

    # Bad argument type
    if isinstance(error, commands.BadArgument):
        await ctx.send(f"❌ Invalid argument for command `{ctx.command}`. {error}", delete_after=5)
        return

    # Command on cooldown
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏳ Command `{ctx.command}` is on cooldown. Try again in {round(error.retry_after, 1)} seconds.", delete_after=5)
        return

    # Missing permissions
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"🚫 You do not have permission to use `{ctx.command}`. Missing: {', '.join(error.missing_permissions)}", delete_after=5)
        return

    # Only bot owner can use
    if isinstance(error, commands.NotOwner):
        await ctx.send(f"🚫 Only the bot owner can use `{ctx.command}`.", delete_after=5)
        return

    # Other errors
    print(f"⚠️ Unexpected error in command `{ctx.command}`: {error}")
    await ctx.send(f"❌ Something went wrong with `{ctx.command}`. Check the console for details.", delete_after=5)


# Flask keep-alive
app = Flask("")

@app.route("/")
def home():
    return "Bot is alive!"

def run():
    app.run(host="0.0.0.0", port=3000)

# ------------------------------
# Optional Flask toggle
# ------------------------------
if os.getenv("RUN_FLASK", "false").lower() == "true":
    t = Thread(target=run)
    t.start()

# ------------------------------
# Run the bot safely with environment variable
# ------------------------------
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    print("❌ No Discord token found! Make sure DISCORD_TOKEN is set.")
else:
    bot.run(TOKEN)