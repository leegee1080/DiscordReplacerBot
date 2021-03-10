#replacerbot.py
import os, discord

from discord.ext import commands
from dotenv import load_dotenv

print("-----------Looking for env file------------")
try:
    with open(r"token.env", "r") as env_file:
        print("Found env file.")      
except IOError:
    print("File named 'token.env' not found. Creating file...please fill out with correct info")
    with open(r"token.env", "w") as env_file:
        env_file.write("#token.env\nDISCORD_TOKEN=\nDISCORD_GUILD=")
    exit()

load_dotenv('token.env')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

print("Connecting to discord...\n")

#using a decorator
# client = discord.Client()
#  
# @client.event
# async def on_ready():
#     print(f'{client.user} has connected to Discord!')

#     #diff methods for finding guild membership
#     guild = discord.utils.get(client.guilds, name=GUILD)

#     # guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)

#     # for guild in client.guilds:
#     #     if guild.name == GUILD:
#     #         break
    
#     print(f'{client.user} is connected to the following guild:\n{guild.name}(id: {guild.id})\n')

#     members = '\n - '.join([member.name for member in guild.members])
#     print(f'Guild Members:\n - {members}')
#     return

#using a subclass
class QuirtisBotClient(discord.Client):
    async def on_ready(self):
        print(f'{client.user} has connected to Discord!')
        
        #diff methods for finding guild membership
        guild = discord.utils.get(client.guilds, name=GUILD)

        # guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)

        # for guild in client.guilds:
        #     if guild.name == GUILD:
        #         break
        
        print(f'{client.user} is connected to the following guild:\n{guild.name}(id: {guild.id})\n')

        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')

        #two methods for finding channels
        channel = discord.utils.get(guild.channels, name='general')
        # channel = client.get_channel(818616194931228686)
        
        await channel.send("I'm here!")
    
    async def on_message(self, message):
        if message.author == client.user:
            return
        
        if message.content == "ah!":
            response = "ooh!"
            await message.channel.send(response)

        if message.content == "kill!":
            await message.channel.send("I'm dead.")
            await client.close()
        

client = QuirtisBotClient()
client.run(TOKEN)


#https://realpython.com/how-to-make-a-discord-bot-python/
#https://discordpy.readthedocs.io/en/latest/api.html#