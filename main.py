import os
import discord
from discord.ext import commands
import telegram
from telegram.error import BadRequest
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch tokens from environment variables
discord_token = os.getenv('DISCORD_BOT_TOKEN')
telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

if not discord_token:
    print("ERROR: Discord bot token not found. Please set DISCORD_BOT_TOKEN environment variable.")
    exit(1)

if not telegram_token or not telegram_chat_id:
    print("ERROR: Telegram bot token or chat ID not found. Please set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables.")
    exit(1)

print(f"DISCORD_BOT_TOKEN fetched from environment: {discord_token}")

# Initialize Discord bot with intents
intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent
bot = commands.Bot(command_prefix='!', intents=intents)

# Telegram bot setup
telegram_bot = telegram.Bot(token=telegram_token)

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
    except Exception as e:
        print(f'Unexpected error: {e}')

    await bot.process_commands(message)

@bot.event
async def on_error(event, *args, **kwargs):
    print(f'Error on event {event}: {args[0]}')

@bot.event
async def on_disconnect():
    print('Bot disconnected, attempting to reconnect...')

@bot.event
async def on_resumed():
    print('Bot resumed connection.')

# Start the Discord bot
print("Starting bot...")
bot.run(discord_token)
