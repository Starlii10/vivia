#!/usr/bin/env python

"""
    ViviaTools contains additional functions for Vivia and extensions.

    Vivia is licensed under the MIT License. For more information, see the LICENSE file.
    TL:DR: you can use Vivia's code as long as you keep the original license intact.
    Vivia is made open source in the hopes that you'll find her code useful.

    If you'd like to contribute, please check out the GitHub repository at https://github.com/starlii10/vivia.

    Have a great time using Vivia!
"""

from asyncio import subprocess
import asyncio
import configparser
import datetime
from functools import wraps
import json
import logging
import os
import random
import shutil
import sys
import traceback
from typing import Callable, Union
import colorlog
import zipfile

import discord
from discord.ext import commands
from discord.ext.commands import errors

if __name__ == "__main__":
    print("This is a helper script for Vivia that should not be run directly.", file=sys.stderr)
    print("To run Vivia, please use \"python bot.py\" in the root directory.", file=sys.stderr)
    print("Exiting.", file=sys.stderr)
    sys.exit(1)

# Variables
loaded_extensions = set(str())
failed_extensions = set(str())
running = False

# Config loading
config = configparser.ConfigParser()
if os.path.exists("config.ini"):
    # Update configuration if example config has something the current config doesn't
    with open('config.ini.example', 'r') as example_config, open('config.ini', 'r') as current_config:
        example = configparser.ConfigParser()
        example.read_file(example_config)
        current = configparser.ConfigParser()
        current.read_file(current_config)
        for section in example.sections():
            if not current.has_section(section):
                current.add_section(section)
                print(f"Config update: new section {section} (automatically applied)")
            for option in example.options(section):
                if not current.has_option(section, option):
                    print(f"Config update: new option {section} - {option} (automatically applied)")
                    current.set(section, option, example.get(section, option))
        with open('config.ini', 'w') as configfile:
            current.write(configfile)
    config.read("config.ini")
else:
    try:
        print("I didn't find a configuration file. I'm creating one for ya!)")
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
        'DEBUG'   : 'cyan',
        'INFO'    : 'cyan',
        'WARNING' : 'yellow',
        'ERROR'   : 'red',
        'CRITICAL': 'red',
    }
))

logger = logging.getLogger()
logger.addHandler(handler)

# File logging
handler = logging.FileHandler(f'data/logs/{datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.log')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s\t %(message)s'))
logger.addHandler(handler)

if config["Advanced"]["Debug"] == "True":
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Functions
def log(message: str, severity: int=logging.INFO):
    """
    Logs a message to the console.
    Essentially just a wrapper for logging.log
    """

    logging.log(severity, message)

def set_refs(bot_ref: commands.Bot):
    """
    An internal function to set variables so that extensions can access them. 
    """
    global bot
    bot = bot_ref

async def unload_extension(extension: str):
    """
    Unloads `extension` if it's loaded.

    ## Args:
        - extension (str): The name of the extension to unload.
    """
    try:
        await bot.unload_extension(extension)
        log(f"Unloaded extension {extension}")
    except errors.ExtensionNotLoaded:
        log(f"Extension {extension} was already unloaded.")
    except Exception as e:
        log(f"Failed to unload extension {extension}", logging.ERROR)
        log(f"{str(type(e))}: {e}", logging.ERROR)
        log("This may cause issues during reloading.", logging.ERROR)

