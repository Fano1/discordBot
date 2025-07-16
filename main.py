from dotenv import load_dotenv
import logging
import os

from protocol.protocolParser import GenerateImage

import discord
from discord.ext import commands

load_dotenv()
token_discord = os.getenv("DISCORD_TOKEN")

# Logging setup
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True

# Bot setup
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "bruh" in message.content.lower():
        await message.channel.send("hello")

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f"hello {ctx.author.mention}")

@bot.command()
async def image(ctx,* , content: str):
    GenerateImage(content)
    print(content)
    file_path = os.path.join("images", "latest.png")
    try:
        with open(file_path, 'rb') as f:
            pic = discord.File(f)
            
            await ctx.send("working", file=pic)
    except FileNotFoundError:
        await ctx.send("Image not found, you naughty file hoarder 😈 ")

bot.run(token_discord, log_handler=handler, log_level=logging.DEBUG)

