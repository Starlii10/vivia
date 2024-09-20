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
import sys
import colorlog

import discord

if __name__ == "__main__":
    print("This is a helper script for Vivia that should not be run directly.", file=sys.stderr)
    print("To run Vivia, please use \"python bot.py\" in the root directory.", file=sys.stderr)
    print("Exiting.", file=sys.stderr)
    sys.exit(1)

# Variables
loaded_extensions = set(str())
failed_extensions = set(str())

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
logger.setLevel(logging.INFO)

# File logging
handler = logging.FileHandler(f'data/logs/{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.log')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s\t %(message)s'))
logger.addHandler(handler)

# Help messages
helpMsg = open("data/help/general.txt", "r").read()
channelmakerHelpMsg = open("data/help/channelmaker.txt", "r").read()
setupHelpMsg = open("data/help/setup.txt", "r").read()

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Functions
def generate_name(type, gender):
    """
    Generator for names.

    ## Args:
        type (str): The type of name to generate.
        gender (str): The gender of the name to generate.

    ## Returns:
        str: The generated name.
    """
    with open('data/names.json') as f:
        names = json.load(f)
        all_names = names['first']['male'] + names['first']['female']
        match type:
            case "first":
                match gender:
                    case "male":
                        random_msg = names['first']['male'][random.randint(0, len(names['first']['male']) - 1)]
                    case "female":
                        random_msg = names['first']['female'][random.randint(0, len(names['first']['female']) - 1)]
                    case _:
                        random_msg = all_names[random.randint(0, len(all_names) - 1)]
            case "middle":
                random_msg = names['middle'][random.randint(0, len(names['middle']) - 1)]
            case "last":
                random_msg = names['last'][random.randint(0, len(names['last']) - 1)]
            case "full":
                match gender:
                    case "male":
                        random_msg = names['first']['male'][random.randint(0, len(names['first']['male']) - 1)] + " "+ names['middle'][random.randint(0, len(names['middle']) - 1)] + " " + names['last'][random.randint(0, len(names['last']) - 1)]
                    case "female":
                        random_msg = names['first']['female'][random.randint(0, len(names['first']['female']) - 1)] + " "+ names['middle'][random.randint(0, len(names['middle']) - 1)] + " " + names['last'][random.randint(0, len(names['last']) - 1)]
                    case _:
                        random_msg = all_names[random.randint(0, len(all_names) - 1)] + " "+ names['middle'][random.randint(0, len(names['middle']) - 1)] + " " + names['last'][random.randint(0, len(names['last']) - 1)]
            
        if config["Advanced"]["Debug"] == "True":
            log(f"Generated name: {random_msg}", logging.DEBUG)
        return random_msg

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
        - dict: The configuration of the server as loaded JSON.
    """
    with open(f"data/servers/{serverID}/config.json", "r") as f:
        return json.load(f)
    
def log(message: str, severity: int=logging.INFO):
    """
    Logs a message to the console.
    """

    logging.log(severity, message)

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