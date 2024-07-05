import discord
from discord.ext import commands
import telegram

# Discord bot token
TOKEN = 'MTI1ODM3ODEwMzMwMzE4MDM2OQ.G6WQ14.hjo-dwTHJd5E1ROKyFI4TXsekn1xC5pAHdeyKk'

# Telegram bot token and chat ID
telegram_bot_token = '7293674303:AAHkx99AFtATHQjjEL7TQDWsqlEM7AnPdFY'
telegram_chat_id = '-4207858086'

# Initialize Discord bot with intents
intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print('Telegram and Discord bot connected successfully!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Check if the message content is empty or whitespace
    if not message.content.strip():
        return

    # Send the message to Telegram
    try:
        telegram_bot = telegram.Bot(token=telegram_bot_token)
        await telegram_bot.send_message(chat_id=telegram_chat_id, text=message.content)
    except Exception as e:
        print(f'Error sending message to Telegram: {e}')
    else:
        print(f'Successfully sent message to Telegram: {message.content}')

    await bot.process_commands(message)  # Ensure commands are processed

bot.run(TOKEN)
