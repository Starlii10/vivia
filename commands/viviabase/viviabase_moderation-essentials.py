"""
    This is the moderation essentials command package used in Vivia.

    Vivia is licensed under the MIT License. For more information, see the LICENSE file.
    TL:DR: you can use Vivia's code as long as you keep the original license intact.
    Vivia is made open source in the hopes that you'll find her code useful.

    If you'd like to contribute, please check out the GitHub repository at https://github.com/starlii10/vivia.

    Have a great time using Vivia!
"""

import logging
import discord
import json
from discord.ext import commands
from discord import app_commands
from extras import viviatools
from extras.viviatools import personalityMessage

async def setup(bot: commands.Bot): # for extension loading
    bot.add_command() # type: ignore

@app_commands.hybrid_command(
    name = "warn"
)
@app_commands.describe(
    user = "The user to warn."
)
async def warn(ctx: commands.Context, user: discord.Member, reason: str = ""):
    """
    Warns the user.

    Args:
        - user (discord.User): The user to warn.
        - reason (str): The reason for the warning.
    """

    # messages
    await ctx.send(personalityMessage("warn").replace("{user}", user.mention), ephemeral=True)
    await user.send(personalityMessage("warned").replace("{server}", ctx.guild.name).replace("{user}", ctx.author.mention)
                    + "\n" + personalityMessage("reason").replace("{reason}", reason).replace("{action}", "warning").replace("{reason}", reason)
                    + "\n" + personalityMessage("followrules").replace("{server}", ctx.guild.name))
    
    # add user to warned users
    viviatools.warns(ctx.guild.id)[user.id] = [reason, ctx.message.created_at, ctx.author.id, viviatools.warns(ctx.guild.id)[user.id][3] + 1]
    viviatools.log(f"{ctx.user} warned {user} in {ctx.guild} ({ctx.guild.id})", logging.DEBUG)


@app_commands.hybrid_command(
    name = "unwarn"
)
@app_commands.describe(
    user = "The user to unwarn."
)
async def unwarn(ctx: commands.Context, user: discord.Member, reason: str = ""):
    """
    Unwarns the user.

    Args:
        - user (discord.User): The user to unwarn.
    """

    await ctx.send(personalityMessage("unwarn").replace("{user}", user.mention), ephemeral=True)
    await user.send(personalityMessage("unwarned").replace("{user}", ctx.author.mention))

    # remove user from warned users
    viviatools.warns(ctx.guild.id)[user.id] = [reason, ctx.message.created_at, ctx.author.id, viviatools.warns(ctx.guild.id)[user.id][3] - 1]

    if viviatools.warns(ctx.guild.id)[user.id][3] == 0:
        # no more warns for this user, pop
        del viviatools.warns(ctx.guild.id)[user.id]
    viviatools.log(f"{ctx.user} unwarned {user} in {ctx.guild} ({ctx.guild.id})", logging.DEBUG)

@app_commands.hybrid_command(
    name = "kick"
)
@app_commands.describe(
    user = "The user to kick."
)
async def kick(ctx: commands.Context, user: discord.Member):
    """
    Kicks the user.

    Args:
        - user (discord.User): The user to kick.
    """

    await ctx.send(personalityMessage("kick").replace("{user}", user.mention), ephemeral=True)
    await user.send(personalityMessage("kicked").replace("{user}", ctx.author.mention))
    await user.kick()
    viviatools.log(f"{ctx.user} kicked {user} from {ctx.guild} ({ctx.guild.id})", logging.DEBUG)

@app_commands.hybrid_command(
    name = "ban"
)
@app_commands.describe(
    user = "The user to ban."
)
async def ban(ctx: commands.Context, user: discord.Member):
    """
    Bans the user.

    Args:
        - user (discord.User): The user to ban.
    """

    await ctx.send(personalityMessage("ban").replace("{user}", user.mention), ephemeral=True)
    await user.send(personalityMessage("banned").replace("{user}", ctx.author.mention))
    await user.ban()
    viviatools.log(f"{ctx.user} banned {user} from {ctx.guild} ({ctx.guild.id})", logging.DEBUG)

@app_commands.hybrid_command(
    name = "unban"
)
@app_commands.describe(
    user = "The user to unban."
)
async def unban(ctx: commands.Context, user: discord.User):
    """
    Unbans the user.

    Args:
        - user (discord.User): The user to unban.
    """

    await ctx.send(personalityMessage("unban").replace("{user}", user.mention), ephemeral=True)
    await user.send(personalityMessage("unbanned").replace("{user}", ctx.author.mention))
    await ctx.guild.unban(user)
    viviatools.log(f"{ctx.user} unbanned {user} from {ctx.guild} ({ctx.guild.id})", logging.DEBUG)