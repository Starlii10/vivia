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
__VERSION__ = "Vivia 20241025"


# Imports
import sys


if __name__ != "__main__": # prevent running as a module, and print ASCII art Vivia!
    print("              ██▓▓▓▓▓▓▓██                            ██▓▓▓▓▓▓▓██                \n               ███▓▓▓▓██                              ███▓▓▓███                 \n                 ██████                                 █████                   \n                   ████                                ████                     \n                    ███   █████████████████████████    ███                      \n                    ██████████████████████████████████████                      \n                 █████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████████                     \n               ██████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████                  \n             █████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████                \n            ████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█████              \n           ████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█████             \n         █████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████            \n        ████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████           \n        ███▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█████████████████▓▓▓▓▓▓▓▓▓▓▓▓▓████          \n       ████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████████████████████████████▓▓▓▓▓▓▓▓▓▓▓████         \n      ████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████████████████████████████▓▓▓▓▓▓▓▓▓▓███         \n      ███▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████████████████████████████████▓▓▓▓▓▓▓▓████        \n      ███▓▓▓▓▓▓▓▓▓▓▓▓███████████████████████░░░░░▒██████▒█████▓▓▓▓▓▓████        \n      ███▓▓▓▓▓▓▓▓███████████████████████████████▓░░░██████▒████████████         \n      ████▓▓▓████████▓▓████████████████████▒░░▒████████████▒▒▓████████          \n       ███████████▒▒▒▒██████████▒▒▒███████▒░░░░▒███████████▒▒▒▒▒▒▒████          \n         ██████▒▒▒▒▒▒██████████▒░░░░▒▒████▒░░░░▒████████████▒▒▒▒▒▒████          \n           ███▒▒▒▒▒▒▒█████████▒░░░░░░░░▒██▒░░░░▒████████████▒▒▒▒▒▒▒███          \n           ███▒▒▒▒▒▒▓████████▒░░░░░░░░░▒██▒░░░░▒█████████████▒▒▒▒▒▒███          \n           ███▒▒▒▒▒▒█████████▒░░░░▒▓▒▒▒███▒░░░░▒█████████████▒▒▒▒▒▒███          \n           ███▒▒▒▒▒▒▓█████████████████████▒░░░░▓█████████████▒▒▒▒▒▒███          \n           ███▓▒▒▒▒▒▒███████████████████████▓███████████████▒▒▒▒▒▒▒███          \n           ████▒▒▒▒▒▒███████████████████████████████████████▒▒▒▒▒▒████          \n            ███▒▒▒▒▒▒▒█████████████████████████████████████▒▒▒▒▒▒▒███           \n            ████▒▒▒▒▒▒▒███████████▒░░░▒███▒░░░▒███████████▒▒▒▒▒▒▒████           \n             ████▒▒▒▒▒▒▒█████████▓░░░░░░░░░░░░░▓█████████▒▒▒▒▒▒▒████            \n              ████▒▒▒▒▒▒▒█████████▒░░░░░░░░░░▒▓█████████▒▒▒▒▒▒▒▓████            \n               ████▒▒▒▒▒▒▒▒█████████▓▒▒░░▒▒▒██████████▒▒▒▒▒▒▒▒████▓██  ███      \n                ████▒▒▒▒▒▒▒▒▒███████████████████████▒▒▒▒▒▒▒▒▒█████▒▓███▓██      \n                 █████▒▒▒▒▒▒▒▒▒▒█████████████████▒▒▒▒▒▒▒▒▒▒▓███████▒▒▒███       \n                   █████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓████ █████████        \n                    ██████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██████ ███▓▓▓███         \n                       ██████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒███████  ███▓▓▓███          \n                       ███████████▓▒▒▒▒▒▒▒▒▒▒▒▓███████████  ███▓▓▓███           \n                      ████▓▓▓███████████████████████▓▓▓████ ██▓▓▓▓███           \n                     ████▓▓▓▓▓▓▓▓▓▓███████████▓▓▓▓▓▓▓▓▓▓████████▓███            \n                  ███████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████████             \n               █████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███▒▒▒▓████            \n              ████▒▒▒███▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███▒▒▒▒▒████           \n\"Please don't try to import me as a module... I'm not used to my entire existence being tied to a program I have no control over.\"")
    print("Psst! If you're looking for helper functions, you probably want ViviaTools (import extras.viviatools).")
    sys.exit(0)

