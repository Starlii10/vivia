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
from discord.ext import commands
from discord import app_commands
from extras import viviatools
from extras.viviatools import personalityMessage

async def setup(bot: commands.Bot): # for extension loading
    bot.add_command(warn) # type: ignore
    bot.add_command(unwarn) # type: ignore
    bot.add_command(kick) # type: ignore
    bot.add_command(ban) # type: ignore
    bot.add_command(unban) # type: ignore


@commands.hybrid_command(
    name = "warn"
)
@app_commands.describe(
    user = "The user to warn.",
    reason = "The reason for the warning."
)
async def warn(ctx: commands.Context, user: discord.Member, reason: str = "No reason provided."):
    """
    Warns the user.

    Args:
        - user (discord.User): The user to warn.
        - reason (str): The reason for the warning.
    """

    if user._permissions.administrator:
        await ctx.send(personalityMessage("adminmoderation").replace("{user}", user.name).replace("{action}", "warning"), ephemeral=True)
        return
    
    if user.id == ctx.author.id:
        await ctx.send(personalityMessage("cantwarnself"), ephemeral=True)
        return
    
    if user.top_role >= ctx.author.top_role:
        await ctx.send(personalityMessage("cantwarnhigher").replace("{user}", user.name), ephemeral=True)
        return
    
    if user == ctx.me:
        await ctx.send(personalityMessage("cantwarnbot"), ephemeral=True)

    # messages
    await ctx.send(personalityMessage("warn").replace("{user}", user.mention), ephemeral=True)
    await user.send(personalityMessage("warned").replace("{server}", ctx.guild.name).replace("{user}", ctx.author.mention)
                    + "\n" + personalityMessage("reason").replace("{reason}", reason).replace("{action}", "warning").replace("{reason}", reason)
                    + "\n" + personalityMessage("followrules").replace("{server}", ctx.guild.name))
    
    # add user to warned users
    # TODO: users can be warned multiple times
    viviatools.warns(ctx.guild.id)[user.id] = [reason, ctx.message.created_at, ctx.author.id]
    viviatools.log(f"{ctx.user} warned {user} in {ctx.guild} ({ctx.guild.id})", logging.DEBUG)


@commands.hybrid_command(
    name = "unwarn"
)
@app_commands.describe(
    user = "The user to unwarn.",
    reason = "The reason for the unwarning."
)
async def unwarn(ctx: commands.Context, user: discord.Member, reason: str = "No reason provided."):
    """
    Unwarns the user.

    Args:
        - user (discord.User): The user to unwarn.
        - reason (str): The reason for the unwarning.
    """

    # messages
    await ctx.send(personalityMessage("unwarn").replace("{user}", user.mention), ephemeral=True)
    await user.send(personalityMessage("unwarned").replace("{user}", ctx.author.mention)
                    + "\n" + personalityMessage("reason").replace("{reason}", reason).replace("{action}", "unwarning").replace("{reason}", reason)
                    + "\n" + personalityMessage("followrules").replace("{server}", ctx.guild.name))

    # remove user from warned users
    # TODO: users can be warned multiple times
    del viviatools.warns(ctx.guild.id)[user.id]
    viviatools.log(f"{ctx.author} unwarned {user} in {ctx.guild} ({ctx.guild.id})", logging.DEBUG)

@commands.hybrid_command(
    name = "kick"
)
@app_commands.describe(
    user = "The user to kick.",
    reason = "The reason for the kick."
)
async def kick(ctx: commands.Context, user: discord.Member, reason: str = "No reason provided."):
    """
    Kicks the user.

    Args:
        - user (discord.User): The user to kick.
        - reason (str): The reason for the kick.
    """

    await ctx.send(personalityMessage("moderationactions").replace("{user}", user.mention).replace("{action}", "kicked"), ephemeral=True)
    await user.send(personalityMessage("kicked").replace("{user}", ctx.author.mention).replace("{server}", ctx.guild.name)
                    + "\n" + personalityMessage("reason").replace("{reason}", "").replace("{action}", "kicking").replace("{reason}", reason)
                    + "\n" + personalityMessage("followrules").replace("{server}", ctx.guild.name))
    await user.kick(reason=f"Kicked by {ctx.author}: {reason}")
    viviatools.log(f"{ctx.author} kicked {user} from {ctx.guild} ({ctx.guild.id})", logging.DEBUG)

@commands.hybrid_command(
    name = "ban"
)
@app_commands.describe(
    user = "The user to ban."
)
async def ban(ctx: commands.Context, user: discord.Member, reason: str = "No reason provided."):
    """
    Bans the user.

    Args:
        - user (discord.User): The user to ban.
        - reason (str): The reason for the ban.
    """

    await ctx.send(personalityMessage("moderationactions").replace("{user}", user.mention).replace("{action}", "banned"), ephemeral=True)
    await user.send(personalityMessage("banned").replace("{user}", ctx.author.mention).replace("{server}", ctx.guild.name)
                    + "\n" + personalityMessage("reason").replace("{reason}", "").replace("{action}", "banning").replace("{reason}", reason)
                    + "\n" + personalityMessage("followrules").replace("{server}", "other servers"))
    await user.ban(reason=f"Banned by {ctx.author}: {reason}")
    viviatools.log(f"{ctx.author} banned {user} from {ctx.guild} ({ctx.guild.id})", logging.DEBUG)

@commands.hybrid_command(
    name = "unban"
)
@app_commands.describe(
    user = "The user to unban."
)
async def unban(ctx: commands.Context, user: discord.User, reason: str = "No reason provided."):
    """
    Unbans the user.

    Args:
        - user (discord.User): The user to unban.
        - reason (str): The reason for the unban.
    """

    await ctx.send(personalityMessage("unban").replace("{user}", user.mention), ephemeral=True)
    await user.send(personalityMessage("unbanned").replace("{user}", ctx.author.mention).replace("{server}", ctx.guild.name)
                    + "\n" + personalityMessage("reason").replace("{reason}", "").replace("{action}", "unbanning").replace("{reason}", "")
                    + "\n" + personalityMessage("followrules").replace("{server}", ctx.guild.name))
    await ctx.guild.unban(user)
    viviatools.log(f"{ctx.author} unbanned {user} from {ctx.guild} ({ctx.guild.id})", logging.DEBUG)