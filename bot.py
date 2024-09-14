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
__VERSION__ = "Vivia 20240910"

import asyncio
import shutil
import sys
import json
import threading
import traceback
import dotenv
import random
import os
from os import system
import logging

# Discord
import discord, discord.ext
from discord import app_commands
from discord.ext import tasks, commands, commands
from discord.ext.commands import errors

# Vivia's extra scripts
from commands.viviabase.viviabase_addquote import addquote
import extras.viviatools as viviatools
from extras.viviatools import config, serverConfig, handler, personalityMessage
import extras.viviallama as Llama

# Variables
current_status = "Vivia is powering up..."

# Terminal title. VSCode will scream at you that one of these is unreachable, ignore it
if sys.platform == 'win32':
    # Windows title
    system(f"title Running {__VERSION__} - {config['General']['StatusMessage']}")
else:
    # Linux title (if this doesn't work on your distro please open an issue because I suck at Linux)
    system(f"echo -ne '\033]0;Running {__VERSION__} - {config['General']['StatusMessage']}\007'")

# Get ready to run the bot
intents = discord.Intents.default()
intents.message_content = True # will need to verify at 100 servers
bot = commands.Bot(command_prefix=config['General']['Prefix'], intents=intents)
bot.remove_command("help") # because we hate the default help command
tree = bot.tree

# Events
@bot.event
async def on_ready():
    """
    Function called when Vivia starts up.
    """
    
    viviatools.log("Vivia is powering up...")
    
    # Statuses
    with open("data/statuses.json", "r") as f:
        statuses = json.load(f)
    await bot.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name=random.choice(statuses["statuses"])))
    statusChanges.start()

    # Load extensions
    viviatools.log("Loading extensions!")

    # viviabase
    for file in os.listdir("commands/viviabase"):
        if file.endswith(".py"):
            try:
                await bot.load_extension(f"commands.viviabase.{file[:-3]}")
            except Exception as e:
                viviatools.log(f"Failed to load base extension {file[:-3]}", logging.ERROR)
                viviatools.log(f"{type(e)}: {e}\n{traceback.format_exc()}", logging.ERROR)
                viviatools.log("Functionality may be limited. Please report this on GitHub.", logging.ERROR)
                continue
            viviatools.log(f"Loaded base extension {file[:-3]}")

    # Custom extensions
    for file in os.listdir("commands"):
        if file.endswith(".py"):
            try:
                await bot.load_extension(f"commands.{file[:-3]}")
            except Exception as e:
                viviatools.log(f"Failed to load custom extension {file[:-3]}")
                viviatools.log(f"{type(e)}: {e}\n{traceback.format_exc()}")
                continue
            viviatools.log(f"Loaded extension {file[:-3]}")

    viviatools.log("Vivia is all ready!")

@tasks.loop(hours=1)
async def statusChanges():
    """
    Changes the bot's status every hour.
    """
    with open("data/statuses.json", "r") as f:
        statuses = json.load(f)
    status = random.choice(statuses["statuses"])
    await bot.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name=status))
    current_status = status
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
    if config["Advanced"]["Debug"]:
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
    if config["Advanced"]["Debug"]:
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
    if message.guild == None:
        return

    # Process commands
    try:
        await bot.process_commands(message)
    except app_commands.CommandNotFound or errors.CommandNotFound:
        viviatools.log(f"Command not found: {message.content} (requested by {message.author}). Ignoring.", logging.WARNING)
        await message.reply("That command doesn't seem to exist... did you spell it correctly?")
        pass

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

    generation = generation_fut.result()
    
    # Send the reply (note that reply is async so we need to use asyncio)
    asyncio.run_coroutine_threadsafe(message.reply(generation), bot.loop) # we don't care about the result

# Core commands
# These commands are always available

@bot.hybrid_command()
async def sync(ctx, guild: int=0):
    """
    Syncs the command tree.

    ## Notes:
        - Only the bot owner can use this command.
        - If you want to sync the entire bot, use "v!sync 0" or "v!sync". Otherwise specify the ID of the guild you want to sync.
    """
    if await bot.is_owner(ctx.author):
        if guild is 0:
            await bot.tree.sync()
            await ctx.send('The command tree was synced, whatever that means.')
            viviatools.log("The command tree was synced, whatever that means.")
        else:
            await bot.tree.sync(guild=discord.utils.get(bot.guilds, id=guild))
            await ctx.send(f'The command tree was synced for {guild}, whatever that means.')
            viviatools.log(f"The command tree was synced for {guild}, whatever that means.")
    else:
        await ctx.send('That\'s for the bot owner, not random users...')

