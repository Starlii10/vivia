#!/usr/bin/env python

"""
    This is Vivia's main script.

    Vivia is licensed under the MIT License. For more information, see the LICENSE file.
    TL:DR: you can use Vivia's code as long as you keep the original license intact.
    Vivia is made open source in the hopes that you'll find her code useful.

    If you'd like to contribute, please check out the GitHub repository at https://github.com/starlii10/vivia.

    Have a great time using Vivia!
"""

# Vivia version
__VERSION__ = "Vivia 20241127"

if __name__ != "__main__":
    print("              ██▓▓▓▓▓▓▓██                            ██▓▓▓▓▓▓▓██                \n               ███▓▓▓▓██                              ███▓▓▓███                 \n                 ██████                                 █████                   \n                   ████                                ████                     \n                    ███   █████████████████████████    ███                      \n                    ██████████████████████████████████████                      \n                 █████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████████                     \n               ██████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████                  \n             █████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████                \n            ████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█████              \n           ████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█████             \n         █████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████            \n        ████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████           \n        ███▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█████████████████▓▓▓▓▓▓▓▓▓▓▓▓▓████          \n       ████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████████████████████████████▓▓▓▓▓▓▓▓▓▓▓████         \n      ████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████████████████████████████▓▓▓▓▓▓▓▓▓▓███         \n      ███▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████████████████████████████████▓▓▓▓▓▓▓▓████        \n      ███▓▓▓▓▓▓▓▓▓▓▓▓███████████████████████░░░░░▒██████▒█████▓▓▓▓▓▓████        \n      ███▓▓▓▓▓▓▓▓███████████████████████████████▓░░░██████▒████████████         \n      ████▓▓▓████████▓▓████████████████████▒░░▒████████████▒▒▓████████          \n       ███████████▒▒▒▒██████████▒▒▒███████▒░░░░▒███████████▒▒▒▒▒▒▒████          \n         ██████▒▒▒▒▒▒██████████▒░░░░▒▒████▒░░░░▒████████████▒▒▒▒▒▒████          \n           ███▒▒▒▒▒▒▒█████████▒░░░░░░░░▒██▒░░░░▒████████████▒▒▒▒▒▒▒███          \n           ███▒▒▒▒▒▒▓████████▒░░░░░░░░░▒██▒░░░░▒█████████████▒▒▒▒▒▒███          \n           ███▒▒▒▒▒▒█████████▒░░░░▒▓▒▒▒███▒░░░░▒█████████████▒▒▒▒▒▒███          \n           ███▒▒▒▒▒▒▓█████████████████████▒░░░░▓█████████████▒▒▒▒▒▒███          \n           ███▓▒▒▒▒▒▒███████████████████████▓███████████████▒▒▒▒▒▒▒███          \n           ████▒▒▒▒▒▒███████████████████████████████████████▒▒▒▒▒▒████          \n            ███▒▒▒▒▒▒▒█████████████████████████████████████▒▒▒▒▒▒▒███           \n            ████▒▒▒▒▒▒▒███████████▒░░░▒███▒░░░▒███████████▒▒▒▒▒▒▒████           \n             ████▒▒▒▒▒▒▒█████████▓░░░░░░░░░░░░░▓█████████▒▒▒▒▒▒▒████            \n              ████▒▒▒▒▒▒▒█████████▒░░░░░░░░░░▒▓█████████▒▒▒▒▒▒▒▓████            \n               ████▒▒▒▒▒▒▒▒█████████▓▒▒░░▒▒▒██████████▒▒▒▒▒▒▒▒████▓██  ███      \n                ████▒▒▒▒▒▒▒▒▒███████████████████████▒▒▒▒▒▒▒▒▒█████▒▓███▓██      \n                 █████▒▒▒▒▒▒▒▒▒▒█████████████████▒▒▒▒▒▒▒▒▒▒▓███████▒▒▒███       \n                   █████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓████ █████████        \n                    ██████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██████ ███▓▓▓███         \n                       ██████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒███████  ███▓▓▓███          \n                       ███████████▓▒▒▒▒▒▒▒▒▒▒▒▓███████████  ███▓▓▓███           \n                      ████▓▓▓███████████████████████▓▓▓████ ██▓▓▓▓███           \n                     ████▓▓▓▓▓▓▓▓▓▓███████████▓▓▓▓▓▓▓▓▓▓████████▓███            \n                  ███████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████████             \n               █████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███▒▒▒▓████            \n              ████▒▒▒███▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███▒▒▒▒▒████           \n\"Please don't try to import me as a module... I'm not used to my entire existence being tied to a program I have no control over.\"")
    print("Psst! If you're looking for helper functions, you probably want ViviaTools (import extras.viviatools).")
    exit(0)

