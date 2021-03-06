#!/usr/bin/env python3
#__main__.py

#imports
import os, discord, re
from discord.ext import commands
from dotenv import load_dotenv
from botBrainsClass import bot_brains



def main():
    ###using a subclass
    class QuirtisBotClient(discord.Client):
        async def on_ready(self):
            print(f'{client.user} has connected to Discord!')
            
            ###diff methods for finding guild membership
            guild = discord.utils.get(client.guilds, name=GUILD)

            # guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)

            # for guild in client.guilds:
            #     if guild.name == GUILD:
            #         break
            ###end diff methods
            
            print(f'{client.user} is connected to the following guild:\n{guild.name}(id: {guild.id})\n')

            members = '\n - '.join([member.name for member in guild.members])
            print(f'Guild Members:\n - {members}')

            #two methods for finding channels
            channel = discord.utils.get(guild.channels, name='general')
            # channel = client.get_channel(818616194931228686)
            
            await channel.send("I'm here!")
        
        async def on_message(self, message):
            #check to make sure the bot isnt' responding to itself.
            if message.author == client.user:
                return

            #a statment to kill the bot for good.
            if message.content == "kill QuirtisBot!":
                await message.channel.send("I'm dead.")
                await client.close()    

            #a statment to detect miro
            if re.search(r"\bQuirtisBot\b", message.content, re.IGNORECASE) or re.search(r".818611808734674964.", message.content, re.IGNORECASE):
                #checks for miro
                if message.author.id == 195671482653736961:
                #checks for me
                #if message.author.id == 143216784802054144:
                    await message.channel.send("Papa?")
                    return
                else:
                    await message.channel.send("You ain't my dad.")
                    return

            #check the message.content for certain phrases
            output = current_bot_brains.message_checker(message)
            if output != "":
                await message.channel.send(output)

    #grabbing the func need to run the bot
    current_bot_brains = bot_brains()

    #connection to discord
    print("-----------Looking for env file------------")
    try:
        with open(r"token.env", "r") as env_file:
            print("Found env file.")
        current_bot_brains.refresh_adj_list()      
    except IOError:
        print("File named 'token.env' not found. Creating file...please fill out with correct info.\n")
        with open(r"token.env", "w") as env_file:
            env_file.write("#token.env\nDISCORD_TOKEN=\nDISCORD_GUILD=")
        exit()
    load_dotenv('token.env')
    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD = os.getenv('DISCORD_GUILD')
    print("Connecting to discord...\n")

    client = QuirtisBotClient()
    client.run(TOKEN)

if __name__ == "__main__":
    main()

###using a decorator
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

#https://discord.com/api/oauth2/authorize?client_id=818611808734674964&permissions=2148005952&scope=bot
#https://discordpy.readthedocs.io/en/latest/api.html#
