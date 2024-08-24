#!/usr/bin/env python

"""
    This is the primary script for Vivia.

    Vivia is licensed under the MIT License. For more information, see the LICENSE file.
    TL:DR: you can use Vivia's code as long as you keep the original license intact.
    Vivia is made open source in the hopes that you'll find her code useful.

    If you'd like to contribute, please check out the GitHub repository at https://github.com/starlii10/vivia.

    Have a great time using Vivia!
"""

# Vivia version
__VERSION__ = "Vivia 20240821"

import asyncio
import datetime
import shutil
import sys
import json
import traceback
import dotenv
import random
import os
from os import system
import configparser
import logging

# Discord
import discord
from discord import Embed, app_commands
from discord.ext import tasks, commands

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

# Vivia's extra scripts (these require the config to be loaded first)
import extras.viviatools as viviaTools
import extras.viviallama as Llama

# Load commonly used config values
logChannel = int(config['Channels']['LoggingChannel'])

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

# Terminal title. VSCode will scream at you that one of these is unreachable, ignore it
if sys.platform == 'win32':
    # Windows title
    system("title Running " + __VERSION__ + " - " + config['General']['StatusMessage'])
else:
    # Linux title (if this doesn't work on your distro please open an issue because I suck at Linux)
    system("echo -ne '\033]0;Vivia - " + config['General']['StatusMessage'] + "\007'")

print("Preparing to start up!")

# Get ready to run the bot
intents = discord.Intents.default()
intents.message_content = True # will need to verify at 100 servers
bot = commands.Bot(command_prefix=config['General']['Prefix'], intents=intents)
bot.remove_command("help") # because we hate the default help command
tree = bot.tree

# Help messages
helpMsg = open("data/help/general.txt", "r").read()
channelmakerHelpMsg = open("data/help/channelmaker.txt", "r").read()
setupHelpMsg = open("data/help/setup.txt", "r").read()

# Functions
# I should separate this into ViviaTools but who cares
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
    try:
        adminRole = discord.utils.find(lambda a: a.name == "Vivia Admin", server.roles)
    except AttributeError:
        # TODO: log this issue so it can be fixed by the server admins
        return False
    return user.id == server.owner or user.guild_permissions.administrator or user in adminRole.members

def serverConfig(serverID: int):
    with open(f"data/servers/{serverID}/config.json", "r") as f:
        return json.load(f)

async def log(message: str, sendToLogChannel: bool=True, severity: int=logging.INFO):
    """
    Outputs a message to the log.

    ## Args:
        - message (str): The message to output.
        - sendToLogChannel (bool): Whether to send the message to the log channel.
        - severity (int): The severity of the message (defaults to Info).

    ## Notes:
        - This function will output to the console, log file, and to a Discord channel.
        - Errors will ping the owner of the bot if sent to the log channel.
    """
    try:
        if sendToLogChannel:
            if severity == logging.ERROR:
                await bot.get_channel(logChannel).send("<@" + config["General"]["Owner"] + "> " + message)
            else:
                await bot.get_channel(logChannel).send(message)
    except:
        pass # we don't care if the channel doesn't exist
    logging.log(severity, message) # also prints to the console

# Events
@bot.event
async def on_ready():
    """
    Function called when Vivia starts up.
    """
    
    await log("Vivia is online!", sendToLogChannel=False)
    
    # Statuses
    with open("data/statuses.json", "r") as f:
        statuses = json.load(f)
    await bot.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name=random.choice(statuses["statuses"])))
    statusChanges.start()

@tasks.loop(hours=1)
async def statusChanges():
    """
    Changes the bot's status every hour.
    """
    with open("data/statuses.json", "r") as f:
        statuses = json.load(f)
    await bot.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name=random.choice(statuses["statuses"])))

@bot.event
async def on_member_join(member):
    """
    Function called when a member joins the server.
    """

@bot.event
async def on_guild_join(guild: discord.Guild):
    """
    Function called when the bot joins a server.
    """

    await log(f"Bot joined {guild.name} ({guild.id})")
    with open(f'data/servers/{guild.id}/quotes.json', 'w') as f:
        json.dump({'quotes': []}, f)
    with open(f'data/servers/{guild.id}/config.json', 'w') as f, open(f'data/config.json.example', 'r') as g:
        json.dump(g, f)
    await guild.create_role(name="Vivia Admin", reason="Vivia setup: Users with this role have privileges when running Vivia's commands in this server.")
    for member in guild.members:
        if member.guild_permissions.administrator:
            await member.add_roles(discord.utils.find(lambda r: r.name == "Vivia Admin", guild.roles), reason="Vivia setup: This user has administrative permissions and was automatically assigned to the Vivia Admin role.")

