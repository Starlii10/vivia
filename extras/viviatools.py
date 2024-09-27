#!/usr/bin/env python

"""
    This is ViviaTools, a helper script for Vivia that contains commonly used functions.

    Vivia is licensed under the MIT License. For more information, see the LICENSE file.
    TL:DR: you can use Vivia's code as long as you keep the original license intact.
    Vivia is made open source in the hopes that you'll find her code useful.

    If you'd like to contribute, please check out the GitHub repository at https://github.com/starlii10/vivia.

    Have a great time using Vivia!
"""

import configparser
import datetime
import json
import logging
import os
import random
import shutil
import sys
import colorlog
import discord
import zipfile

from discord.ext import commands

if __name__ == "__main__":
    print("This is a helper script for Vivia that should not be run directly.", file=sys.stderr)
    print("To run Vivia, please use \"python bot.py\" in the root directory.", file=sys.stderr)
    print("Exiting.", file=sys.stderr)
    sys.exit(1)

# Variables
loaded_extensions = set(str())
failed_extensions = set(str())
running = False
bot_ref = commands.Bot()

# Config loading
config = configparser.ConfigParser()
if os.path.exists("config.ini"):
    config.read("config.ini")
else:
    try:
        print("I didn't find a configuration file. I'm creating one for ya!")
        config.read("config.ini.example")
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    except Exception as e:
        print("I couldn't create a config file. Is something wrong with config.ini.example?")
        print(f"{str(type(e))}: {e}")
        sys.exit(1)
    
# Create log folder if it doesn't exist
os.makedirs("data/logs", exist_ok=True)

# Set up logging

# Terminal logging (color)
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '\033[0;37m%(asctime)s %(log_color)s%(levelname)s\t \033[0;35m%(name)s %(reset)s%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    reset=True,
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'cyan',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red',
    }
))

logger = logging.getLogger()
logger.addHandler(handler)
if config["Advanced"]["Debug"] == "True":
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

# File logging
handler = logging.FileHandler(f'data/logs/{datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.log')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s\t %(message)s'))
logger.addHandler(handler)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Functions
def log(message: str, severity: int=logging.INFO):
    """
    Logs a message to the console.
    """

    logging.log(severity, message)

def extractVSE(file: str):
    """
    Extracts a self-contained extension (VSE) file.

    ## Args:
        - file (str): The path to the VSE file to extract.

    ## Returns:
        - None.

    ## Notes:
        - VSEs are zipped files that contain multiple files, specifically a Python script and data files.
    """

    # find the name of the VSE file
    filename = os.path.basename(file).removesuffix(".vse")

    # Create the data/temp/extracted folder if it doesn't exist
    os.makedirs("data/temp/extracted", exist_ok=True)

    # Create the data/temp/extracted/{vse file name} folder
    os.makedirs(f"data/temp/extracted/{filename}", exist_ok=True)

    # Unzip the VSE
    zipfile.ZipFile(file).extractall(f"data/temp/extracted/{filename}")

    # python file
    for f in os.listdir(f"data/temp/extracted/{filename}"):
        if f.endswith(".py"):
            os.rename(f"data/temp/extracted/{filename}/{f}", f"commands/{filename}.py")
            break
    
    # help text
    for f in os.listdir(f"data/temp/extracted/{filename}"):
        if f.endswith(".txt") and "help" in f:
            os.rename(f"data/temp/extracted/{filename}/{f}", f"data/help/{f}")

    # personality messages
    for f in os.listdir(f"data/temp/extracted/{filename}/personalityMessages"):
        if f.endswith(".json"):
            os.rename(f"data/temp/extracted/{filename}/personalityMessages/{f}", f"data/personalityMessages/{f}")
    
    # requirements.txt
    for f in os.listdir(f"data/temp/extracted/{filename}"):
        if f.endswith(".txt") and "requirements" in f:
            os.rename(f"data/temp/extracted/{filename}/{f}", f"requirements.txt")
            break

    # TODO: Find and copy any other files (if any)

    # Remove the temporary folder
    shutil.rmtree(f"data/temp/extracted/{filename}")\
    
    # Remove the VSE if configured
    if config["Extensions"]["VSEClear"] == "True":
        log(f"Removing extracted VSE file: {file}", logging.DEBUG)
        os.remove(file)
    