async def load_extension(file: str, directory: str="commands"):
    """
    Loads `file` as an extension.

    ## Args:
        - file (str): The name of the file to load.
        - directory (str, optional): The directory to load the extension from. Defaults to "commands".
    """
    try:
        await bot.load_extension(f"{directory}.{file[:-3]}")
        loaded_extensions.append(f"{directory}.{file[:-3]}")
    except errors.ExtensionAlreadyLoaded:
        log(f"Extension {directory}.{file[:-3]} was already loaded.", logging.WARN)
    except Exception as e:
        log(f"Failed to load extension {file[:-3]} - functionality may be limited.", logging.ERROR)
        log("".join(traceback.format_exception(e)), logging.ERROR)
        failed_extensions.append(f"{directory}.{file[:-3]}")
    else:
        log(f"Loaded extension {directory}.{file[:-3]}")

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

    # verify that the file exists
    if not os.path.exists(file):
        log(f"VSE file {file} does not exist - skipping extraction", logging.ERROR)
        return
    
    # find the name of the VSE file
    filename = os.path.splitext(os.path.basename(file))[0]

    # Create the data/temp/extracted folder if it doesn't exist
    os.makedirs(os.path.join("data", "temp", "extracted"), exist_ok=True)

    # Create the data/temp/extracted/{vse file name} folder
    extract_path = os.path.join("data", "temp", "extracted", filename)
    os.makedirs(extract_path, exist_ok=True)

    # Unzip the VSE
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    # main python file (__main__.py)
    for f in os.listdir(extract_path):
        if f == "__main__.py":
            os.makedirs(os.path.join("commands", filename), exist_ok=True)
            os.rename(os.path.join(extract_path, f), os.path.join("commands", filename, f))
            break
    
    # extra python files
    for f in os.listdir(extract_path):
        if f.endswith(".py"):
            os.makedirs(os.path.join("commands", filename), exist_ok=True)
            os.rename(os.path.join(extract_path, f), os.path.join("commands", filename, f))
    
    # help text
    for f in os.listdir(extract_path):
        if f.endswith(".txt") and "help" in f:
            os.makedirs(os.path.join("data", "help", filename), exist_ok=True)
            os.rename(os.path.join(extract_path, f), os.path.join("data", "help", filename, "help.txt"))

    # personality messages
    personality_path = os.path.join(extract_path, "personalityMessages")
    if os.path.exists(personality_path):
        for f in os.listdir(personality_path):
            if f.endswith(".json"):
                os.makedirs("data/personalityMessages", exist_ok=True)
                os.rename(os.path.join(personality_path, f), os.path.join("data", "personalityMessages", f))
    
    # requirements.txt
    for f in os.listdir(extract_path):
        if f.endswith(".txt") and "requirements" in f:
            os.rename(os.path.join(extract_path, f), "requirements.txt")
            log(f"VSE extension {filename} contains a requirements.txt file. Attempting to run pip to install it", logging.WARNING)
            try:
                asyncio.run(subprocess.create_subprocess_shell("pip install -r requirements.txt", shell=True))
            except Exception as e:
                log(f"Failed to install requirements for VSE extension {filename}", logging.ERROR)
                log(f"{str(type(e))}: {e}", logging.ERROR)
                log(f"{filename} may not load correctly. Please install the requirements manually", logging.ERROR)
            break
    
    # statuses
    for f in os.listdir(extract_path):
        if f.endswith(".json") and "status" in f:
            os.makedirs(os.path.join("data", "status", filename), exist_ok=True)
            os.rename(os.path.join(extract_path, f), os.path.join("data", "status", filename, f))

    # Find and copy any other files (if any)
    for f in os.listdir(extract_path):
        if not f.endswith(".py") and not f.endswith(".txt") and not f.endswith(".json"):
            os.makedirs(os.path.join("data", filename), exist_ok=True)
            os.rename(os.path.join(extract_path, f), os.path.join("data", filename, f))

    # Remove the temporary folder
    shutil.rmtree(extract_path)
    
    # Remove the VSE if configured
    if config["Extensions"]["VSEClear"] == "True":
        log(f"Removing extracted VSE file: {file}", logging.DEBUG)
        os.remove(file)
    
def has_bot_permissions(user: discord.Member, server: discord.Guild):
    """
    Checks if the specified user has bot administrator permissions.

    ## Args:
        - user (discord.User): The user to check.
        - server (discord.Guild): The server to check in.

    ## Returns:
        - bool: True if the user has bot administrator permissions, False otherwise.

    ## Notes:
        - This always returns true for the server owner.
        - This also returns true if the user has a role with general administrator permissions.
    """
    adminRole = discord.utils.find(lambda a: a.name == "Vivia Admin", server.roles)
    if adminRole == None:
        return user.id == server.owner or user.guild_permissions.administrator
    else:
        return user.id == server.owner or user.guild_permissions.administrator or user in adminRole.members

def serverConfig(serverID: int):
    """
    Gets the configuration of a server.

    ## Args:
        - serverID (int): The ID of the server to get the config file of.

    ## Returns:
        - dict: The configuration of the server as a dictionary (JSON object).
    """
    with open(os.path.join("data", "servers", str(serverID), "config.json"), "r") as f:
        return json.load(f)
    
