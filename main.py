from dotenv import load_dotenv
import logging
import time
import yt_dlp
import asyncio
from protocol.test import invokeR
from protocol.protocolParser import InputImage, GenerateImage, EditImage, LedOn
from discord import FFmpegPCMAudio
from gtts import gTTS
import os
import asyncio
import discord
from discord.ext import commands

load_dotenv()
token_discord = os.getenv("DISCORD_TOKEN")

# Logging setup
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

# Bot setup
bot = commands.Bot(command_prefix="!", intents=intents)

FFMPEG_OPTIONS = {
    'options': '-vn'
}

YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': 'True',
    'quiet': True,
    'extract_flat': False,
    'default_search': 'ytsearch1',
    'source_address': '0.0.0.0'
}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if str(message.channel) != "playground":
        return 
    
    if message.content.startswith("!ask "):
        query = message.content[len("!ask "):]
        await message.channel.send("Thinking... 💭")

        try:
            response = invokeR(query)
            # response = "Model not found."
            await message.channel.send(f"```\n{response}\n```")
        except Exception as e:
            await message.channel.send(f"fuck you, that is a stupid thing to utterfrom your vile mouth wtf.") 
    await bot.process_commands(message)



@bot.command()
async def helper(ctx):
    listCommand = ["!ledControl (n seconds)", "!helper", "!genImg (prompt)", "!analyseImg (prompt) (+file)", "!editImg (prompt) (+file)"]
    for i in listCommand:
        await ctx.send(i)

@bot.command()
async def ledControl(ctx, n:int):
    await ctx.send("Establishing the Communication")
    await ctx.send("Turned the LED on")
    LedOn(n = n)
    await ctx.send("Serial Communication Terminated")

@bot.command()
async def genImg(ctx,* , content: str):
    GenerateImage(content)
    print(content)
    file_path = os.path.join("images", "latest.png")
    try:
        with open(file_path, 'rb') as f:
            pic = discord.File(f)

            await ctx.send("working", file=pic)
    except FileNotFoundError:
        await ctx.send("Image not found, you naughty file hoarder 😈 ")

@bot.command()
async def analyseImg(ctx, *, prompt: str):
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]

        if attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            img_bytes = await attachment.read()

            await ctx.send("Unzipping image, Hold on tight.")
            try:
                response_text = InputImage(img_bytes, prompt)
                time.sleep(1)
                await ctx.send(f"{response_text}")
            except Exception as e:
                await ctx.send(f"Something broke 🧨: `{e}`")
        else:
            await ctx.send("That ain’t an image file, buddy 💀")
    else:
        await ctx.send("You forgot the pic, sweetheart")

@bot.command()
async def editImg(ctx, *, prompt: str):
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
        if attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            img_bytes = await attachment.read()

            await ctx.send("Unzipping image, Hold on tight.")
            try:
                EditImage(img_bytes, prompt)
                file_path = os.path.join("images", "generated.png")

                with open(file_path, 'rb') as f:
                    pic = discord.File(f)
                    await ctx.send("working", file=pic)

            except Exception as e:
                await ctx.send(f"Something broke 🧨: `{e}`")
        else:
            await ctx.send("That ain’t an image file, buddy 💀")
    else:
        await ctx.send("You forgot the pic, sweetheart")

@bot.command()
async def play(ctx, *, search: str):
    vc = ctx.author.voice
    if not vc:
        await ctx.send("You need to be in a voice channel to play music.")
        return

    voice_channel = vc.channel
    if ctx.voice_client is None:
        await voice_channel.connect()
    elif ctx.voice_client.channel != voice_channel:
        await ctx.voice_client.move_to(voice_channel)

    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            info = ydl.extract_info(search, download=False)
            if 'entries' in info:
                info = info['entries'][0]  # handle playlist/search
            url = info['url']
            title = info.get('title', 'Unknown Title')
        except Exception as e:
            await ctx.send(f"Error: Could not extract audio.\n```{e}```")
            return

    source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
    ctx.voice_client.stop()
    ctx.voice_client.play(source, after=lambda e: print(f"🎵 Player error: {e}") if e else None)
    await ctx.send(f"🎶 Now playing:**{title}**")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected from voice channel. Bye fucker")
    else:
        await ctx.send("Bitch you blind? I am not in any channel")

@bot.command()
async def say(ctx, *, text: str):
    user = ctx.author
    if user.voice is None:
        await ctx.send("Bruh, you gotta be in a voice channel to summon me!")
        return

    channel = user.voice.channel
    vc = ctx.voice_client

    if not vc:
        vc = await channel.connect()

    tts = gTTS(text=text, lang='en', slow=False)
    tts.save("voices\\tts-audio.mp3")

    if vc.is_playing():
        vc.stop()

    print("Playing audio now...")
    source = FFmpegPCMAudio("voices\\tts-audio.mp3")
    vc.play(source)

    # Wait until audio finishes playing
    while vc.is_playing():
        await asyncio.sleep(1)

    # Optional: disconnect after speaking
    # await vc.disconnect()

@bot.command()
async def esay(ctx, *, text: str):
    user = ctx.author
    if user.voice is None:
        await ctx.send("Bruh, you gotta be in a voice channel to summon me!")
        return

    channel = user.voice.channel
    vc = ctx.voice_client

    if not vc:
        vc = await channel.connect()

    if vc.is_playing():
        vc.stop()

    print("Playing audio now...")
    source = FFmpegPCMAudio("voices\\tts-audio.mp3")
    vc.play(source)

    # Wait until audio finishes playing
    while vc.is_playing():
        await asyncio.sleep(1)

    # Optional: disconnect after speaking
    # await vc.disconnect()


bot.run(token_discord, log_handler=handler, log_level=logging.DEBUG)