@bot.event
async def on_message(message: discord.Message):
    """
    Function called when a message is sent.
    """

    # Make sure Vivia doesn't respond to herself
    if message.author == bot.user:
        return

    # Process commands
    await bot.process_commands(message)

    # Invoke LLaMa if pinged (this also works for replies)
    if serverConfig(message.guild.id)['aiEnabled']:
        # we need to check both for direct mentions of Vivia and for mentions of the Vivia role to prevent confusion
        if (message.mentions and (message.mentions[0] == bot.user or message.role_mentions[0] == discord.utils.get(message.guild.roles, name="Vivia"))): # This is throwing IndexErrors for some reason. Gonna ignore it
            async with message.channel.typing():
                await llamaReply(message)

async def llamaReply(message: discord.Message):
    """
    Gets a reply using LLaMa.
    """
    task = asyncio.create_task(Llama.createResponse(message.content.removeprefix(f"<@{str(message.author.id)}> "), message.author.display_name, message.author.name, message.attachments))
    await message.reply(await task)

# Commands
# TODO: move commands to a separate file so they're easier to deal with
@tree.command(
    name="quote",
    description="Say a random (slightly chaotic) quote."
)
async def quote(interaction: discord.Interaction):
    """
    Sends a random (slightly chaotic) quote.
    """
    try:
        with open('data/quotes.json') as f:
            with open(f'data/servers/{interaction.guild.id}/quotes.json') as g:
                default_quotes = json.load(f)
                custom_quotes = json.load(g)
                quotes = default_quotes['quotes'] + custom_quotes['quotes']
                quote = random.choice(quotes)
                await interaction.response.send_message(quote)
    except Exception as e:
        await interaction.response.send_message("Something went wrong. Maybe try again?")
        if serverConfig(interaction.guild.id)['verboseErrors']:
            await interaction.followup.send(f"{type(e)}: {e}\n-# To disable these messages, run /config verboseErrors false")
        await log(f"Couldn't send a quote for server {interaction.guild.name} ({interaction.guild.id}): {type(e)}: {e}", severity=logging.ERROR)
    
@tree.command(
    name="listquotes",
    description="List all quotes."
)
async def listquotes(interaction: discord.Interaction):
    """
    Sends a list of all quotes.
    """
    try:
        with open('data/quotes.json') as f:
            with open(f'data/servers/{interaction.guild.id}/quotes.json') as g:
                default_quotes = json.load(f)
                custom_quotes = json.load(g)
                quotes = default_quotes['quotes'] + custom_quotes['quotes']
                await interaction.response.send_message(quotes)
    except Exception as e:
        await interaction.response.send_message("Something went wrong. Maybe try again?")
        if serverConfig(interaction.guild.id)['verboseErrors']:
            await interaction.followup.send(f"{type(e)}: {e}\n-# To disable these messages, run /config verboseErrors false")
        await log(f"Couldn't list quotes for server {interaction.guild.name} ({interaction.guild.id}): {type(e)}: {e}", severity=logging.ERROR)
@tree.command(
    name="help",
    description="Sends a help message, and virtual hugs!"
)
@app_commands.choices(message=[
    app_commands.Choice(name="general", value="general"),
    app_commands.Choice(name="channelmaker", value="channelmaker"),
    app_commands.Choice(name="setup", value="setup"),
])
async def help(interaction: discord.Interaction, message: str="general"):
    match message:
        case "general":
            await interaction.user.send(helpMsg)
        case "channelmaker":
            await interaction.user.send(channelmakerHelpMsg)
        case "setup":
            await interaction.user.send(setupHelpMsg)
        case _:
            await interaction.user.send(helpMsg)
    await interaction.response.send_message(f"Do you need me, {interaction.user.display_name}? I just sent you a message with some helpful information.", ephemeral=True)

@bot.command()
async def sync(ctx):
    """
    Syncs the command tree.

    ## Notes:
        - Only the bot owner can use this command. If you run Vivia locally, make sure to add your Discord user ID in config.ini.
        - This command does not appear in the command list. Use "v!sync" to run it.
    """
    if ctx.author.id == config["General"]["Owner"]:
        await bot.tree.sync()
        await ctx.send('The command tree was synced, whatever that means.')
        await log("The command tree was synced, whatever that means.")
    else:
        await ctx.send('That\'s for the bot owner, not random users...')