def has_bot_permissions(user: discord.Member, server: discord.Guild):
    """
    Checks if the specified user has bot permissions.

    ## Args:
        - user (discord.User): The user to check.
        - server (discord.Guild): The server to check in.

    ## Returns:
        - bool: True if the user has bot permissions, False otherwise.

    ## Notes:
        - This always returns true for the server owner.
        - This also returns true if the user has a role with administrator permissions.
    """
    adminRole = discord.utils.find(lambda a: a.name == "Vivia Admin", server.roles)
    if adminRole == None:
        return user.id == server.owner or user.guild_permissions.administrator
    return user.id == server.owner or user.guild_permissions.administrator or user in adminRole.members

def serverConfig(serverID: int):
    """
    Gets the configuration of a server.

    ## Args:
        - serverID (int): The ID of the server to get the config file of.

    ## Returns:
        - dict: The configuration of the server as a dictionary (JSON object).
    """
    with open(f"data/servers/{serverID}/config.json", "r") as f:
        return json.load(f)
    

def add_custom_quote(quote: str, serverID: int):
    """
    Adds a custom quote to a server's quotes.json file.

    ## Args:
        - quote (str): The quote to add.
        - serverID (int): The ID of the server to add the quote to.
    """
    with open(f"data/servers/{serverID}/quotes.json", "r") as f:
        quotes = json.load(f)
    quotes["quotes"].append(quote)
    with open(f"data/servers/{serverID}/quotes.json", "w") as f:
        json.dump(quotes, f)
    if config["Advanced"]["Debug"] == "True":
        log(f"Added custom quote for {serverID}: {quote}", logging.DEBUG)

def personalityMessage(type: str):
    """
    Gets a random message of the specified type.

    ## Args:
        - type (str): The type of message to get.

    ## Returns:
        - str: The random message of the specified type. An empty string if the type is not found.
    
    ## Notes:
        - In debug mode, this will log the message to the console and also return the message type at the end of the string.
        - Types in folders within the personalityMessages folder are valid (such as "extension1/messages").
    """
    try:
        with open(f'data/personalityMessages/{type}.json') as f:
            messages = json.load(f)
            random_msg = messages["messages"][random.randint(0, len(messages["messages"]) - 1)]
            if config["Advanced"]["Debug"] == "True":
                log(f"Got a random {type} message: {random_msg}", logging.DEBUG)
                return random_msg + f" (Message type: {type})"
            else:
                return random_msg
    except FileNotFoundError:
        log(f"Couldn't find personality message database for type {type}. Does it even exist?", logging.ERROR)
        return ""
    
def perServerFile(serverID: int, filename: str, template: str | None = None):
    """
    Gets a file from the per-server folder.

    ## Args:
        - serverID (int): The ID of the server to get the file from.
        - filename (str): The name of the file to get.
        - template (str | None, optional): The template to use if the file doesn't exist. Defaults to a blank string, or "{}" for JSON files.
        
    ## Returns:
        - TextIOWrapper[_WrappedBuffer]: The opened file.

    ## Notes:
        - This will automatically create the file using `template` if it doesn't exist.
        - This will create the per-server folder if it doesn't exist.
        - This only opens the file. You'll need to manage reading and writing to it yourself.
    """
    os.makedirs(f"data/servers/{serverID}", exist_ok=True)
    if not os.path.exists(f"data/servers/{serverID}/{filename}"):
        with open(f"data/servers/{serverID}/{filename}", "w") as f:
            if template is None:
                if filename.endswith(".json"):
                    f.write("{}")
                else:
                    f.write("")
            else:
                f.write(template)
    return open(f"data/servers/{serverID}/{filename}", "r+")

async def setCustomPresence(message: str, bot: commands.Bot):
    """
    Sets the bot's presence to the specified message.

    ## Args:
        - message (str): The message to set the presence to.
        - bot (commands.Bot): A reference to the bot.

    ## Notes:
        - This will always set the bot's status to online.
    """
    await bot.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name=message))

def helpMsg(extension: str):
    """
    Gets the help message for the specified extension.

    ## Args:
        - extension (str): The name of the extension to get the help message for.

    ## Returns:
        - str: The help message for the specified extension.
    """
    with open(f"data/extensions/{extension}/help.txt", "r") as f:
        return f.read()