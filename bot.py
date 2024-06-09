#!/usr/bin/env python

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

# Config loading
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
    print("I found my configuration file!")

# Set up logging
handler = logging.FileHandler(
    filename=config['Logging']['Filename'],
    encoding='utf-8',
    mode='w'
)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logging.basicConfig(level=logging.INFO)

system("title Vivia - " + config['General']['StatusMessage'])
print("Preparing to start up!")

# Get ready to run the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=config['General']['Prefix'], intents=intents)
bot.remove_command("help")
tree = bot.tree
helpMsg = open("helpmsg.txt", "r").read()

@bot.event
async def on_ready():
    """
    Function called when Vivia starts up.
    """

    await log(f'I\'m awake! Discord says my username is {bot.user}.')
    
    # Change status
    await bot.change_presence(activity=discord.CustomActivity(name=f'{config["General"]["Prefix"]}help | ' + config['General']['StatusMessage']))

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

    # Make sure Vivia doesn't respond to herself
    if message.author == bot.user:
        return
#    if "regina" in message.content:
#        await message.channel.send("\"BRO, STOP CALLING US YOU DONT EVEN WORK HERE?\"\n\nbut really RC is great")

@tree.command(
    name="quote",
    description="Say a random (slightly chaotic) quote."
)
async def quote(interaction):
    """
    Sends a random (slightly chaotic) quote.
    """
    with open('quotes.json') as f:
        quotes = json.load(f)
        quote = random.choice(quotes['quotes'])
        await interaction.response.send_message(quote)

async def log(message, severity=logging.INFO):
    """
    Outputs a message to the log.

    ## Args:
        - message (str): The message to output.
        - severity (int): The severity of the message (defaults to Info).

    ## Notes:
        - This function will output to the console, log file, and to a Discord channel.
    """
    print(message)
    await bot.get_channel(int(config['Channels']['LoggingChannel'])).send(message)
    logging.log(severity, message)

@tree.command(
    name="help",
    description="Sends a help message, and virtual hugs!"
)
async def help(interaction):
    await interaction.user.send(helpMsg)
    await interaction.response.send_message(f"Do you need me, {interaction.user.display_name}? I just sent you a message with some helpful information.", ephemeral=True)

@bot.command()
async def sync(ctx):
    """
    Syncs the command tree.

    ## Notes:
        Only users with bot permissions can use this command.
    """
    if ctx.author.id == int(config['General']['Owner']):
        await bot.tree.sync()
        await ctx.send('The command tree was synced, whatever that means.')
        await log("The command tree was synced, whatever that means.")
    else:
        await ctx.send('That\'s for the bot owner, not random users...')

async def has_bot_permissions(user):
    """
    Checks if the specified user has bot permissions.

    ## Args:
        - user (discord.User): The user to check.

    ## Returns:
        - bool: True if the user has bot permissions, False otherwise.
    ## Notes:
        - This always returns true for the bot owner specified in config.ini.
    """
    with open('permissions.json') as f:
        users = json.load(f)
    return user.id in users['permissions'] or user.id == int(config['General']['Owner'])

@tree.command(
    name="say",
    description="Makes Vivia say something."
)
async def say(interaction, message: str):
    """
    Makes Vivia say something.

    ## Args:
        - message (str): The message to say.
    ## Notes:
        - Only the bot owner can use this command.
    """
    if interaction.user.id == int(config['General']['Owner']):
        await interaction.response.send_message(message)
        await log(f"{interaction.user} said {message} as Vivia")
    else:
        await interaction.response.send_message("That's for the bot owner, not random users...", ephemeral=True)

@tree.command(
    name="addquote",
    description="Adds a quote to the list."
    
)
async def addquote(interaction, quote: str, author: str, date: str):
    """
    Adds a quote to the list.

    ## Args:
        - quote (str): The quote to add.
        - author (str): The author of the quote.
        - date (str): The date of the quote.
    ## Notes:
        - Only users with bot permissions can use this command.
        - The quote will be formatted as `"quote" - author, date`.
    """
    if has_bot_permissions(interaction.user):
        with open('quotes.json') as f:
            quotes = json.load(f)
            quotes['quotes'].append(f'"{quote}" - {author}, {date}')
        with open('quotes.json', 'w') as f:
            json.dump(quotes, f)
        await interaction.response.send_message(f'"{quote}" - {author}, {date} was added to the list.')
        await log(f"{interaction.user} added {quote} - {author}, {date} to the list")
    else:
        await interaction.response.send_message("That's for authorized users, not you...", ephemeral=True)

# Run
bot.run(dotenv.get_key("token.env", "token"), log_handler=handler)
