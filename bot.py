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
from discord import app_commands
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
try:
    handler = logging.FileHandler(
        filename=config['Logging']['Filename'],
        encoding='utf-8',
        mode='w'
    )
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logging.basicConfig(level=logging.INFO)
except:
    print("Something's wrong with the logging file. I'm going to ignore it.")
    handler = logging.StreamHandler(sys.stdout)

system("title Vivia - " + config['General']['StatusMessage'])
print("Preparing to start up!")

# Get ready to run the bot
intents = discord.Intents.default()
intents.message_content = True # will need to verify at 100 servers to get this working, but for now it's fine
bot = commands.Bot(command_prefix=config['General']['Prefix'], intents=intents)
bot.remove_command("help")
tree = bot.tree
helpMsg = open("helpmsg.txt", "r").read()
channelmakerHelpMsg = open("channelmakerhelpmsg.txt", "r").read()

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
        with open('custom-quotes.json') as g:
            default_quotes = json.load(f)
            custom_quotes = json.load(g)
            quotes = default_quotes['quotes'] + custom_quotes['quotes']
            quote = random.choice(quotes)
            await interaction.response.send_message(quote)

@tree.command(
    name="listquotes",
    description="List all quotes."
)
async def listquotes(interaction):
    """
    Sends a list of all quotes.
    """
    with open('quotes.json') as f:
        with open('custom-quotes.json') as g:
            default_quotes = json.load(f)
            custom_quotes = json.load(g)
            quotes = default_quotes['quotes'] + custom_quotes['quotes']
            await interaction.response.send_message(quotes)

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

def has_bot_permissions(user):
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
        await log(f"{interaction.user} said \"{message}\" as Vivia")
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
        - This adds the quote to the custom quote list.
    """
    if has_bot_permissions(interaction.user):
        with open('custom-quotes.json') as f:
            quotes = json.load(f)
            quotes['quotes'].append(f'"{quote}" - {author}, {date}')
        with open('custom-quotes.json', 'w') as f:
            json.dump(quotes, f)
        await interaction.response.send_message(f'"{quote}" - {author}, {date} was added to the list.')
        await log(f"{interaction.user} added \"{quote} - {author}, {date}\" to the list")
    else:
        await interaction.response.send_message("That's for authorized users, not you...", ephemeral=True)

@tree.command(
    name="removequote",
    description="Removes a quote from the list."
)
async def removequote(interaction, quote: str):
    """
    Removes a quote from the list.

    ## Args:
        - quote (str): The quote to remove.
    ## Notes:
        - Only users with bot permissions can use this command.
        - This removes the quote from the custom quote list.
    """
    if has_bot_permissions(interaction.user):
        with open('custom-quotes.json') as f:
            quotes = json.load(f)
            quotes['quotes'].remove(quote)
        with open('custom-quotes.json', 'w') as f:
            json.dump(quotes, f)
        await interaction.response.send_message(f'"{quote}" was removed from the list.')
        await log(f"{interaction.user} removed \"{quote}\" from the list")
    else:
        await interaction.response.send_message("That's for authorized users, not you...", ephemeral=True)

channelMakerCmds = app_commands.Group(name="channelmaker", description="Makes channels from JSON.")

@tree.command(
    name="channelmaker",
    description="Makes a bunch of channels from JSON."
)
@app_commands.choices(type=[
    app_commands.Choice(name="text",value="Makes text channels."),
    app_commands.Choice(name="voice",value="Makes voice channels."),
    app_commands.Choice(name="forum",value="Makes forum channels."),
])
async def channelmaker(interaction, channel_config: str, type: str="text"):
    """
    Makes a bunch of channels from JSON.

    ## Notes:
        - Only users with bot permissions can use this command.
    """
    if has_bot_permissions(interaction.user):
        try:
            channels = json.loads(channel_config) # Channels is a list of categories, each category is a list of channels
            for category in channels['categories']:
                if not category in interaction.guild.categories.name:
                    # Create the category
                    target = await interaction.guild.create_category(category, reason=f"Created by /channelmaker - run by {interaction.user}")
                else:
                    target = interaction.guild.categories.get(category)
                for channel in channels['categories'][category]:
                    # Create the channel
                    match type:
                        case "text":
                            await interaction.guild.create_text_channel(channel, category=target, reason=f"Created by /channelmaker - run by {interaction.user}")
                        case "voice":
                            await interaction.guild.create_voice_channel(channel, category=target, reason=f"Created by /channelmaker - run by {interaction.user}")
                        case "forum":
                            await interaction.guild.create_forum(channel, category=target, reason=f"Created by /channelmaker - run by {interaction.user}")
                    await log(f"{interaction.user} created {channel} in {category}")
            await interaction.response.send_message("All done!")
        except Exception as e:
            await interaction.response.send_message("Couldn't make the channels: " + str(e), ephemeral=True)
            await log(e)
    else:
        await interaction.response.send_message("That's for authorized users, not you...", ephemeral=True)

@channelMakerCmds.command(
    name="help",
    description="Sends a help message for the channelmaker tool."
)
async def channelmaker(interaction):
    """
    Sends a help message for the channelmaker tool.
    """
    await interaction.user.send(channelmakerHelpMsg)
    await interaction.response.send_message(f"Do you need me, {interaction.user.display_name}? I just sent you a message with some helpful information.", ephemeral=True)
# Run
bot.run(dotenv.get_key("token.env", "token"), log_handler=handler)
