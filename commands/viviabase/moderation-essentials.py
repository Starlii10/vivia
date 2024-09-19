"""
    This is the moderation essentials command package used in Vivia.

    Vivia is licensed under the MIT License. For more information, see the LICENSE file.
    TL:DR: you can use Vivia's code as long as you keep the original license intact.
    Vivia is made open source in the hopes that you'll find her code useful.

    If you'd like to contribute, please check out the GitHub repository at https://github.com/starlii10/vivia.

    Have a great time using Vivia!
"""

import json
import logging
import discord
from discord.ext import commands
from discord import HTTPException, app_commands
from extras import viviatools
from extras.viviatools import personalityMessage

async def setup(bot: commands.Bot):
    bot.add_command(warn)
    bot.add_command(unwarn)
    bot.add_command(kick)
    bot.add_command(ban)
    bot.add_command(unban)

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

    if not ctx.author.guild_permissions.moderate_members:
        await ctx.send(personalityMessage("nopermissions"), ephemeral=True)
        return

    if user == None:
        await ctx.send(personalityMessage("moderation/targetnone"), ephemeral=True)
        return

    if user == ctx.me:
        await ctx.send(personalityMessage("moderation/moderatevivia").replace("{action}", "warn"), ephemeral=True)
        return
    
    if user == ctx.author:
        await ctx.send(personalityMessage("moderation/moderateself").replace("{action}", "warn"), ephemeral=True)
        return

    if user.guild_permissions.administrator:
        await ctx.send(personalityMessage("moderation/moderateadmin").replace("{user}", user.name).replace("{action}", "warn"), ephemeral=True)
        return
    
    if user.top_role >= ctx.author.top_role and not ctx.author.guild_permissions.administrator:
        await ctx.send(personalityMessage("moderation/moderatehigher").replace("{user}", user.name).replace("{action}", "warn"), ephemeral=True)
        return

    # add user to warned users
    # TODO: users can be warned multiple times
    viviatools.log(json.dumps([reason, ctx.message.created_at.strftime('%Y-%m-%d %H:%M:%S'), ctx.author.id]))
    with open(f"data/servers/{ctx.guild.id}/warns.json", "w") as f:
        json.dump({user.id: [reason, ctx.message.created_at.strftime('%Y-%m-%d %H:%M:%S'), ctx.author.id]}, f)
    
    viviatools.log(f"{ctx.author.name} warned {user} in {ctx.guild} ({ctx.guild.id})", logging.DEBUG)

    # messages
    await ctx.send(personalityMessage("moderation/warn").replace("{user}", user.mention), ephemeral=True)

    try:
        await user.send(f"# You've been warned in {ctx.guild} ({ctx.guild.id})\n\n" + personalityMessage("moderation/warned").replace("{server}", ctx.guild.name).replace("{user}", ctx.author.mention)
                        + "\n" + personalityMessage("moderation/reason").replace("{reason}", reason).replace("{action}", "warning").replace("{reason}", reason)
                        + "\n\n" + personalityMessage("moderation/followrules").replace("{server}", ctx.guild.name)
                        + "\n" + "-# This automated message was sent because a moderator warned you using Vivia.")
    except HTTPException:
        await ctx.send("I couldn't DM the user.", ephemeral=True)

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

    if not ctx.author.guild_permissions.moderate_members:
        await ctx.send(personalityMessage("nopermissions"), ephemeral=True)
        return

    if user == None:
        await ctx.send(personalityMessage("moderation/targetnone"), ephemeral=True)
        return
    
    if user == ctx.me:
        await ctx.send(personalityMessage("moderation/moderatevivia").replace("{action}", "unwarn"), ephemeral=True)
        return
    
    if user == ctx.author:
        await ctx.send(personalityMessage("moderation/moderateself").replace("{action}", "unwarn"), ephemeral=True)
        return
    
    if user.guild_permissions.administrator:
        await ctx.send(personalityMessage("moderation/moderateadmin").replace("{user}", user.name).replace("{action}", "unwarn"), ephemeral=True)
        return
    
    if user.top_role >= ctx.author.top_role and not ctx.author.guild_permissions.administrator:
        await ctx.send(personalityMessage("moderation/moderatehigher").replace("{user}", user.name).replace("{action}", "unwarn"), ephemeral=True)
        return

    # remove user from warned users
    # TODO: users can be warned multiple times
    with open(f"data/servers/{ctx.guild.id}/warns.json", "r") as f:
        warns = json.load(f)
        if warns[user.id]:
            del warns[user.id]
        else:
            await ctx.send(personalityMessage("moderation/notwarned").replace("{user}", user.mention), ephemeral=True)
            return
        with open(f"data/servers/{ctx.guild.id}/warns.json", "w") as f:
            json.dump(warns, f)

    viviatools.log(f"{ctx.author.name} unwarned {user} in {ctx.guild} ({ctx.guild.id})", logging.DEBUG)

    # messages
    await ctx.send(personalityMessage("moderation/unwarn").replace("{user}", user.mention), ephemeral=True)
    try:
        await user.send(f"# You've been unwarned in {ctx.guild} ({ctx.guild.id})\n\n" + personalityMessage("moderation/unwarned").replace("{user}", ctx.author.mention)
                        + "\n" + personalityMessage("moderation/reason").replace("{reason}", reason).replace("{action}", "unwarning").replace("{reason}", reason)
                        + "\n\n" + personalityMessage("moderation/followrules").replace("{server}", ctx.guild.name)
                        + "\n" + "-# This automated message was sent because a moderator unwarned you using Vivia.")
    except HTTPException:
        await ctx.send("I couldn't DM the user.", ephemeral=True)

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
    
    if not ctx.author.guild_permissions.kick_members:
        await ctx.send(personalityMessage("nopermissions"), ephemeral=True)
        return

    if user == None:
        await ctx.send(personalityMessage("moderation/targetnone"), ephemeral=True)
        return
    
    if user == ctx.me:
        await ctx.send(personalityMessage("moderation/moderatevivia").replace("{action}", "kick"), ephemeral=True)
        return
    
    if user == ctx.author:
        await ctx.send(personalityMessage("moderation/moderateself").replace("{action}", "kick"), ephemeral=True)
        return
    
    if user.guild_permissions.administrator:
        await ctx.send(personalityMessage("moderation/moderateadmin").replace("{user}", user.name).replace("{action}", "kick"), ephemeral=True)
        return
    
    if user.top_role >= ctx.author.top_role and not ctx.author.guild_permissions.administrator:
        await ctx.send(personalityMessage("moderation/moderatehigher").replace("{user}", user.name).replace("{action}", "kick"), ephemeral=True)
        return

    await user.kick(reason=f"Kicked by {ctx.author}: {reason}")
    await ctx.send(personalityMessage("moderation/moderationactions").replace("{user}", user.mention).replace("{action}", "kicked"), ephemeral=True)
    try:
        await user.send(f"# You've been kicked from {ctx.guild} ({ctx.guild.id})\n\n" + personalityMessage("moderation/kicked").replace("{user}", ctx.author.mention).replace("{server}", ctx.guild.name)
                        + "\n" + personalityMessage("moderation/reason").replace("{reason}", "").replace("{action}", "kicking").replace("{reason}", reason)
                        + "\n\n" + personalityMessage("moderation/followrules").replace("{server}", ctx.guild.name)
                        + "\n" + "-# This automated message was sent because a moderator kicked you using Vivia.")
    except HTTPException:
        await ctx.send("I couldn't DM the user.", ephemeral=True)
    viviatools.log(f"{ctx.author.name} kicked {user} from {ctx.guild} ({ctx.guild.id})", logging.DEBUG)

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

    if not ctx.author.guild_permissions.ban_members:
        await ctx.send(personalityMessage("nopermissions"), ephemeral=True)
        return
    
    if user == None:
        await ctx.send(personalityMessage("moderation/targetnone"), ephemeral=True)
        return
    
    if user == ctx.me:
        await ctx.send(personalityMessage("moderation/moderatevivia").replace("{action}", "ban"), ephemeral=True)
        return
    
    if user == ctx.author:
        await ctx.send(personalityMessage("moderation/moderateself").replace("{action}", "ban"), ephemeral=True)
        return
    
    if user.guild_permissions.administrator:
        await ctx.send(personalityMessage("moderation/moderateadmin").replace("{user}", user.name).replace("{action}", "ban"), ephemeral=True)
        return
    
    if user.top_role >= ctx.author.top_role and not ctx.author.guild_permissions.administrator:
        await ctx.send(personalityMessage("moderation/moderatehigher").replace("{user}", user.name).replace("{action}", "ban"), ephemeral=True)
        return

    await user.ban(reason=f"Banned by {ctx.author}: {reason}")
    await ctx.send(personalityMessage("moderation/moderationactions").replace("{user}", user.mention).replace("{action}", "banned"), ephemeral=True)
    try:
        await user.send(f"# You've been banned from {ctx.guild} ({ctx.guild.id})\n\n" + personalityMessage("moderation/banned").replace("{user}", ctx.author.mention).replace("{server}", ctx.guild.name)
                        + "\n" + personalityMessage("moderation/reason").replace("{reason}", "").replace("{action}", "banning").replace("{reason}", reason)
                        + "\n" + personalityMessage("moderation/followrules").replace("{server}", "other servers")
                        + "\n" + "-# This automated message was sent because a moderator banned you using Vivia.")
    except HTTPException:
        await ctx.send("I couldn't DM the user.", ephemeral=True)
    viviatools.log(f"{ctx.author.name} banned {user} from {ctx.guild} ({ctx.guild.id})", logging.DEBUG)

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
    
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send(personalityMessage("nopermissions"), ephemeral=True)
        return
    
    if user == None:
        await ctx.send(personalityMessage("moderation/targetnone"), ephemeral=True)
        return

    if user == ctx.me:
        await ctx.send(personalityMessage("moderation/moderatevivia").replace("{action}", "unban"), ephemeral=True)
        return
    
    if user == ctx.author:
        await ctx.send(personalityMessage("moderation/moderateself").replace("{action}", "unban"), ephemeral=True)
        return
    
    if user.guild_permissions.administrator:
        await ctx.send(personalityMessage("moderation/moderateadmin").replace("{user}", user.name).replace("{action}", "unban"), ephemeral=True)
        return
    
    if user.top_role >= ctx.author.top_role and not ctx.author.guild_permissions.administrator:
        await ctx.send(personalityMessage("moderation/moderatehigher").replace("{user}", user.name).replace("{action}", "unban"), ephemeral=True)
        return

    await ctx.guild.unban(user, reason=f"Unbanned by {ctx.author}: {reason}")
    await ctx.send(personalityMessage("moderation/unban").replace("{user}", user.mention), ephemeral=True)
    try:
        await user.send(f"# You've been unbanned from {ctx.guild} ({ctx.guild.id})\n\n" + personalityMessage("moderation/unbanned").replace("{user}", ctx.author.mention).replace("{server}", ctx.guild.name)
                        + "\n" + personalityMessage("moderation/reason").replace("{reason}", "").replace("{action}", "unbanning").replace("{reason}", "")
                        + "\n" + personalityMessage("moderation/followrules").replace("{server}", ctx.guild.name)
                        + "\n" + "-# This automated message was sent because a moderator unbanned you using Vivia.")
    except HTTPException:
        await ctx.send("I couldn't DM the user.", ephemeral=True)
    viviatools.log(f"{ctx.author.name} unbanned {user} from {ctx.guild} ({ctx.guild.id})", logging.DEBUG)