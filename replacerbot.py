#replacerbot.py
import os, discord

from dotenv import load_dotenv

print("-----------Looking for env file------------")
try:
    with open(r"token.env", "r") as env_file:
        print("Found env file.")      
except IOError:
    print("File named 'token.env' not found. Creating file...please fill out with correct info")
    with open(r"token.env", "w") as env_file:
        env_file.write("#token.env\nDISCORD_TOKEN=")
    exit()

load_dotenv('token.env')
TOKEN = os.getenv('DISCORD_TOKEN')


client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)

#test working
#https://realpython.com/how-to-make-a-discord-bot-python/