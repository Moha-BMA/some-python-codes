# Some Python Codes

A small collection of Python projects that are added to this repository one by one.

## Projects

### 1. Caesar Encryption

- Folder: `Cesar_encryption`
- Main file: `Cesar_encryption/cesar.py`
- Status: Available now
- Summary: A simple Caesar cipher example that shifts alphabetic text while keeping punctuation unchanged.
- Highlights:
  - Supports both uppercase and lowercase letters.
  - Uses modulo arithmetic to wrap around the alphabet cleanly.
  - Includes a small example that encrypts the word 'mohamed' with a shift of 3.
- Requirements:
  - Python 3

### 2. Random Word Game

- Folder: `Random Word game`
- Main file: `Random Word game/RandomWordGame.py`
- Status: Available now
- Summary: A console word guessing game inspired by Hangman.
- Highlights:
  - Chooses a random word from a small built-in word bank.
  - Shows progress after every guess and tracks remaining attempts.
  - Ends with either a victory message or the correct answer when attempts run out.
- Requirements:
  - Python 3

### 3. Search Engine

- Folder: `Search Engine`
- Main file: `Search Engine/ExaEngine.py`
- Status: Available now
- Summary: A command-line search example built with the Exa API.
- Highlights:
  - Prompts the user for a search query.
  - Fetches up to five keyword-based search results.
  - Currently filters results to the Netflix domain as a focused demo.
- Requirements:
  - Python 3
  - exa-py
  - An Exa API key

### 4. Discord Chatbot

- Folder: `discord_chatbot`
- Main file: `discord_chatbot/discord vhatbot.py`
- Status: Available now
- Summary: A starter Discord bot configured with a command prefix and message intents.
- Highlights:
  - Creates a bot with the '!' command prefix.
  - Enables basic message intents so the bot can respond to server activity.
  - Provides a minimal foundation for adding commands and events.
- Requirements:
  - Python 3
  - discord.py
  - A Discord bot token

### 5. YouTube Video Downloader

- Folder: `youtube_video_downloader`
- Main file: `youtube_video_downloader/YT.py`
- Status: Coming next
- Summary: A utility that downloads a YouTube video with yt-dlp.
- Highlights:
  - Accepts a YouTube URL and an optional output folder.
  - Downloads the best video stream up to 1080p and shows progress updates.
  - Prints the saved file path after the download finishes.
- Requirements:
  - Python 3
  - yt-dlp