# Back to imports lol
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

# Discord
import discord, discord.ext
from discord import GatewayNotFound, HTTPException, LoginFailure, app_commands
from discord.ext import tasks, commands, commands
from discord.ext.commands import errors
from discord.ext.commands.errors import CommandError

# ViviaTools
import extras.viviatools as viviatools
from extras.viviatools import config, serverConfig, personalityMessage

# Command line args
if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        match arg:
            case "--help" | "-h" | "--h" | "-help" | "/?" | "/h" | "/help":
                viviatools.log("Usage: python bot.py", logging.INFO)
                viviatools.log("For help with Vivia, please check out the GitHub repository at https://github.com/starlii10/vivia.", logging.INFO)
                sys.exit(0)
            case "--version" | "-v" | "--v" | "-version" | "-version" | "/v" | "/version":
                viviatools.log(f"Version {__VERSION__}", logging.INFO)
                sys.exit(0)
            case _:
                viviatools.log("Unknown argument: " + arg, logging.ERROR)
                sys.exit(1)

# LLaMa
import extras.viviallama as Llama

# Variables
current_status = "Vivia is powering up..."

# Terminal title. VSCode will scream at you that one of these is unreachable, ignore it
if sys.platform == 'win32':
    # Windows title
    system(f"title Running {__VERSION__}")
else:
    # Linux title (if this doesn't work on your distro please open an issue because I suck at Linux)
    system(f"echo -ne '\033]0;Running {__VERSION__}\007'")

# Configure bot settings
intents = discord.Intents.default()
intents.message_content = True # will need to verify at 100 servers
bot = commands.Bot(command_prefix=config['General']['Prefix'], intents=intents)
bot.remove_command("help") # because we hate the default help command
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

    # Load VSCs
    for root, dirs, files in os.walk("commands"):
        for file in files:
            if file.endswith(".vse"):
                try:
                    viviatools.extractVSE(os.path.join(root, file))
                except Exception as e:
                    viviatools.log(f"Failed to extract VSE extension {file}", logging.ERROR)
                    viviatools.log(f"{str(type(e))}: {e}", logging.ERROR)
                    viviatools.log("VSE extension will not be loaded - functionality may be limited.", logging.ERROR)
                    if config['Advanced']['Debug'] != "True":
                        os.remove(os.path.join(root, file))
                else:
                    viviatools.log(f"VSE extension {file} extracted", logging.DEBUG)
    
    # Create server data folder
    if not os.path.exists("data/servers"):
        os.makedirs("data/servers")

    viviatools.log("VSE extensions extracted.")

@bot.event
async def on_error(event, *args, **kwargs):
    """
    Function called when an error is raised in Vivia.
    """

    viviatools.log(f"Error in event {event}!\n{''.join(traceback.format_exception(*sys.exc_info()))}", logging.ERROR)
    viviatools.log(f"(Error args: {args} | Error kwargs: {kwargs})", logging.DEBUG)

