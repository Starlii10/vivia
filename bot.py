# this is a whole hecking lot of imports, and yes, every single one is used

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
        print("config.ini not found, creating new from default. If this is the first run please ignore this message")
        config.read("config.ini.example")
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    except:
        print("config.ini.example not found or couldn't be read")
        sys.exit(1)
else:
    print("config.ini found, loading it")


handler = logging.FileHandler(
    filename=config['Logging']['Filename'],
    encoding='utf-8',
    mode='w'
)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logging.basicConfig(level=logging.INFO)

system("title Vivia - " + config['General']['StatusMessage'])

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='ntb!', intents=intents)
bot.remove_command("help")
tree = bot.tree

helpMsg = open("helpmsg.txt", "r").read()

@bot.event
async def on_ready():
    """
    Function called when the bot starts up
    """
    await log(f'Logged in as {bot.user}')
    
    # Change status
    await bot.change_presence(activity=discord.CustomActivity(name='ntb!help | ' + config['General']['StatusMessage']))

    # say whatever here
    # await bot.get_channel(1243032295481282657).send("yes")

@bot.event
async def on_member_join(member):
    """
    Function called when a member joins the server
    """
    welcome_channel = bot.get_channel(1246532114266980433) # Welcome channel
    await welcome_channel.send("Heya, " + member.mention + "! Welcome to the server!")

@bot.event
async def on_message(message):
    """
    Function called when a message is sent
    """

    # Process commands
    await bot.process_commands(message)

    if message.author == bot.user:
        return
    if "regina" in message.content:
        await message.channel.send("\"BRO, STOP CALLING US YOU DONT EVEN WORK HERE?\"\n\nbut really RC is great")

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
async def help(ctx):
    await ctx.author.send(helpMsg)
    await ctx.send(f"Check your DMs {ctx.author.mention}")

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