# Imports
import sys
import concurrent
import asyncio
import shutil
import json
import threading
import time
import traceback
from aiohttp import ClientConnectorError
import discord.ext.commands
import dotenv
import random
import os
from os import system
import logging
import argparse

# Discord
import discord, discord.ext
from discord import GatewayNotFound, HTTPException, LoginFailure, app_commands
from discord.ext import tasks, commands, commands
from discord.ext.commands import errors
from discord.ext.commands.errors import CommandError

# ViviaTools
import extras.viviatools as viviatools
from extras.viviatools import config, perServerFile, serverConfig, personalityMessage

# Command line args
argparser = argparse.ArgumentParser()
argparser.add_argument("--version", action="store_true", help="Print version and exit")
argparser.add_argument("--debug", action="store_true", help="Enable debug mode for this session")
argparser.add_argument("--beta", action="store_true", help="Enable loading ViviaBase-beta extensions")
argparser.add_argument("--disable-sharded", action="store_true", help="Disable sharded mode for this session")
argparser.add_argument("--token", help="Discord bot token")

args = argparser.parse_args()

# Determine configs
debug = args.debug or config['Advanced']['Debug'] == "True"
sharded = not args.disable_sharded and config['Advanced']['Sharded'] == "True"
betaExtensions = args.beta or config['Extensions']['BetaExtensions'] == "True"
if not args.token:
    token = dotenv.get_key("token.env", "token")
else:
    token = args.token

# LLaMa
# TODO: this is slow, run it in a separate thread
import extras.viviallama as Llama

# Variables
current_status = "Vivia is powering up..."

# Terminal title
if sys.platform == 'win32':
    # Windows
    system(f"title Running {__VERSION__}")
else:
    # Linux/Unix. Should work on most unix systems, if not please open an issue
    system(f"echo -ne '\033]0;Running {__VERSION__}\007'")

# Configure bot settings
intents = discord.Intents.default()
intents.message_content = True # requires verification after reaching 100 servers
if sharded:
    bot = commands.AutoShardedBot(command_prefix=config['General']['Prefix'], intents=intents)
else:
    viviatools.log("Sharded mode is disabled - running in non-sharded mode, performance may be degraded", logging.WARNING)
    bot = commands.Bot(command_prefix=config['General']['Prefix'], intents=intents)
bot.remove_command("help")
tree = bot.tree

# Set viviatools references
viviatools.set_refs(bot)

# Events
@bot.event
async def setup_hook():
    """
    Function called early in Vivia's initialization process.
    """

    # skip if Vivia is already running
    if viviatools.running:
        viviatools.log("Vivia is already running. Skipping early initialization process", logging.DEBUG)
        return

    viviatools.log("Searching for VSE extensions...")

    # Load VSEs
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for root, dirs, files in os.walk("commands"):
            for file in files:
                if file.endswith(".vse"):
                    futures.append(executor.submit(viviatools.extractVSE, os.path.join(root, file)))
        for future in concurrent.futures.as_completed(futures):
            if future.exception():
                viviatools.log(f"Failed to extract VSE extension {future.result()[1]}", logging.ERROR)
                viviatools.log("".join(traceback.format_exception(future.exception())), logging.ERROR)
                viviatools.log("VSE extension will not be loaded - functionality may be limited.", logging.ERROR)
                if debug:
                    os.remove(os.path.join(future.result()[0], future.result()[1]))
            else:
                viviatools.log(f"VSE extension {future.result()[1]} extracted", logging.DEBUG)
    
    # Create server data folder
    if not os.path.exists(os.path.join("data", "servers")):
        os.makedirs(os.path.join("data", "servers"))
    viviatools.log("VSE extensions extracted.")