@bot.event
async def on_command_error(ctx: commands.Context, error: CommandError):
    """
    Function called when a command error is raised in Vivia.
    """

    errtype = type(error)
    match errtype:
        case errors.CommandNotFound:
            viviatools.log(f"Command not found: {ctx.invoked_with}", logging.WARNING)
            await ctx.send(personalityMessage("commandnotfound"))
        case errors.MissingRequiredArgument:
            viviatools.log(f"Missing required argument(s) in 'v!{ctx.invoked_with}': {error.param.name}", logging.WARNING)
            viviatools.log("".join(traceback.format_exception(error)), logging.WARNING)
            await ctx.send(personalityMessage("missingarguments").replace("{arg}", error.param.name))
        case errors.BadArgument:
            viviatools.log(f"Bad argument(s) in 'v!{ctx.invoked_with}': {error.param.name}", logging.WARNING)
            viviatools.log("".join(traceback.format_exception(error)), logging.WARNING)
            await ctx.send(personalityMessage("badarguments").replace("{arg}", error.param.name))
        case errors.BotMissingPermissions | errors.MissingPermissions:
            viviatools.log(f"Missing permissions in 'v!{ctx.invoked_with}': {error.missing_permissions}", logging.WARNING)
            viviatools.log("".join(traceback.format_exception(error)), logging.WARNING)
            await ctx.send(personalityMessage("missingpermissions"))
        case errors.CommandInvokeError:
            viviatools.log(f"Command invoke error in 'v!{ctx.invoked_with}': {error}", logging.WARNING)
            viviatools.log("".join(traceback.format_exception(error)), logging.WARNING)
            await ctx.send(personalityMessage("error"))
        case _:
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
    with open("data/statuses.json", "r") as f:
        statuses = json.load(f)
    status = random.choice(statuses["statuses"])
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
    if config["Advanced"]["Debug"] == "True":
        viviatools.log(f"Setting up custom quotes, config file, and Vivia admin role for {guild.name} ({guild.id})", logging.DEBUG)
    with open(f'data/servers/{guild.id}/quotes.json', 'w') as f:
        json.dump({'quotes': []}, f)
    with open(f'data/servers/{guild.id}/config.json', 'w') as f, open(f'data/config.json.example', 'r') as g:
        json.dump(g, f)
    await guild.create_role(name="Vivia Admin", reason="Vivia setup: Users with this role have privileges when running Vivia's commands in this server.")
    for member in guild.members:
        if member.guild_permissions.administrator:
            await member.add_roles(discord.utils.find(lambda r: r.name == "Vivia Admin", guild.roles), reason="Vivia setup: This user has administrative permissions and was automatically assigned to the Vivia Admin role.")
            viviatools.log(f"User {member.name} ({member.id}) was automatically assigned the Vivia Admin role in {guild.name} ({guild.id}).", logging.DEBUG)
    if config["Advanced"]["Debug"] == "True":
        viviatools.log(f"Setup complete for {guild.name} ({guild.id})", logging.DEBUG)    

@bot.event
async def on_message(message: discord.Message):
    """
    Function called when a message is sent.
    """

    # Make sure Vivia doesn't respond to herself
    if message.author == bot.user:
        return
    
    # Ignore DMs
    # TODO: Vivia LLaMa triggers in DMs
    if message.guild == None:
        return

    # Process commands
    await bot.process_commands(message)

    # Invoke LLaMa if pinged (this also works for replies)
    # "Starlii when will this be async?" Good question
    if serverConfig(message.guild.id)['aiEnabled']:
        # we need to check both for direct mentions of Vivia and for mentions of the Vivia role to prevent confusion
        if (message.mentions and (message.mentions[0] == bot.user or message.role_mentions[0] == discord.utils.get(message.guild.roles, name="Vivia"))):
            async with message.channel.typing():
                threading.Thread(target=llamaReply, args=(message,)).start()


def llamaReply(message: discord.Message):
    """
    Gets a reply using LLaMa.
    This has to be a separate (non-async) function because threads.
    """
    
    generation_fut = asyncio.run_coroutine_threadsafe(Llama.createResponse(message.content.removeprefix(f"<@{str(message.author.id)}> "),
                                                    message.author.display_name,
                                                    message.author.name,
                                                    message.attachments,
                                                    message.author.raw_status,
                                                    current_status,
                                                    message.guild.name,
                                                    message.channel.name,
                                                    message.channel.category.name), bot.loop)
    
    asyncio.wait([generation_fut])

    generation = generation_fut.result()
    
    # Send the reply (note that reply is async so we need to use asyncio)
    asyncio.run_coroutine_threadsafe(message.reply(generation), bot.loop) # we don't care about the result

