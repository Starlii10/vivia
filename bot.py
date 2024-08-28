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
__VERSION__ = "Vivia 20240826"

import asyncio
import shutil
import sys
import json
import dotenv
import random
import os
from os import system
import logging

# Discord
import discord
from discord import app_commands
from discord.ext import tasks, commands

# Vivia's extra scripts
from commands.addquote import addquote
import extras.viviatools as viviaTools
from extras.viviatools import config, serverConfig, handler
import extras.viviallama as Llama

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

# Events
@bot.event
async def on_ready():
    """
    Function called when Vivia starts up.
    """
    
    await viviaTools.log("Vivia is powering up...")
    
    # Statuses
    with open("data/statuses.json", "r") as f:
        statuses = json.load(f)
    await bot.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name=random.choice(statuses["statuses"])))
    statusChanges.start()

    # Commands
    for file in os.listdir("commands"):
        if file.endswith(".py"):
            await viviaTools.log(f"Loading extension {file[:-3]}")
            await bot.load_extension(f"commands.{file[:-3]}")

    await viviaTools.log("Vivia is all ready!")

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

    await viviaTools.log(f"Bot joined {guild.name} ({guild.id})")
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

# Core commands
# These commands are always available

@bot.command()
async def sync(ctx, guild: int=0):
    """
    Syncs the command tree.

    ## Notes:
        - Only the bot owner can use this command. If you run Vivia locally, make sure to add your Discord user ID in config.ini.
        - This command does not appear in the command list. Use "v!sync" to run it.
        - If you want to sync the entire bot, use "v!sync 0" or "v!sync". Otherwise specify the ID of the guild you want to sync.
    """
    if ctx.author.id == int(config["General"]["owner"]):
        if guild is 0:
            await bot.tree.sync()
            await ctx.send('The command tree was synced, whatever that means.')
            await viviaTools.log("The command tree was synced, whatever that means.")
        else:
            await bot.tree.sync(guild=discord.utils.get(bot.guilds, id=guild))
            await ctx.send(f'The command tree was synced for {guild}, whatever that means.')
            await viviaTools.log(f"The command tree was synced for {guild}, whatever that means.")
    else:
        await ctx.send('That\'s for the bot owner, not random users...')

@bot.command()
async def fixconfig(ctx: commands.Context):
    """
    Regenerates configuration and custom quotes files for servers where they are missing.

    ## Notes:
        - Only the bot owner can use this command. If you run Vivia locally, make sure to add your Discord user ID in config.ini.
        - This command does not appear in the command list. Use "v!fixconfig" to run it.
    """
    if ctx.author.id == int(config["General"]["owner"]):
        for guild in bot.guilds:
            # Regenerate server data path if it doesn't exist
            if not os.path.exists(f'data/servers/{guild.id}'):
                os.mkdir(f'data/servers/{guild.id}')
            await viviaTools.log(f'Data path for {guild.name} ({guild.id}) was regenerated.')

            # Regenerate configuration if guild config is missing
            try:
                with open(f'data/servers/{guild.id}/config.json', 'x') as f, open(f'data/config.json.example', 'r') as g:
                    json.dump(obj=json.load(g), fp=f)
                await viviaTools.log(f'Config file for {guild.name} ({guild.id}) was regenerated.')
            except FileExistsError:
                pass # Most likely there was nothing wrong with it

            # Regenerate quotes if guild quotes is missing
            try:
                with open(f'data/servers/{guild.id}/quotes.json', 'x') as f:
                    json.dump({'quotes': []}, f)
                await viviaTools.log(f'Custom quote file for {guild.name} ({guild.id}) was regenerated.')
            except FileExistsError:
                pass # Most likely there was nothing wrong with it

        await ctx.send('Fixed all missing config and quotes files. Check log channel for more info.')
    else:
        await ctx.send('That\'s for the bot owner, not random users...')

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
        await viviaTools.log(f"{interaction.user} cleared their chat history")
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
    if viviaTools.has_bot_permissions(interaction.user, interaction.guild):
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
            await viviaTools.log(f"Error while changing config for {interaction.guild.name} ({str(interaction.guild.id)}): {type(e)}: {str(e)}", severity=logging.ERROR)
    else:
        await interaction.response.send_message("That's for authorized users, not you...", ephemeral=True)

# Context menu commands
@app_commands.context_menu(name="Add Custom Quote")
async def add_custom_quote(interaction: discord.Interaction, message: discord.Message):
    viviaTools.add_custom_quote(f"\"{message.content}\" - {message.author.display_name}, {message.created_at.strftime('%Y-%m-%d')}", interaction.guild.id)
    await interaction.response.send_message(f"\"{message.content}\" - {message.author.display_name}, {message.created_at.strftime('%Y-%m-%d')} was added to the list.", ephemeral=True)

# Add context menu commands
tree.add_command(add_custom_quote)

# Run
while True:
    bot.run(dotenv.get_key("token.env", "token"), log_handler=handler)