@bot.event
async def on_error(event, *args, **kwargs):
    """
    Function called when an error is raised in Vivia.
    """

    viviatools.log(f"Error in event {event}!\n{''.join(traceback.format_exception(*sys.exc_info()))}", logging.ERROR)
    viviatools.log(f"(Error args: {args} | Error kwargs: {kwargs})", logging.DEBUG)
    # attempt to send generic error message
    try:
        await args[0].send(personalityMessage("errors.error"))
    except:
        viviatools.log("Failed to send error message to user", logging.ERROR)

@tree.error
async def on_app_command_error(interaction, error: app_commands.AppCommandError):
    """
    Function called when an app command error is raised in Vivia.

    This function handles errors derived from `discord.app_commands.AppCommandError`.
    """

    viviatools.log(f"App command error in interaction {interaction}!\n{''.join(traceback.format_exception(*sys.exc_info()))}", logging.ERROR)
    match type(error):
        case app_commands.CommandSignatureMismatch:
            # Command out of sync - usually because v!sync was run
            await interaction.response.send_message(personalityMessage("errors.commandoutofsync"))
        case app_commands.CommandNotFound:
            # Command not found
            await interaction.response.send_message(personalityMessage("errors.commandnotfound"))
        case _:
            # Anything else
            await interaction.response.send_message(personalityMessage("errors.error"))

@bot.event
async def on_command_error(ctx: commands.Context, error: CommandError):
    """
    Function called when a command error is raised in Vivia.
    """

    errtype = type(error)
    match errtype:
        case errors.CommandNotFound:
            # Command not found
            viviatools.log(f"Command not found: {ctx.invoked_with}", logging.WARNING)
            await ctx.send(personalityMessage("errors.commandnotfound"))
        case errors.MissingRequiredArgument:
            # Missing argument
            viviatools.log(f"Missing required argument(s) in 'v!{ctx.invoked_with}': {error.param.name}", logging.WARNING)
            viviatools.log("".join(traceback.format_exception(error)), logging.WARNING)
            await ctx.send(personalityMessage("errors.missingarguments").replace("{arg}", error.param.name))
        case errors.BadArgument:
            # Invalid argument
            viviatools.log(f"Bad argument(s) in 'v!{ctx.invoked_with}': {error.param.name}", logging.WARNING)
            viviatools.log("".join(traceback.format_exception(error)), logging.WARNING)
            await ctx.send(personalityMessage("errors.badarguments").replace("{arg}", error.param.name))
        case errors.BotMissingPermissions | errors.MissingPermissions:
            # Vivia is missing permissions
            viviatools.log(f"Missing permissions in 'v!{ctx.invoked_with}': {error.missing_permissions}", logging.WARNING)
            viviatools.log("".join(traceback.format_exception(error)), logging.WARNING)
            await ctx.send(personalityMessage("errors.missingpermissions").replace("{perms}", ", ".join(error.missing_permissions)))
        case errors.CommandInvokeError:
            # General command error
            viviatools.log(f"Command invoke error in 'v!{ctx.invoked_with}': {error}", logging.WARNING)
            viviatools.log("".join(traceback.format_exception(error)), logging.WARNING)
            await ctx.send(personalityMessage("errors.error"))
        case _:
            # Anything else
            viviatools.log(f"An unhandled error occurred in 'v!{ctx.invoked_with}': " + "".join(traceback.format_exception(error)), logging.ERROR)
    viviatools.log(f"Error context: \nGuild: {ctx.guild}\nChannel: {ctx.channel}\nMessage: {ctx.message}\nUser: {ctx.author}", logging.DEBUG)

