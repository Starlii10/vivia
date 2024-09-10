#!/usr/bin/env python

"""
    This script is part of Vivia.

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
import traceback

import discord

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
        print(f"{type(e)}: {e}\n{traceback.format_exc()}")
        sys.exit(1)

# Set up logging
try:
    handler = logging.FileHandler(
        filename="data/logs/" + datetime.datetime.now().strftime("%Y-%m-%d") + ".log",
        encoding='utf-8',
        mode='w'
    )
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logging.basicConfig(level=logging.INFO)
except:
    print("Something's wrong with the logging file. I'm going to ignore it.")
    handler = logging.StreamHandler(sys.stdout)

# Help messages
helpMsg = open("data/help/general.txt", "r").read()
channelmakerHelpMsg = open("data/help/channelmaker.txt", "r").read()
setupHelpMsg = open("data/help/setup.txt", "r").read()

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
                        return names['first']['male'][random.randint(0, len(names['first']['male']) - 1)]
                    case "female":
                        return names['first']['female'][random.randint(0, len(names['first']['female']) - 1)]
                    case _:
                        return all_names[random.randint(0, len(all_names) - 1)]
            case "middle":
                return names['middle'][random.randint(0, len(names['middle']) - 1)]
            case "last":
                return names['last'][random.randint(0, len(names['last']) - 1)]
            case "full":
                match gender:
                    case "male":
                        return names['first']['male'][random.randint(0, len(names['first']['male']) - 1)] + " "+ names['middle'][random.randint(0, len(names['middle']) - 1)] + " " + names['last'][random.randint(0, len(names['last']) - 1)]
                    case "female":
                        return names['first']['female'][random.randint(0, len(names['first']['female']) - 1)] + " "+ names['middle'][random.randint(0, len(names['middle']) - 1)] + " " + names['last'][random.randint(0, len(names['last']) - 1)]
                    case _:
                        return all_names[random.randint(0, len(all_names) - 1)] + " "+ names['middle'][random.randint(0, len(names['middle']) - 1)] + " " + names['last'][random.randint(0, len(names['last']) - 1)]

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
    print(message + f" ({logging.getLevelName(severity)})")

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

def personalityMessage(type: str):
    """
    Gets a random message of the specified type.

    ## Args:
        - type (str): The type of message to get.

    ## Returns:
        - str: The random message of the specified type. An empty string if the type is not found.
    """
    try:
        with open(f'data/personalityMessages/{str}.json') as f:
            messages = json.load(f)
            return messages[type][random.randint(0, len(messages[type]) - 1)]
    except FileNotFoundError:
        log(f"Couldn't find personality message database for type {type}. Does it even exist?", logging.ERROR)
        return ""