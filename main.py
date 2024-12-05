import discord
from discord import app_commands
from discord.ext import commands
import yt_dlp

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

#
queue = []

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You must be in a voice channel to invite me!")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send("I'm not in a voice channel!")

@bot.command()
async def play(ctx, url: str):
    if not ctx.voice_client:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await ctx.send("You must be in a voice channel to invite me!")
            return

    # YouTube
    ydl_opts = {
        'format': 'bestaudio',
        'noplaylist': True,
        'extractaudio': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['url']
            title = info['title']
            queue.append((url2, title))
            await ctx.send(f"Added to queue: {title}")

        if not ctx.voice_client.is_playing():
            await play_next(ctx)

    except Exception as e:
        await ctx.send(f"An error occurred while extracting information: {str(e)}")

async def play_next(ctx):
    if queue:
        url2, title = queue.pop(0)

        # Options
        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn -filter:a "volume=0.25"'
        }

        ctx.voice_client.play(discord.FFmpegOpusAudio(
            executable="C:/ffmpeg/bin/ffmpeg.exe",
            source=url2,
            **ffmpeg_options
        ), after=lambda e: bot.loop.create_task(play_next(ctx)))

        await ctx.send(f"Now playing: {title}")
    else:
        await ctx.send("The queue is empty.")

@bot.command()
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("Music paused.")
    else:
        await ctx.send("Nothing is playing right now.")

@bot.command(aliases=['unpause'])
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("Music resumed.")
    else:
        await ctx.send("Music is not paused.")

@bot.command()
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await play_next(ctx)
        await ctx.send("Track skipped.")
    else:
        await ctx.send("Nothing is playing right now.")

# Bot Launch
bot.run(BOT_TOKEN)