@bot.command()
async def fixconfig(ctx):
    """
    Regenerates configuration and custom quotes files for servers where they are missing.

    ## Notes:
        - Only the bot owner can use this command. If you run Vivia locally, make sure to add your Discord user ID in config.ini.
        - This command does not appear in the command list. Use "v!fixconfig" to run it.
    """
    if ctx.author.id == config["General"]["Owner"]:
        for guild in bot.guilds:
            # Regenerate server data path if it doesn't exist
            if not os.path.exists(f'data/servers/{guild.id}'):
                os.mkdir(f'data/servers/{guild.id}')
            await log(f'Data path for {guild.name} ({guild.id}) was regenerated.')

            # Regenerate configuration if guild config is missing
            try:
                with open(f'data/servers/{guild.id}/config.json', 'x') as f, open(f'data/config.json.example', 'r') as g:
                    json.dump(obj=json.load(g), fp=f)
                await log(f'Config file for {guild.name} ({guild.id}) was regenerated.')
            except FileExistsError:
                pass # Most likely there was nothing wrong with it

            # Regenerate quotes if guild quotes is missing
            try:
                with open(f'data/servers/{guild.id}/quotes.json', 'x') as f:
                    json.dump({'quotes': []}, f)
                await log(f'Custom quote file for {guild.name} ({guild.id}) was regenerated.')
            except FileExistsError:
                pass # Most likely there was nothing wrong with it

        await ctx.send('Fixed all missing config and quotes files. Check log channel for more info.')
    else:
        await ctx.send('That\'s for the bot owner, not random users...')


@tree.command(
    name="addquote",
    description="Adds a quote to the list."
)
async def addquote(interaction: discord.Interaction, quote: str, author: str, date: str):
    """
    Adds a quote to the list.

    ## Args:
        - quote (str): The quote to add.
        - author (str): The author of the quote.
        - date (str): The date of the quote.
    ## Notes:
        - Only users with bot permissions can use this command.
        - The quote will be formatted as `"quote" - author, date`.
        - This adds the quote to the custom quote list for the server the command was used in.
    """
    if has_bot_permissions(interaction.user, interaction.guild):
        try:
            with open(f'data/servers/{interaction.guild.id}/quotes.json') as f:
                quotes = json.load(f)
                # Add the quote
                quotes['quotes'].append(f'"{quote}" - {author}, {date}')
            # Write the updated list
            with open(f'data/servers/{interaction.guild.id}/quotes.json', 'w') as f:
                json.dump(quotes, f)
        except Exception as e:
            await interaction.response.send_message(f'Something went wrong. Maybe try again?', ephemeral=True)
            if config["General"]["VerboseErrors"]:
                await interaction.followup.send(f"{type(e)}: {e}\n-# To disable these messages, run /config verboseErrors false")
            await log(f'Failed to add "{quote} - {author}, {date}" to the custom quote list for server {interaction.guild.name} ({interaction.guild.id}): {type(e)}: {e}', severity=logging.ERROR)
            return
        await interaction.response.send_message(f'"{quote}" - {author}, {date} was added to the list.')
        await log(f"{interaction.user} added \"{quote} - {author}, {date}\" to the custom quote list for server {interaction.guild.name} ({interaction.guild.id})")
    else:
        await interaction.response.send_message("That's for authorized users, not you...", ephemeral=True)

@tree.command(
    name="removequote",
    description="Removes a quote from the list."
)
async def removequote(interaction: discord.Interaction, quote: str):
    """
    Removes a quote from the list.

    ## Args:
        - quote (str): The quote to remove.
    ## Notes:
        - Only users with bot permissions can use this command.
        - This removes the quote from the custom quote list.
    """
    if has_bot_permissions(interaction.user, interaction.guild):
        try:
            with open(f'data/servers/{str(interaction.guild.id)}/quotes.json') as f:
                quotes = json.load(f)
                if quote in quotes['quotes']:
                    quotes['quotes'].remove(quote)
                else:
                    await interaction.response.send_message("That quote isn't in the list, though...", ephemeral=True)
                    return
            with open('quotes.json', 'w') as f:
                json.dump(quotes, f)
        except Exception as e:
            await interaction.response.send_message(f'Something went wrong. Maybe try again?', ephemeral=True)
            if config["General"]["VerboseErrors"]:
                await interaction.followup.send(f"{type(e)}: {e}\n-# To disable these messages, run /config verboseErrors false")
            await log(f'Failed to remove "{quote}" from the list for server {interaction.guild.name} ({interaction.guild.id}): {type(e)}: {e}', severity=logging.ERROR)
            return
        await interaction.response.send_message(f'"{quote}" was removed from the list.')
        await log(f"{interaction.user} removed \"{quote}\" from the list")
    else:
        await interaction.response.send_message("That's for authorized users, not you...", ephemeral=True)

