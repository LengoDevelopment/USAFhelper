import discord
from discord.ext import commands

import tracemalloc
tracemalloc.start()


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
    await ctx.send(f"Pong! 🏓 \nLatency: {round(bot.latency * 1000)}ms")

@bot.command()
async def owner(ctx):
    await ctx.send(f"<@891615297071624212> is the owner of me!")

@bot.command()
async def say(ctx, *, message):
    await ctx.message.delete()
    
    message = message.replace("**", "@everyone")
    
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
   wait(5)

   await ctx.send(f"Channel: <#{ctx.channel.id}>\nServer: {ctx.guild.name}\nUsage: <@{ctx.author.id}>")

@bot.command()
async def info(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        title="Bot Commands",
        description="`!hello`\n> Says hellow to the user who intially ran the command.\n\n`!ping`\n> Gives the latenency of the bot.\n\n`!owner`\n> Informs you of the bot owner.\n\n`!say [MSG]`\n> Makes the bot say something. Use ** to mention @everyone!",
        color=discord.Color.yellow()
    )
    await ctx.send(embed=embed)

@bot.command()
async def ready(ctx, member: discord.Member):
    # Delete the command message
    await ctx.message.delete()
    
    # Ping the member as a normal message
    await ctx.send(f"{member.mention}, please read the ticket closure information below:")
    
    # Send the embed
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


bot.run("MTQxNzc3MDI0OTAwODE4OTQ0MA.GN-BCj.57BkV4GFg1D-yoBtWpy_qhz4Z1nNXuLKVr43Tw")
