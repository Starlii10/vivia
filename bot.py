"""
    This is the primary script for Vivia.

    Vivia is licensed under the MIT License. For more information, see the LICENSE file.
    TL:DR: you can use Vivia's code as long as you keep the original license intact.
    Vivia is made open source in the hopes that you'll find her code useful.

    If you'd like to contribute, please check out the GitHub repository at https://github.com/starlii10/vivia.

    Have a great time using Vivia!
"""

import sys
import discord
from discord.ext import tasks, commands
import json
from datetime import datetime
import dotenv
import random
from os import system
import configparser
import logging
config = configparser.ConfigParser()

try:
    config.read("config.ini")
except:
    try:
        print("I didn't find a configuration file. I'm creating one for ya!")
        config.read("config.ini.example")
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    except:
        print("I couldn't create a config file. Is something wrong with config.ini.example?")
        sys.exit(1)
else:
    print("I found my configuration file. One moment...")


handler = logging.FileHandler(
    filename=config['Logging']['Filename'],
    encoding='utf-8',
    mode='w'
)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logging.basicConfig(level=logging.INFO)

system("title Vivia - " + config['General']['StatusMessage'])

print("Preparing to start up!")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='v!', intents=intents)
bot.remove_command("help")
tree = bot.tree

helpMsg = open("helpmsg.txt", "r").read()

@bot.event
async def on_ready():
    """
    Function called when Vivia starts up.
    """
    await log(f'Logged in as {bot.user}')
    
    # Change status
    await bot.change_presence(activity=discord.CustomActivity(name='v!help | ' + config['General']['StatusMessage']))

    # say whatever here
    await bot.get_channel(1247597054059085954).send("Heya all! I'd like to introduce myself.\nMy name is **Vivia!** It's a pleasure to meet you all.\n\nIf you need any help using my functions, just call me with `v!help` and I'll give more information!")

@bot.event
async def on_member_join(member):
    """
    Function called when a member joins the server.
    """
    welcome_channel = bot.get_channel(1246532114266980433) # Welcome channel
    await welcome_channel.send("Heya, " + member.mention + "! Welcome to the server!")

@bot.event
async def on_message(message):
    """
    Function called when a message is sent.
    """

    # Process commands
    await bot.process_commands(message)

    if message.author == bot.user:
        return
#    if "regina" in message.content:
#        await message.channel.send("\"BRO, STOP CALLING US YOU DONT EVEN WORK HERE?\"\n\nbut really RC is great")

@tree.command(
    name="quote",
    description="Say a random (slightly chaotic) quote."
)
async def quote(interaction):
    with open('quotes.json') as f:
        quotes = json.load(f)
        quote = random.choice(quotes['quotes'])
        await interaction.response.send_message(quote)

async def log(message, severity=logging.INFO):
    """
    Outputs a message to the log.

    Args:
        message (str): The message to output.
        severity (int): The severity of the message (defaults to Info).

    Notes:
        This function will output to the console, log file, and to a Discord channel.
    """
    print(message)
    await bot.get_channel(1246546976124965015).send(message)
    logging.log(severity, message)

@tree.command(
    name="help",
    description="Sends a help message, and virtual hugs!"
)
async def help(interaction):
    await interaction.user.send(helpMsg)
    await interaction.response.send_message(f"Do you need me, {interaction.user.display_name}? I just sent you a message with some helpful information.")

@bot.command()
async def sync(ctx):
    if ctx.author.id == 1141181390445101176:
        await bot.tree.sync()
        await log("Command tree synced")
    else:
        await ctx.send('You do not have permission to use this command.')

async def has_bot_permissions(user):
    """
    Checks if the specified user has bot permissions.

    Args:
        user (discord.User): The user to check.

    Returns:
        bool: True if the user has bot permissions, False otherwise.
    """
    with open('permissions.json') as f:
        users = json.load(f)
    return user.id in users['permissions']

bot.run(dotenv.get_key("token.env", "token"), log_handler=handler)
