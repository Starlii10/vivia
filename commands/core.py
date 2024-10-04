"""
    This is Vivia's core command extension.

    Vivia is licensed under the MIT License. For more information, see the LICENSE file.
    TL:DR: you can use Vivia's code as long as you keep the original license intact.
    Vivia is made open source in the hopes that you'll find her code useful.

    If you'd like to contribute, please check out the GitHub repository at https://github.com/starlii10/vivia.

    THIS FILE SHOULD NOT BE REMOVED! Most of the commands here are designed to always be available.
    Tampering with this file could result in an unusable Vivia.

    Have a great time using Vivia!
"""

import json
import logging
import os
import random
import shutil
import sys
import discord
from discord.ext import commands, tasks
from discord import app_commands

from extras import viviatools
from extras.viviatools import log, personalityMessage, config, serverConfig, bot_ref

async def setup(bot):
    bot.add_cog(viviacore_cmds(bot))
    bot.add_cog(viviacore_functions(bot))
    try:
        viviacore_functions.statusChanges.start()
    except RuntimeError:
        pass # already started

class viviacore_cmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot_ref.hybrid_command()
    async def sync(ctx, guild: int=0):
        """
        Syncs the command tree.

        ## Notes:
            - Only the bot owner can use this command.
            - If you want to sync the entire bot, use "v!sync 0" or "v!sync". Otherwise specify the ID of the guild you want to sync.
        """
        if await bot_ref.is_owner(ctx.author):
            if guild == 0:
                await bot_ref.tree.sync()
                await ctx.send('The command tree was synced, whatever that means.')
                viviatools.log("The command tree was synced, whatever that means.")
            else:
                await bot_ref.tree.sync(guild=discord.utils.get(bot_ref.guilds, id=guild))
                await ctx.send(f'The command tree was synced for {guild}, whatever that means.')
                viviatools.log(f"The command tree was synced for {guild}, whatever that means.")
        else:
            await ctx.send(personalityMessage("nopermissions"))

    @bot_ref.hybrid_command()
    async def fixconfig(ctx: commands.Context):
        """
        Regenerates server files for servers where they are missing.

        ## Notes:
            - Only the bot owner can use this command.
        """
        if await bot_ref.is_owner(ctx.author):
            viviatools.log(f"Regenerating missing data files for all servers...", logging.DEBUG)
            for guild in bot_ref.guilds:
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

                # Regenerate warns if guild warns is missing
                try:
                    with open(f'data/servers/{guild.id}/warns.json', 'x') as f:
                        json.dump({'warns': []}, f)
                    viviatools.log(f'Warn file for {guild.name} ({guild.id}) was regenerated.', logging.DEBUG)
                except FileExistsError:
                    pass # Most likely there was nothing wrong with it

            await ctx.send('Fixed all missing config and quotes files. Check log for more info.')
        else:
            await ctx.send(personalityMessage("nopermissions"))

    @bot_ref.hybrid_command(
        name="statuschange",
        description="Manually randomizes the current status of the bot."
    )
    async def statuschange(ctx: commands.Context):
        """
        Manually randomizes the current status of the bot.

        ## Notes:
            - Only the bot owner can use this command.
        """
        if await bot_ref.is_owner(ctx.author):
            await viviacore_functions.statusChanges()
            await ctx.send('Status randomized!')
        else:
            await ctx.send(personalityMessage("nopermissions"), ephemeral=True)

    @bot_ref.hybrid_command(
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
            viviatools.log(f"{ctx.author.name} cleared their chat history", logging.DEBUG)
        else:
            await ctx.send(personalityMessage("nohistory"), ephemeral=True)
        
    @bot_ref.hybrid_command(
        name="setting",
        description="Manages Vivia's configuration."
    )
    @app_commands.choices(option=[
        app_commands.Choice(name="AI Enabled",value="aiEnabled"),
        app_commands.Choice(name="Verbose Errors",value="verboseErrors"),
    ])
    async def setting(ctx: commands.Context, option: str, value: bool):
        """
        Manages Vivia's configuration for a specific server.

        ## Notes:
            - Only users with Vivia admin permissions can use this command.
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
                    await ctx.send(f"{str(type(e))}: {e}\n-# To disable these messages, run /config verboseErrors false")
                viviatools.log(f"Error while changing config for {ctx.guild.name} ({str(ctx.guild.id)}): {str(type(e))}: {str(e)}", severity=logging.ERROR)
        else:
            await ctx.send(personalityMessage("nopermissions"), ephemeral=True)

    @bot_ref.hybrid_command(
        name="reboot",
        description="Performs a full reboot of Vivia."
    )
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
        if await bot_ref.is_owner(ctx.author):
            await ctx.send("Rebooting...")
            viviatools.log(f"Rebooting on request of {ctx.author.name} ({str(ctx.author.id)})...")
            await bot_ref.close()
            if pull_git:
                try:
                    os.system("git pull")
                    viviatools.log("Pulled git repository.", logging.DEBUG)
                    os.system("pip install -r requirements.txt")
                    viviatools.log("Installed new dependencies.", logging.DEBUG)
                except Exception as e:
                    viviatools.log(f"Failed to pull git repository: {str(type(e))}: {str(e)}", logging.ERROR)
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            await ctx.send(personalityMessage("nopermissions"), ephemeral=True)

    @bot_ref.hybrid_command(
        name="extensions",
        description="Displays Vivia's available extensions."
    )
    async def extensions(ctx: commands.Context):
        """
        Displays Vivia's available extensions.
        """
        await ctx.send("Available extensions: \n- " + ("\n- ".join(viviatools.loaded_extensions)) if len(viviatools.loaded_extensions) > 0 else "No extensions loaded? Wait, what?!", ephemeral=True)
        await ctx.send("Extensions that failed to load: \n- " + ("\n- ".join(viviatools.failed_extensions)) if len(viviatools.failed_extensions) > 0 else "No extensions failed to load!", ephemeral=True)

class viviacore_functions(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @tasks.loop(hours=1)
    async def statusChanges():
        """
        Changes the bot's status every hour.
        """
        with open("data/statuses.json", "r") as f:
            statuses = json.load(f)
        status = random.choice(statuses["statuses"])
        await viviatools.setCustomPresence(status, bot_ref)
        current_status = status
        viviatools.log(f"Status changed to {status}", logging.DEBUG)