@bot.hybrid_command()
async def fixconfig(ctx: commands.Context):
    """
    Regenerates configuration and custom quotes files for servers where they are missing.

    ## Notes:
        - Only the bot owner can use this command.
    """
    if await bot.is_owner(ctx.author):
        viviatools.log(f"Regenerating missing data files for all servers...", logging.DEBUG)
        for guild in bot.guilds:
            # Regenerate server data path if it doesn't exist
            if not os.path.exists(f'data/servers/{guild.id}'):
                os.mkdir(f'data/servers/{guild.id}')
            viviatools.log(f'Data path for {guild.name} ({guild.id}) was regenerated.', logging.DEBUG)

            # Regenerate configuration if guild config is missing
            try:
                with open(f'data/servers/{guild.id}/config.json', 'x') as f, open(f'data/config.json.example', 'r') as g:
                    json.dump(obj=json.load(g), fp=f)
                viviatools.log(f'Config file for {guild.name} ({guild.id}) was regenerated.', logging.DEBUG)
            except FileExistsError:
                pass # Most likely there was nothing wrong with it

            # Regenerate quotes if guild quotes is missing
            try:
                with open(f'data/servers/{guild.id}/quotes.json', 'x') as f:
                    json.dump({'quotes': []}, f)
                viviatools.log(f'Custom quote file for {guild.name} ({guild.id}) was regenerated.', logging.DEBUG)
            except FileExistsError:
                pass # Most likely there was nothing wrong with it

        await ctx.send('Fixed all missing config and quotes files. Check log for more info.')
    else:
        await ctx.send('That\'s for the bot owner, not random users...')

@bot.hybrid_command(
    name="statuschange",
    description="Manually randomizes the current status of the bot."
)
async def statuschange(ctx: commands.Context):
    """
    Manually randomizes the current status of the bot.

    ## Notes:
        - Only the bot owner can use this command.
    """
    if await bot.is_owner(ctx.author):
        await statusChanges()
        await ctx.send('Status randomized!')
    else:
        await ctx.send('That\'s for the bot owner, not random users...')

@bot.hybrid_command(
    name="clearhistory",
    description="Clears your recent chat history with me."
)
async def clearhistory(ctx: commands.Context):
    """
    Clears a user's recent chat history with Vivia.
    """
    if os.path.exists(f"data/tempchats/{str(ctx.author.name)}"):
        shutil.rmtree(f"data/tempchats/{str(ctx.author.name)}")
        await ctx.send(personalityMessage("historyclear"), ephemeral=True)
        viviatools.log(f"{ctx.user} cleared their chat history", logging.DEBUG)
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
async def setting(ctx: commands.Context, option: str, value: bool):
    """
    Manages Vivia's configuration.

    ## Notes:
        - Only users with bot permissions can use this command.
    """
    if viviatools.has_bot_permissions(ctx.author, ctx.guild):
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
                await ctx.send(f"{type(e)}: {e}\n-# To disable these messages, run /config verboseErrors false")
            viviatools.log(f"Error while changing config for {ctx.guild.name} ({str(ctx.guild.id)}): {type(e)}: {str(e)}", severity=logging.ERROR)
    else:
        await ctx.send("That's for authorized users, not you...", ephemeral=True)

@bot.hybrid_command(
    name="reboot",
    description="Performs a full reboot of Vivia."
)
async def reboot(ctx: commands.Context):
    """
    Performs a full reboot of Vivia.

    ## Notes:
        - Only the bot owner can use this command.
    """
    if await bot.is_owner(ctx.author):
        await ctx.send("Rebooting...")
        viviatools.log(f"Rebooting on request of {ctx.author.name} ({str(ctx.author.id)})...")
        await bot.close()
        os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        await ctx.send("That's for the bot owner, not random users...", ephemeral=True)

# Context menu commands
@app_commands.context_menu(name="Add Custom Quote")
async def add_custom_quote(interaction: discord.Interaction, message: discord.Message):
    viviatools.add_custom_quote(f"\"{message.content}\" - {message.author.display_name}, {message.created_at.strftime('%Y-%m-%d')}", interaction.guild.id)
    await interaction.response.send_message(f"\"{message.content}\" - {message.author.display_name}, {message.created_at.strftime('%Y-%m-%d')} was added to the list.", ephemeral=True)

# Add context menu commands
tree.add_command(add_custom_quote)

# Run
while True:
    bot.run(dotenv.get_key("token.env", "token"), log_handler=handler)