async def reload_all_extensions():
    """
        Reloads EVERY extension Vivia can find.
    """

    # Unload all extensions
    for extension in viviatools.loaded_extensions:
        try:
            await bot.unload_extension(extension)
            viviatools.log(f"Unloaded extension {extension}")
        except errors.ExtensionNotLoaded:
            viviatools.log(f"Extension {extension} was already unloaded.")
        except Exception as e:
            viviatools.log(f"Failed to unload extension {extension}", logging.ERROR)
            viviatools.log(f"{str(type(e))}: {e}", logging.ERROR)
            viviatools.log("This may cause issues during reloading.", logging.ERROR)
            
    # Reset list of extensions
    loaded = ["core"] # Vivia core is always loaded
    failed = []

    # Load ViviaBase
    for file in os.listdir(os.path.join("commands", "viviabase")):
        if file.endswith(".py"):
            try:
                await bot.load_extension(f"commands.viviabase.{file[:-3]}")
                loaded += [f"viviabase.{file[:-3]}"]
            except errors.ExtensionAlreadyLoaded:
                viviatools.log(f"Extension viviabase.{file[:-3]} was already loaded.")
                loaded += [f"viviabase.{file[:-3]}"]
            except Exception as e:
                viviatools.log(f"Failed to load base extension {file[:-3]}", logging.ERROR)
                viviatools.log(f"{str(type(e))}: {e}", logging.ERROR)
                viviatools.log("Functionality may be limited. Please report this on GitHub.", logging.ERROR)
                failed += [f"viviabase.{file[:-3]}"]
                continue
            viviatools.log(f"Loaded extension viviabase.{file[:-3]}")
    
    # Load ViviaBase beta
    if config["Advanced"]["betaextensions"]:
        viviatools.log("Loading beta extensions.")
        for file in os.listdir(os.path.join("commands", "viviabase-beta")):
            if file.endswith(".py"):
                try:
                    await bot.load_extension(f"commands.viviabase-beta.{file[:-3]}")
                    loaded += [f"viviabase-beta.{file[:-3]}"]
                except errors.ExtensionAlreadyLoaded:
                    viviatools.log(f"Extension viviabase-beta.{file[:-3]} was already loaded.")
                    loaded += [f"viviabase-beta.{file[:-3]}"]
                except Exception as e:
                    viviatools.log(f"Failed to load beta extension {file[:-3]}", logging.ERROR)
                    viviatools.log(f"{str(type(e))}: {e}", logging.ERROR)
                    viviatools.log("Functionality may be limited.", logging.ERROR)
                    failed += [f"viviabase-beta.{file[:-3]}"]
                    continue
                viviatools.log(f"Loaded extension viviabase-beta.{file[:-3]}")

    # Load custom extensions
    for file in os.listdir("commands"):
        if file.endswith(".py"):
            try:
                await bot.load_extension(f"commands.{file[:-3]}")
                loaded += [f"{file[:-3]}"]
            except errors.ExtensionAlreadyLoaded:
                viviatools.log(f"Extension {file[:-3]} was already loaded.")
                loaded += [f"{file[:-3]}"]
            except discord.ext.commands.NoEntryPointError:
                viviatools.log(f"Failed to load custom extension {file[:-3]}", logging.ERROR)
                viviatools.log("No entry point found. Does the extension contain a setup(bot) function?", logging.ERROR)
                viviatools.log("Functionality may be limited.", logging.ERROR)
                failed += [f"{file[:-3]}"]
                continue
            except Exception as e:
                viviatools.log(f"Failed to load custom extension {file[:-3]}", logging.ERROR)
                viviatools.log(f"{str(type(e))}: {e}", logging.ERROR)
                viviatools.log("Functionality may be limited. Ensure the extension contains no errors.", logging.ERROR)
                failed += [f"{file[:-3]}"]
                continue
            viviatools.log(f"Loaded extension {file[:-3]}")

    viviatools.loaded_extensions = loaded
    viviatools.failed_extensions = failed
    viviatools.log(f"Loaded {len(loaded)} extensions - failed loading {len(failed)}.")

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
    for guild in bot.guilds:
        # Regenerate server data path if it doesn't exist
        if not os.path.exists(os.path.join('data', 'servers', str(guild.id))):
            os.mkdir(os.path.join('data', 'servers', str(guild.id)))
        viviatools.log(f'Data path for {guild.name} ({guild.id}) was regenerated.', logging.DEBUG)

        # Regenerate configuration if guild config is missing
        try:
            with open(os.path.join('data', 'servers', str(guild.id), 'config.json'), 'x') as f, open(f'data/config.json.example', 'r') as g:
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

    await ctx.send('Fixed all missing config and quotes files. Check log for more info.')

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
        await ctx.send(personalityMessage("historyclear"), ephemeral=True)
        viviatools.log(f"{ctx.author.name} cleared their chat history", logging.DEBUG)
    else:
        await ctx.send(personalityMessage("nohistory"), ephemeral=True)
    
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
        await ctx.send(personalityMessage("error"), ephemeral=True)
        if serverConfig(ctx.guild.id)['verboseErrors']:
            await ctx.send(f"{str(type(e))}: {e}\n-# To disable these messages, run /config verboseErrors false")
        viviatools.log(f"Error while changing config for {ctx.guild.name} ({str(ctx.guild.id)}): {str(type(e))}: {str(e)}", severity=logging.ERROR)

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
            os.system("pip install -r requirements.txt")
            viviatools.log("Installed new dependencies.", logging.DEBUG)
        except Exception as e:
            viviatools.log(f"Failed to pull git repository: {str(type(e))}: {str(e)}", logging.ERROR)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.hybrid_command(
    name="extensions",
    description="Displays Vivia's available extensions."
)
async def extensions(ctx: commands.Context):
    """
    Displays Vivia's available extensions.
    """
    await ctx.send("Available extensions: \n- " + ("\n- ".join(viviatools.loaded_extensions)) if len(viviatools.loaded_extensions) > 0 else "No extensions loaded? Wait, what?!", ephemeral=True)
    await ctx.send("Extensions that failed to load: \n- " + ("\n- ".join(viviatools.failed_extensions)) if len(viviatools.failed_extensions) > 0 else "No extensions failed to load!", ephemeral=True)

