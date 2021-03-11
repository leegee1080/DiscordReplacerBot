#!/usr/bin/env python3
#replacerbot.py

#imports
import os, discord, random, re
from discord.ext import commands
from dotenv import load_dotenv

#global vars
rand_num_top = 1
adj_list = []
is_sleeping = False

##commands
#!QB ----> keyword
re_keyword = re.compile(r"\b!QB\b")

#"QB add <word> --->adds a word to the adj list
#"QB remove <word>" ---> removes a word to the adj list
#"!QB sleep" --->sleeps the bot.
#"!QB awake" --->awakens the bot.
#"!QB calm" ---> reduces the number of times the bot checks messages
re_command_check = re.compile(r"\b!QB\s(add|remove|calm|sleep|awake)\s([a-z][A-Z]*)\b")
command_dict_switch = {
    "add": word_adder,
    "remove": word_remover,
    "calm": bot_calmer,
    "sleep": bot_sleeper,
    "awake": bot_awaker
}


#"Kill QuirtisBot!" --->kills the bot..
re_kill_check = re.compile(r"\bKill QuirtisBot!\b")


#connection to discord
print("-----------Looking for env file------------")
try:
    with open(r"token.env", "r") as env_file:
        print("Found env file.")      
except IOError:
    print("File named 'token.env' not found. Creating file...please fill out with correct info.\n")
    with open(r"token.env", "w") as env_file:
        env_file.write("#token.env\nDISCORD_TOKEN=\nDISCORD_GUILD=")
    exit()

print("-----------Looking for adj file------------")
try:
    with open (r"adjectives.txt") as adj_file:
        adj_list = adj_file.readlines()
        print("Found adj file.")
except IOError:
    print("'adjectives.txt' not found.")
    exit()

load_dotenv('token.env')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
print("Connecting to discord...\n")

#functions
def message_checker(message):
    if re.search(re_keyword, message.content):
        command = re.search(re_command_check, message.content)
        command_dict_switch[command.group(1)](message, command.group(2))
        return
    if(random.randint(1, rand_num_top) == 1):
        print("I'm looking at the message!")
        new_message = adj_replacer(message.content)
        if(new_message == ""):
            return
        else:
            await message.channel.send(new_message)
            return
    return

def adj_replacer(message_content):
    print(f"starting replacer on message '{message_content}'")
    adjrep_output = ""
    for adj in adj_list:
        regex_adj = adj.rstrip("\n")
        regex_adj = regex_adj
        adj_check = re.compile(r"\b" + regex_adj + r"\b", re.IGNORECASE)
        if(adj_check.search(message_content)):
            adjrep_output = f"You're {regex_adj}."
            break
    return adjrep_output

def bot_awaker(first_param, orignal_message):
    is_sleeping = False
    return print("I'm awake.")

def bot_sleeper(first_param, orignal_message):
    is_sleeping = True
    return print("I'm asleep.")

def bot_calmer(first_param, orignal_message):
    rand_num_top = 3
    await orignal_message.channel.send("No you.")
    return print("I'm calm.")

def word_adder(word_to_add, orignal_message):
    wordadd = word_to_add
    adj_list.append(wordadd)
    with open (r"adjectives.txt", "w") as adj_file:
        adj_file.writelines(adj_list)
    await orignal_message.channel.send(f"Sure, I guess {word_to_add} is a word.")
    return print(f"'{wordadd}' added")

def word_remover(word_to_remove, orignal_message):
    wordrem = word_to_remove
    temp_list = []
    if wordrem in adj_list:
        for adj in adj_list:
            if adj != wordrem:
                temp_list.append(adj)
        with open (r"adjectives.txt", "w") as adj_file:
            adj_file.writelines(temp_list)
            adj_list = temp_list
        await orignal_message.channel.send(f"Wow, I guess {word_to_remove} isn't a word.")
        return print(f"'{wordrem}' removed")
    return print(f"'{wordrem}' is not in the list")

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

        #check the message.content for certain phrases
        message_checker(message)

        

client = QuirtisBotClient()
client.run(TOKEN)






#https://discord.com/api/oauth2/authorize?client_id=818611808734674964&permissions=2148005952&scope=bot
#https://discordpy.readthedocs.io/en/latest/api.html#
