import discord
from discord.ext import commands

# Create an Intents object
intents = discord.Intents.default()  # You can customize this as needed
intents.messages = True  # Enable the message intent if you want to read messages

# Initialize the bot with the intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Your bot commands and events go here

# Run the bot
bot.run('PUT bot API here')