@bot.event
async def on_ready():
    """
    Function called when Vivia starts up.
    """

    # skip if Vivia is already running
    if viviatools.running:
        viviatools.log("Vivia is already running. Skipping initialization process.")
        await statusChanges() # get rid of temporary "Connecting to websocket" status
        return
    
    viviatools.log("Connected to websocket - powering on!")
    
    # Load extensions
    viviatools.log("Loading extensions!")
    await viviatools.setCustomPresence("POWERING UP - Loading extensions...", bot)
    await reload_all_extensions()
    
    # Statuses
    try:
        statusChanges.start()
    except RuntimeError:
        pass # already started
    viviatools.log("Vivia is all ready!")
    viviatools.running = True

@tasks.loop(hours=1)
async def statusChanges():
    """
    Changes the bot's status every hour.
    """
    # statuses are now stored in data/statuses/*.json to support extensions that add their own statuses
    statuses = []
    for file in os.listdir("data/statuses"):
        if file.endswith(".json"):
            with open(os.path.join("data", "statuses", file), "r") as f:
                statuses.extend(json.load(f)["statuses"])
    status = random.choice(statuses)
    await viviatools.setCustomPresence(status, bot)
    viviatools.log(f"Status changed to {status}", logging.DEBUG)

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

    viviatools.log(f"Bot joined {guild.name} ({guild.id})")

    def setup_guild_data():
        if debug:
            viviatools.log(f"Setting up custom quotes, config file, and Vivia admin role for {guild.name} ({guild.id})", logging.DEBUG)
        with open(os.path.join('data', 'servers', str(guild.id), 'quotes.json'), 'w') as f:
            json.dump({'quotes': []}, f)
        with open(os.path.join('data', 'servers', str(guild.id), 'config.json'), 'w') as f, open(os.path.join('data', 'config.json.example'), 'r') as g:
            json.dump(json.load(g), f)

    def setup_roles():
        for member in guild.members:
            if member.guild_permissions.administrator:
                role = discord.utils.find(lambda r: r.name == "Vivia Admin", guild.roles)
                if role is None:
                    role = asyncio.run_coroutine_threadsafe(guild.create_role(name="Vivia Admin", reason="Vivia setup: Users with this role have privileges when running Vivia's commands in this server."), bot.loop).result()
                asyncio.run_coroutine_threadsafe(member.add_roles(role, reason="Vivia setup: This user has administrative permissions and was automatically assigned to the Vivia Admin role."), bot.loop)
                viviatools.log(f"User {member.name} ({member.id}) was automatically assigned the Vivia Admin role in {guild.name} ({guild.id}).", logging.DEBUG)

    threads = [
        threading.Thread(target=setup_guild_data),
        threading.Thread(target=setup_roles)
    ]

    for t in threads:
        t.start()

    if debug:
        viviatools.log(f"Setup complete for {guild.name} ({guild.id})", logging.DEBUG)

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

    # Invoke LLaMa if pinged
    # DMs (need to be checked separately because the message.guild attribute is None in DMs)
    if not message.guild:
        await message.channel.typing()
        thread = threading.Thread(target=Llama.createResponse, args=((message.content,
                                                                    message.author.display_name,
                                                                    message.author.name,
                                                                    message.channel,
                                                                    bot.loop,
                                                                    message.attachments,
                                                                    message.author.raw_status,
                                                                    current_status,
                                                                    "DMs",
                                                                    "DMs",
                                                                    "DMs")))
        thread.start()
        return
    
    # Guilds
    if serverConfig(message.guild.id)['aiEnabled']:
        # we need to check both for direct mentions of Vivia and for mentions of the Vivia role to prevent confusion
        if (message.mentions and (message.mentions[0] == bot.user or message.role_mentions[0] == discord.utils.get(message.guild.roles, name="Vivia"))):
                await message.channel.typing()
                thread = threading.Thread(target=Llama.createResponse, args=((message.content.removeprefix(f"<@{str(message.author.id)}>"),
                                                    message.author.display_name,
                                                    message.author.name,
                                                    message.channel,
                                                    bot.loop,
                                                    message.attachments,
                                                    message.author.raw_status,
                                                    current_status,
                                                    message.guild.name,
                                                    message.channel.name,
                                                    message.channel.category.name)))
                thread.start()
                return