# TODO: Separate this into quotes extension, doesn't make sense to be in ViviaTools
def add_custom_quote(quote: str, serverID: int):
    """
    Adds a custom quote to a server's quotes.json file.

    ## Args:
        - quote (str): The quote to add.
        - serverID (int): The ID of the server to add the quote to.
    """
    with perServerFile(serverID, "quotes.json", template="{'quotes': []}") as f:
        quotes = json.load(f)
    quotes["quotes"].append(quote)
    with perServerFile(serverID, "quotes.json") as f:
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
        - Types in folders within the personalityMessages folder are valid (such as "extension1.messages").
    """
    try:
        with open(os.path.join("data", "personalityMessages", f"{type.replace('.', os.path.sep)}.json")) as f:
            messages = json.load(f)
            if config["General"]["UsePersonalityMessages"] == "True":
                random_msg = messages["messages"][random.randint(0, len(messages["messages"]) - 1)]
                if config["Advanced"]["Debug"] == "True":
                    log(f"Got a random {type} message: {random_msg}", logging.DEBUG)
                    return random_msg + f"\n-# (Message type: {type})"
                else:
                    return random_msg
            else:
                return messages["default"]
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
    os.makedirs(os.path.join("data", "servers", str(serverID)), exist_ok=True)
    if not os.path.exists(os.path.join("data", "servers", str(serverID), filename)):
        with open(os.path.join("data", "servers", str(serverID), filename), "w") as f:
            if template is None:
                if filename.endswith(".json"):
                    f.write("{}")
                else:
                    f.write("")
            else:
                f.write(template)
    return open(f"data/servers/{serverID}/{filename}", "r+")

async def setCustomPresence(message: str, bot: discord.Client, status: str = "online"):
    """
    Sets the bot's presence to the specified message.

    ## Args:
        - message (str): The message to set the presence to.
        - bot (discord.Client): A reference to the bot.
        - status (str, optional): The status to set the bot to. Can be "online", "idle", or "dnd". Defaults to "online".
    """
    await bot.change_presence(status=discord.Status[status], activity=discord.CustomActivity(name=message))

def helpMsg(extension: str):
    """
    Gets the help message for the specified extension.

    ## Args:
        - extension (str): The name of the extension to get the help message for.

    ## Returns:
        - str: The help message for the specified extension.

    ## Notes:
        - Help messages are stored in `data/help/<extension>/help.txt` - formatted for a Discord message (Markdown supported!).
    """
    try:
        with open(os.path.join('data', 'help', extension.replace(".", os.path.sep), 'help.txt'), 'r') as f:
            return f.read()
    except FileNotFoundError:
        log(f"Couldn't find help message for extension {extension}. Does it even exist?", logging.ERROR)
        return "There was supposed to be a help message here, but it doesn't seem to exist. Sorry about that!"
    
# ------------------------------------------------------------------------------
# Decorators

def ownerOnly(func: Callable) -> Callable:
    """
    Decorator that only allows the bot owner to execute a command.
    """
    @wraps(func)
    async def wrapper(ctx: Union[commands.Context, discord.Interaction], *args, **kwargs):
        if type(ctx) == discord.Interaction:
            # handle interactions differently since ctx.author isn't available
            if has_bot_permissions(ctx.user, ctx.guild):
                return await func(ctx, *args, **kwargs)
        else:
            if await bot.is_owner(ctx.author):
                return await func(ctx, *args, **kwargs)
        await ctx.send(personalityMessage("errors.missingpermissions"))
        return False
    return wrapper

def adminOnly(func: Callable) -> Callable:
    """
    Decorator that only allows Vivia Admins to execute a command.
    """
    @wraps(func)
    async def wrapper(ctx: Union[commands.Context, discord.Interaction], *args, **kwargs):
        if type(ctx) == discord.Interaction:
            # handle interactions differently since ctx.author isn't available
            if has_bot_permissions(ctx.user, ctx.guild):
                return await func(ctx, *args, **kwargs)
        else:
            if has_bot_permissions(ctx.author, ctx.guild):
                return await func(ctx, *args, **kwargs)
        await ctx.send(personalityMessage("errors.missingpermissions"))
        return False
    return wrapper

def blockInDMs(func: Callable) -> Callable:
    """
    Decorator that blocks commands from being executed in DMs.

    The difference between this decorator and the one provided by DPY is that this one outputs the `errors.nodm` message instead of outright blocking the command.
    """
    @wraps(func)
    async def wrapper(ctx: commands.Context, *args, **kwargs):
        if not ctx.guild:
            await ctx.send(personalityMessage("errors.nodm"))
            return False
        return await func(ctx, *args, **kwargs)
    return wrapper