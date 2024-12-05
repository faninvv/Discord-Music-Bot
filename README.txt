Discord Music Bot
A simple and feature-rich Discord music bot that allows users to play music in voice channels from YouTube. The bot supports the following commands:

Features:
Join: The bot joins your voice channel when requested.
Leave: The bot disconnects from the voice channel.
Play: Play music from YouTube by providing a URL.
Pause: Pause the current track.
Resume: Resume playback from where it was paused.
Skip: Skip the current track and play the next in the queue.

Commands:
!join: Invite the bot to your voice channel.
!leave: Make the bot leave your voice channel.
!play <URL>: Play a YouTube video as audio in the voice channel.
!pause: Pause the current track.
!unpause or !resume: Resume playback.
!skip: Skip the current track and play the next one.

Requirements:
Python 3.x
discord.py: A Python wrapper for the Discord API.
yt-dlp: A tool to download YouTube videos and extract audio.

Setup:
Install required dependencies.

Add your bot token to the code and run the bot.