async def reload_all_extensions():
    """
    Reloads EVERY extension Vivia can find.
    """

    # Unload all extensions
    unload_threads = [threading.Thread(target=asyncio.run, args=(viviatools.unload_extension(extension),)) for extension in viviatools.loaded_extensions]
    for thread in unload_threads:
        thread.start()
    for thread in unload_threads:
        thread.join()

    # Reset list of extensions
    viviatools.loaded_extensions = ["core"] # Vivia core is always loaded
    viviatools.failed_extensions = []

    # Load extensions
    load_tasks = []

    # ViviaBase
    for extension in os.listdir(os.path.join("commands", "viviabase")):
        if extension.endswith(".py"):
            load_tasks.append(threading.Thread(target=asyncio.run, args=(viviatools.load_extension(extension, "commands.viviabase"),)))
        
    # ViviaBase-beta if enabled
    if betaExtensions:
        for extension in os.listdir(os.path.join("commands", "viviabase-beta")):
            if extension.endswith(".py"):
                load_tasks.append(threading.Thread(target=asyncio.run, args=(viviatools.load_extension(extension, "commands.viviabase-beta"),)))

    # Custom commands
    for extension in os.listdir(os.path.join("commands")):
        if extension.endswith(".py"):
            load_tasks.append(threading.Thread(target=asyncio.run, args=(viviatools.load_extension(extension, "commands"),)))

    for task in load_tasks:
        if task:
            task.start()

    for task in load_tasks:
        if task:
            task.join()

    viviatools.log(f"Loaded {len(viviatools.loaded_extensions)} extensions - failed loading {len(viviatools.failed_extensions)}.")

# Core commands
# These commands are always available

@bot.hybrid_command()
@viviatools.ownerOnly
async def sync(ctx, guild: int=0):
    """
    Syncs the command tree.

    ## Notes:
        - Only the bot owner can use this command.
        - If you want to sync the entire bot, use "v!sync 0" or "v!sync". Otherwise specify the ID of the guild you want to sync.
        - Syncing the entire bot requires up to 1 hour. This is a Discord limitation and I (and DPY devs) can't do anything about it.
    """

    if guild == 0:
        await bot.tree.sync()
        await ctx.send('The command tree was synced, whatever that means.')
        viviatools.log("The command tree was synced, whatever that means.")
    else:
        await bot.tree.sync(guild=discord.utils.get(bot.guilds, id=guild))
        await ctx.send(f'The command tree was synced for {guild}, whatever that means.')
        viviatools.log(f"The command tree was synced for {guild}, whatever that means.")

