import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import telegram
from telegram.error import BadRequest

# Load environment variables from .env file
load_dotenv()

# Fetch Discord bot token from environment variable
discord_token = os.getenv('DISCORD_BOT_TOKEN')
print(f"DISCORD_BOT_TOKEN fetched from environment: {discord_token}")

# Initialize Discord bot with intents
intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent
bot = commands.Bot(command_prefix='!', intents=intents)

# Telegram bot setup
telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
telegram_bot = telegram.Bot(token=telegram_token)
telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    try:
        # Mirror message to Telegram
        await telegram_bot.send_message(chat_id=telegram_chat_id, text=message.content)
    except BadRequest as e:
        print(f'Error sending message to Telegram: {e}')

    await bot.process_commands(message)

# Start the Discord bot
print("Starting bot...")
bot.run(discord_token)
