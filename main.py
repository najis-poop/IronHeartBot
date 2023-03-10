import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from common import InternalBotError, UserBotError

#load_dotenv("temp.env")
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
#TOKEN = os.getenv("TEST_TOKEN")

if TOKEN is None:
    print("You forgot to set the token in .env")
    print("if you already did go to the line `load_dotenv(\"temp.env\")` and remove")
    print("it and uncomment the line under it")
    exit(1)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=";", intents=intents)

bot.load_extensions(*(
    "davinci.playground",
    "davinci.dalle",
    "tag.tag",
))

@bot.event
async def on_ready():
    print("ready")

@bot.event
async def on_command_error(ctx: commands.Context, err: Exception):
    if isinstance(err, commands.CommandNotFound):
        await ctx.reply(embed=UserBotError(ctx, "CommandNotFound", err.args[0]))
        return
    if isinstance(err, commands.MissingRequiredArgument):
        await ctx.reply(embed=UserBotError(ctx, "MissingArgument", err.args[0]))
        return
    await ctx.reply(embed=InternalBotError(ctx, err.__class__.__name__, ','.join(err.args)))
    raise err

bot.run(TOKEN)