@tree.command(
    name="channelmaker",
    description="Makes a bunch of channels from JSON."
)
@app_commands.choices(type=[
    app_commands.Choice(name="text",value="text"),
    app_commands.Choice(name="voice",value="voice"),
    app_commands.Choice(name="forum",value="forum"),
])
async def channelmaker(interaction: discord.Interaction, channel_config: str, type: str="text"):
    """
    Makes a bunch of channels from JSON.

    ## Args:
        - channel_config (str): The JSON string containing the channel configuration.
        - type (str): The type of channel to make. Defaults to "text".
    ## Notes:
        - Only users with bot permissions can use this command.
        - The channelmaker JSON configuration looks like this: {"categories":{"test":["test"]}}
        - For more info, read the channelmakerhelpmsg.txt file or run /help channelmaker when the bot is running.
    """
    if has_bot_permissions(interaction.user, interaction.guild):
        await interaction.response.send_message("Making channels! (This may take a moment.)")
        try:
            try:
                channels = json.loads(channel_config) # Channels is a list of categories, each category is a list of channels
            except Exception:
                await interaction.followup.send(f"I couldn't parse that JSON.\n\nIf you need help with using this command, run /help channelmaker.")
                return
            for category in channels['categories']:
                if not category in interaction.guild.categories:
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
        except Exception as e:
            await interaction.followup.send(f"Something went wrong. Maybe try again?")
            if serverConfig(interaction.guild.id)['verboseErrors']:
                await interaction.followup.send(str(e) + "\n-# To disable these messages, run /config verboseErrors false")
            await log(f"Error while making channels in server {str(interaction.guild.name)} ({str(interaction.guild.id)}): {type(e)}: {str(e)}", severity=logging.ERROR)
    else:
        await interaction.response.send_message("That's for authorized users, not you...", ephemeral=True)

@tree.command(
    name="namegenerator",
    description="Generator for names."
)
@app_commands.choices(type=[
    app_commands.Choice(name="first",value="first"),
    app_commands.Choice(name="middle",value="middle"),
    app_commands.Choice(name="last",value="last"),
    app_commands.Choice(name="full",value="full"),
])
@app_commands.choices(gender=[
    app_commands.Choice(name="male",value="male"),
    app_commands.Choice(name="female",value="female"),
    app_commands.Choice(name="none",value="none"),
])
async def namegenerator(interaction: discord.Interaction, type: str="first", gender: str="none"):
    """
    Generator for names.
    """
    name = viviaTools.generate_name(type, gender)
    await interaction.response.send_message(name)

@tree.command(
    name="clearhistory",
    description="Clears your recent chat history with me."
)
async def clearhistory(interaction: discord.Interaction):
    """
    Clears a user's recent chat history with Vivia.
    """
    if os.path.exists(f"data/tempchats/{str(interaction.user.name)}"):
        shutil.rmtree(f"data/tempchats/{str(interaction.user.name)}")
        await interaction.response.send_message("Cleared your chat history with me!", ephemeral=True)
        await log(f"{interaction.user} cleared their chat history", False)
    else:
        await interaction.response.send_message("You haven't chatted with me yet, so there's nothing to clear!", ephemeral=True)
    
@tree.command(
    name="setting",
    description="Manages Vivia's configuration."
)
@app_commands.choices(option=[
    app_commands.Choice(name="AI Enabled",value="aiEnabled"),
    app_commands.Choice(name="Verbose Errors",value="verboseErrors"),
])
async def setting(interaction: discord.Interaction, option: str, value: bool):
    """
    Manages Vivia's configuration.

    ## Notes:
        - Only users with bot permissions can use this command.
    """
    if has_bot_permissions(interaction.user, interaction.guild):
        try:
            match(option):
                case "aiEnabled":
                    changed = serverConfig(interaction.guild.id)
                    changed['aiEnabled'] = value
                    with open(f"data/servers/{interaction.guild.id}/config.json", "w") as f:
                        json.dump(changed, f)
                case "verboseErrors":
                    changed = serverConfig(interaction.guild.id)
                    changed['verboseErrors'] = value
                    with open(f"data/servers/{interaction.guild.id}/config.json", "w") as f:
                        json.dump(changed, f)
                case _:
                    await interaction.response.send_message("That option doesn't seem to exist...", ephemeral=True)
                    return
            await interaction.response.send_message(f"Done! `{option}` is now `{value}`.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Something went wrong. Maybe try again?", ephemeral=True)
            if serverConfig(interaction.guild.id)['verboseErrors']:
                await interaction.followup.send_message(f"{type(e)}: {e}\n-# To disable these messages, run /config verboseErrors false")
            await log(f"Error while changing config for {interaction.guild.name} ({str(interaction.guild.id)}): {type(e)}: {str(e)}", severity=logging.ERROR)
    else:
        await interaction.response.send_message("That's for authorized users, not you...", ephemeral=True)

# Run
while True:
    bot.run(dotenv.get_key("token.env", "token"), log_handler=handler)
