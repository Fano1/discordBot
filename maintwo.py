import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from gtts import gTTS
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()
token_discord = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

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
    tts.save("tts-audio.mp3")

    if vc.is_playing():
        vc.stop()

    print("Playing audio now...")
    source = FFmpegPCMAudio("tts-audio.mp3")
    vc.play(source)

    # Wait until audio finishes playing
    while vc.is_playing():
        await asyncio.sleep(1)

    # Optional: disconnect after speaking
    # await vc.disconnect()

bot.run(token_discord)