# Run
while True:
    try:
        bot.activity = discord.CustomActivity(name="POWERING UP - Connecting to Discord gateway...")
        bot.run(dotenv.get_key("token.env", "token"), log_handler=None)
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
    except ClientConnectorError or GatewayNotFound or HTTPException or LoginFailure:
        viviatools.log("Vivia can't connect to Discord. Is your internet connection working, or is Discord's API down?", logging.ERROR)
        viviatools.log("Perhaps the token in token.env is invalid? There's a lot of reasons this could happen.", logging.ERROR)
        viviatools.log("Vivia will retry in 5 seconds.", logging.ERROR)
        time.sleep(5)
        os.execl(sys.executable, sys.executable, *sys.argv)
    except Exception as e:
        viviatools.log(f"Vivia has crashed... oh no...", logging.FATAL)
        viviatools.log("".join(traceback.format_exception(sys.exc_info())), severity=logging.FATAL)
        viviatools.log("Don't worry, she will automatically restart in 5 seconds.", logging.FATAL)
        viviatools.log("I would appreciate if you would report this on GitHub, please.", logging.FATAL)
        asyncio.run(viviatools.setCustomPresence("!! Vivia has crashed - rebooting! !!", "dnd", bot))
        time.sleep(5)
        os.execl(sys.executable, sys.executable, *sys.argv)
