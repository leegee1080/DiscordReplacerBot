#replacerbot.py
import os, discord

from dotenv import load_dotenv

load_dotenv('token.env')
TOKEN = os.getenv('DISCORD_TOKEN')


client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)

#test working
#https://realpython.com/how-to-make-a-discord-bot-python/