@bot.hybrid_command()
@viviatools.ownerOnly
async def fixconfig(ctx: commands.Context):
    """
    Regenerates server files for servers where they are missing.

    ## Notes:
        - Only the bot owner can use this command.
    """

    viviatools.log(f"Regenerating missing data files for all servers...", logging.DEBUG)
    threads = []
    for guild in bot.guilds:
        t = threading.Thread(target=regen_server_files, args=(guild,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    await ctx.send('Fixed all missing config and quotes files. Check log for more info.')

# the actual function
def regen_server_files(guild):
    # Regenerate server data path if it doesn't exist
    if not os.path.exists(os.path.join('data', 'servers', str(guild.id))):
        os.mkdir(os.path.join('data', 'servers', str(guild.id)))
        viviatools.log(f'Data path for {guild.name} ({guild.id}) was regenerated.', logging.DEBUG)

        # Regenerate configuration if guild config is missing
        try:
            with open(os.path.join('data', 'servers', str(guild.id), 'config.json'), 'x') as f, open(os.path.join('data', 'config.json.example'), 'r') as g:
                json.dump(obj=json.load(g), fp=f)
            viviatools.log(f'Config file for {guild.name} ({guild.id}) was regenerated.', logging.DEBUG)
        except FileExistsError:
            pass # Most likely there was nothing wrong with it

        # Regenerate quotes if guild quotes is missing
        try:
            with open(os.path.join('data', 'servers', str(guild.id), 'quotes.json'), 'x') as f:
                json.dump({'quotes': []}, f)
            viviatools.log(f'Custom quote file for {guild.name} ({guild.id}) was regenerated.', logging.DEBUG)
        except FileExistsError:
            pass # Most likely there was nothing wrong with it

        # Regenerate warns if guild warns is missing
        try:
            with open(os.path.join('data', 'servers', str(guild.id), 'warns.json'), 'x') as f:
                json.dump({'warns': []}, f)
            viviatools.log(f'Warn file for {guild.name} ({guild.id}) was regenerated.', logging.DEBUG)
        except FileExistsError:
            pass # Most likely there was nothing wrong with it

@bot.hybrid_command(
    name="statuschange",
    description="Manually randomizes the current status of the bot."
)
@viviatools.ownerOnly
async def statuschange(ctx: commands.Context):
    """
    Manually randomizes the current status of the bot.

    ## Notes:
        - Only the bot owner can use this command.
    """

    await statusChanges()
    await ctx.send('Status randomized!')

@bot.hybrid_command(
    name="clearhistory",
    description="Clears your recent chat history with me."
)
async def clearhistory(ctx: commands.Context):
    """
    Clears a user's recent chat history with Vivia.
    """
    if os.path.exists(os.path.join("data", "tempchats", str(ctx.author.name))):
        shutil.rmtree(os.path.join("data", "tempchats", str(ctx.author.name)))
        await ctx.send(personalityMessage("ai.historyclear"), ephemeral=True)
        viviatools.log(f"{ctx.author.name} cleared their chat history", logging.DEBUG)
    else:
        await ctx.send(personalityMessage("ai.nohistory"), ephemeral=True)
    
@bot.hybrid_command(
    name="setting",
    description="Manages Vivia's configuration."
)
@app_commands.choices(option=[
    app_commands.Choice(name="AI Enabled",value="aiEnabled"),
    app_commands.Choice(name="Verbose Errors",value="verboseErrors"),
])
@viviatools.adminOnly
async def setting(ctx: commands.Context, option: str, value: bool):
    """
    Manages Vivia's configuration for a specific server.

    ## Notes:
        - Only users with Vivia admin permissions can use this command.
    """

    try:
        match(option):
            case "aiEnabled":
                changed = serverConfig(ctx.guild.id)
                changed['aiEnabled'] = value
                with open(f"data/servers/{ctx.guild.id}/config.json", "w") as f:
                    json.dump(changed, f)
            case "verboseErrors":
                changed = serverConfig(ctx.guild.id)
                changed['verboseErrors'] = value
                with open(f"data/servers/{ctx.guild.id}/config.json", "w") as f:
                    json.dump(changed, f)
            case _:
                await ctx.send("That option doesn't seem to exist...", ephemeral=True)
                return
        await ctx.send(f"Done! `{option}` is now `{value}`.", ephemeral=True)
    except Exception as e:
        await ctx.send(personalityMessage("errors.error"), ephemeral=True)
        if serverConfig(ctx.guild.id)['verboseErrors']:
            await ctx.send(f"{str(type(e))}: {e}\n-# To disable these messages, run /config verboseErrors false")
        viviatools.log(f"Error while changing config for {ctx.guild.name} ({str(ctx.guild.id)}): {str(type(e))}: {str(e)}", severity=logging.ERROR)

@bot.hybrid_command(
    name="extensions",
    description="Manages Vivia's extensions for a specific server."
)
@viviatools.adminOnly
async def extensions(ctx: commands.Context, extension: str, value: bool):
    """
    Manages Vivia's extensions for a specific server.

    ## Notes:
        - Only users with Vivia admin permissions can use this command.
    """

    with perServerFile(ctx.guild.id, "extensions.json") as f:
        extensions = json.load(f)
        extensions[extension] = value
        json.dump(extensions, f)

    await ctx.send(f"Done! `{extension}` is now {value and 'enabled' or 'disabled'}.", ephemeral=True)

    # TODO: Handle extension unloading for individual servers

@bot.hybrid_command(
    name="reboot",
    description="Performs a full reboot of Vivia."
)
@viviatools.ownerOnly
async def reboot(ctx: commands.Context, pull_git: bool = False):
    """
    Performs a full reboot of Vivia.

    ## Args:
        pull_git (bool): Whether to pull the git repository before rebooting to automatically update Vivia.
                         Defaults to False. May increase reboot time by a few seconds. Also updates dependencies.
    ## Notes:
        - Only the bot owner can use this command.
        - Because this command replaces the running Vivia script with another one, any changes made to Vivia will take effect after this command is run.
        - `pull_git` requires `git` to be installed on your system, but you probably already have it if you're running Vivia anyway, don't you?
        - `pull_git` will also run `pip install -r requirements.txt` in the root to install any new dependencies.
        - `pull_git` will OVERRIDE LOCAL CHANGES TO VIVIA! Be careful! (This does not affect custom extensions.)
    """

    await ctx.send("Rebooting...")
    viviatools.log(f"Rebooting on request of {ctx.author.name} ({str(ctx.author.id)})...")
    await bot.close()
    if pull_git:
        try:
            os.system("git pull")
            viviatools.log("Pulled git repository.", logging.DEBUG)
            # NOTE: pip command may be different on different systems, this may fail
            os.system("pip install -r requirements.txt")
            viviatools.log("Installed new dependencies.", logging.DEBUG)
        except Exception as e:
            viviatools.log(f"Failed to pull git repository: {str(type(e))}: {str(e)}", logging.ERROR)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.hybrid_command(
    name="listextensions",
    description="Displays Vivia's available extensions."
)
async def listextensions(ctx: commands.Context):
    """
    Displays Vivia's available extensions.
    """
    await ctx.send("Available extensions: \n- " + ("\n- ".join(viviatools.loaded_extensions)) if len(viviatools.loaded_extensions) > 0 else "No extensions loaded? Wait, what?!", ephemeral=True)
    await ctx.send("Extensions that failed to load: \n- " + ("\n- ".join(viviatools.failed_extensions)) if len(viviatools.failed_extensions) > 0 else "No extensions failed to load!", ephemeral=True)

@bot.hybrid_command(
    name="version",
    description="Displays Vivia's version."
)
async def version(ctx: commands.Context):
    """
    Displays Vivia's version.
    """
    await ctx.send(personalityMessage("base.version").replace("{version}", __VERSION__), ephemeral=True)

# Run
while True:
    try:
        bot.activity = discord.CustomActivity(name="POWERING UP - Connecting to Discord...")
        bot.run(token, log_handler=None)
    except TypeError:
        viviatools.log("Unable to start Vivia. Is the token in token.env correct?", logging.ERROR)
        viviatools.log("If token.env doesn't exist, create it and place your bot token inside.", logging.ERROR)
        sys.exit(1)
    except discord.errors.LoginFailure:
        viviatools.log("Unable to start Vivia. Is the token in token.env correct?", logging.ERROR)
        sys.exit(1)
    except RuntimeError as e:
        if "Session is closed" in str(e):
            viviatools.log("Session closed. Vivia is shutting down!", logging.INFO)
            sys.exit(0)
    except (ClientConnectorError, GatewayNotFound, HTTPException, LoginFailure):
        viviatools.log("Vivia can't connect to Discord. Is your internet connection working, or is Discord's API down?", logging.ERROR)
        viviatools.log("Perhaps the token in token.env is invalid? There's a lot of reasons this could happen.", logging.ERROR)
        viviatools.log("Vivia will retry in 5 seconds.", logging.ERROR)
        time.sleep(5)
        os.execl(sys.executable, sys.executable, *sys.argv) # Using bot.run again will just give a "Session is closed" error and crash the script
    except Exception as e:
        # Unhandled exception
        viviatools.log(f"Vivia has crashed... oh no...", logging.FATAL)
        viviatools.log("".join(traceback.format_exception(sys.exc_info())), severity=logging.FATAL)
        viviatools.log("Don't worry, she will automatically restart in 5 seconds.", logging.FATAL)
        viviatools.log("I would appreciate if you would report this on GitHub, please.", logging.FATAL)
        asyncio.run(viviatools.setCustomPresence("!! Vivia has crashed - rebooting! !!", "dnd", bot))
        time.sleep(5)
        os.execl(sys.executable, sys.executable, *sys.argv)
