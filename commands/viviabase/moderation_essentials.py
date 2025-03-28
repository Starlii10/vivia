#!/usr/bin/env python
"""
This is the essential moderation extension, part of the ViviaBase extension package.

Vivia is licensed under the MIT License. For more information, see the LICENSE file.
TL:DR: you can use Vivia's code as long as you keep the original license intact.
Vivia is made open source in the hopes that you'll find her code useful.

If you'd like to contribute, please check out the GitHub repository at https://github.com/starlii10/vivia.

Have a great time using Vivia!
"""

import json
import logging
import os
import discord
from discord.ext import commands
from discord import app_commands
from extras import viviatools
from extras.viviatools import personality_message

if __name__ == "__main__":
    raise Exception("Vivia extensions should not be run as a script.")

async def setup(bot: commands.Bot):
    """
    The main setup function for an extension.
    """
    bot.add_command(warn)
    bot.add_command(unwarn)
    bot.add_command(kick)
    bot.add_command(ban)
    bot.add_command(unban)


@commands.hybrid_command(name="warn")
@app_commands.describe(user="The user to warn.", reason="The reason for the warning.")
@viviatools.block_in_dms
async def warn(
    ctx: commands.Context, user: discord.Member, reason: str = "No reason provided."
):
    """
    Warns a user.

    Args:
        - user (discord.User): The user to warn.
        - reason (str): The reason for the warning.
    """

    if not ctx.author.guild_permissions.moderate_members:
        await ctx.send(personality_message("errors.nopermissions"), ephemeral=True)
        return

    if user is None:
        await ctx.send(personality_message("errors.targetnone"), ephemeral=True)
        return

    if user == ctx.me:
        await ctx.send(
            personality_message("moderation.moderatevivia").replace("{action}", "warn"),
            ephemeral=True,
        )
        return

    if user == ctx.author:
        await ctx.send(
            personality_message("moderation.moderateself").replace("{action}", "warn"),
            ephemeral=True,
        )
        return

    if user.guild_permissions.administrator:
        await ctx.send(
            personality_message("moderation.moderateadmin")
            .replace("{user}", user.name)
            .replace("{action}", "warn"),
            ephemeral=True,
        )
        return

    if (
        user.top_role >= ctx.author.top_role
        and not ctx.author.guild_permissions.administrator
    ):
        await ctx.send(
            personality_message("moderation.moderatehigher")
            .replace("{user}", user.name)
            .replace("{action}", "warn"),
            ephemeral=True,
        )
        return

    # add user to warned users
    # TODO: users can be warned multiple times
    viviatools.log(
        json.dumps(
            [
                reason,
                ctx.message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                ctx.author.id,
            ]
        )
    )
    with open(
        os.path.join("data", "servers", str(ctx.guild.id), "warns.json"),
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            {
                user.id: [
                    reason,
                    ctx.message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    ctx.author.id,
                ]
            },
            f,
        )

    viviatools.log(
        f"{ctx.author.name} warned {user} in {ctx.guild} ({ctx.guild.id})",
        logging.DEBUG,
    )

    # messages
    await ctx.send(
        personality_message("moderation.warn").replace("{user}", user.mention),
        ephemeral=True,
    )

    try:
        await user.send(
            f"# You've been warned in {ctx.guild} ({ctx.guild.id})\n\n"
            + personality_message("moderation.warned")
            .replace("{server}", ctx.guild.name)
            .replace("{user}", ctx.author.mention)
            + "\n"
            + personality_message("moderation.reason")
            .replace("{reason}", reason)
            .replace("{action}", "warning")
            .replace("{reason}", reason)
            + "\n\n"
            + personality_message("moderation.followrules").replace(
                "{server}", ctx.guild.name
            )
            + "\n"
            + "-# This automated message was sent because a moderator warned you using Vivia."
        )
    except:
        await ctx.send("I couldn't DM the user.", ephemeral=True)

    viviatools.log(f"{ctx.author.name} warned {user} in {ctx.guild} ({ctx.guild.id})")


@commands.hybrid_command(name="unwarn")
@app_commands.describe(
    user="The user to unwarn.", reason="The reason for the unwarning."
)
@viviatools.block_in_dms
async def unwarn(
    ctx: commands.Context, user: discord.Member, reason: str = "No reason provided."
):
    """
    Unwarns a user.

    Args:
        - user (discord.User): The user to unwarn.
        - reason (str): The reason for the unwarning.
    """

    if not ctx.author.guild_permissions.moderate_members:
        await ctx.send(personality_message("errors.nopermissions"), ephemeral=True)
        return

    if user is None:
        await ctx.send(personality_message("errors.targetnone"), ephemeral=True)
        return

    if user == ctx.me:
        await ctx.send(
            personality_message("moderation.moderatevivia").replace(
                "{action}", "unwarn"
            ),
            ephemeral=True,
        )
        return

    if user == ctx.author:
        await ctx.send(
            personality_message("moderation.moderateself").replace(
                "{action}", "unwarn"
            ),
            ephemeral=True,
        )
        return

    if user.guild_permissions.administrator:
        await ctx.send(
            personality_message("moderation.moderateadmin")
            .replace("{user}", user.name)
            .replace("{action}", "unwarn"),
            ephemeral=True,
        )
        return

    if (
        user.top_role >= ctx.author.top_role
        and not ctx.author.guild_permissions.administrator
    ):
        await ctx.send(
            personality_message("moderation.moderatehigher")
            .replace("{user}", user.name)
            .replace("{action}", "unwarn"),
            ephemeral=True,
        )
        return

    # remove user from warned users
    # TODO: users can be warned multiple times
    with open(f"data/servers/{ctx.guild.id}/warns.json", "r", encoding="utf-8") as f:
        warns = json.load(f)
        if warns.get(str(user.id)) is not None:
            del warns[str(user.id)]
        else:
            await ctx.send(
                personality_message("moderation.notwarned").replace(
                    "{user}", user.mention
                ),
                ephemeral=True,
            )
            return
        with open(
            f"data/servers/{ctx.guild.id}/warns.json", "w", encoding="utf-8"
        ) as f:
            json.dump(warns, f)

    viviatools.log(
        f"{ctx.author.name} unwarned {user} in {ctx.guild} ({ctx.guild.id})",
        logging.DEBUG,
    )

    # messages
    await ctx.send(
        personality_message("moderation.unwarn").replace("{user}", user.mention),
        ephemeral=True,
    )
    try:
        await user.send(
            f"# You've been unwarned in {ctx.guild} ({ctx.guild.id})\n\n"
            + personality_message("moderation.unwarned").replace(
                "{user}", ctx.author.mention
            )
            + "\n"
            + personality_message("moderation.reason")
            .replace("{reason}", reason)
            .replace("{action}", "unwarning")
            .replace("{reason}", reason)
            + "\n\n"
            + personality_message("moderation.followrules").replace(
                "{server}", ctx.guild.name
            )
            + "\n"
            + "-# This automated message was sent because a moderator unwarned you using Vivia."
        )
    except:
        await ctx.send("I couldn't DM the user.", ephemeral=True)
    viviatools.log(
        f"{ctx.author.name} unwarned {user} in {ctx.guild} ({ctx.guild.id})",
        logging.DEBUG,
    )


@commands.hybrid_command(name="kick")
@app_commands.describe(user="The user to kick.", reason="The reason for the kick.")
@viviatools.block_in_dms
async def kick(
    ctx: commands.Context, user: discord.Member, reason: str = "No reason provided."
):
    """
    Kicks a user.

    Args:
        - user (discord.User): The user to kick.
        - reason (str): The reason for the kick.
    """

    if not ctx.author.guild_permissions.kick_members:
        await ctx.send(personality_message("errors.nopermissions"), ephemeral=True)
        return

    if user is None:
        await ctx.send(personality_message("errors.targetnone"), ephemeral=True)
        return

    if user == ctx.me:
        await ctx.send(
            personality_message("moderation.moderatevivia").replace("{action}", "kick"),
            ephemeral=True,
        )
        return

    if user == ctx.author:
        await ctx.send(
            personality_message("moderation.moderateself").replace("{action}", "kick"),
            ephemeral=True,
        )
        return

    if user.guild_permissions.administrator:
        await ctx.send(
            personality_message("moderation.moderateadmin")
            .replace("{user}", user.name)
            .replace("{action}", "kick"),
            ephemeral=True,
        )
        return

    if (
        user.top_role >= ctx.author.top_role
        and not ctx.author.guild_permissions.administrator
    ):
        await ctx.send(
            personality_message("moderation.moderatehigher")
            .replace("{user}", user.name)
            .replace("{action}", "kick"),
            ephemeral=True,
        )
        return

    await user.kick(reason=f"Kicked by {ctx.author}: {reason}")
    await ctx.send(
        personality_message("moderation.moderationactions")
        .replace("{user}", user.mention)
        .replace("{action}", "kicked"),
        ephemeral=True,
    )
    try:
        await user.send(
            f"# You've been kicked from {ctx.guild} ({ctx.guild.id})\n\n"
            + personality_message("moderation.kicked")
            .replace("{user}", ctx.author.mention)
            .replace("{server}", ctx.guild.name)
            + "\n"
            + personality_message("moderation.reason")
            .replace("{reason}", "")
            .replace("{action}", "kicking")
            .replace("{reason}", reason)
            + "\n\n"
            + personality_message("moderation.followrules").replace(
                "{server}", ctx.guild.name
            )
            + "\n"
            + "-# This automated message was sent because a moderator kicked you using Vivia."
        )
    except:
        await ctx.send("I couldn't DM the user.", ephemeral=True)
    viviatools.log(
        f"{ctx.author.name} kicked {user} from {ctx.guild} ({ctx.guild.id})",
        logging.DEBUG,
    )


@commands.hybrid_command(name="ban")
@app_commands.describe(user="The user to ban.", reason="The reason for the ban.")
@viviatools.block_in_dms
async def ban(
    ctx: commands.Context, user: discord.Member, reason: str = "No reason provided."
):
    """
    Bans a user.

    Args:
        - user (discord.User): The user to ban.
        - reason (str): The reason for the ban.
    """

    if not ctx.author.guild_permissions.ban_members:
        await ctx.send(personality_message("errors.nopermissions"), ephemeral=True)
        return

    if user is None:
        await ctx.send(personality_message("errors.targetnone"), ephemeral=True)
        return

    if user == ctx.me:
        await ctx.send(
            personality_message("moderation.moderatevivia").replace("{action}", "ban"),
            ephemeral=True,
        )
        return

    if user == ctx.author:
        await ctx.send(
            personality_message("moderation.moderateself").replace("{action}", "ban"),
            ephemeral=True,
        )
        return

    if user.guild_permissions.administrator:
        await ctx.send(
            personality_message("moderation.moderateadmin")
            .replace("{user}", user.name)
            .replace("{action}", "ban"),
            ephemeral=True,
        )
        return

    if (
        user.top_role >= ctx.author.top_role
        and not ctx.author.guild_permissions.administrator
    ):
        await ctx.send(
            personality_message("moderation.moderatehigher")
            .replace("{user}", user.name)
            .replace("{action}", "ban"),
            ephemeral=True,
        )
        return

    await user.ban(reason=f"Banned by {ctx.author}: {reason}")
    await ctx.send(
        personality_message("moderation.moderationactions")
        .replace("{user}", user.mention)
        .replace("{action}", "banned"),
        ephemeral=True,
    )
    try:
        await user.send(
            f"# You've been banned from {ctx.guild} ({ctx.guild.id})\n\n"
            + personality_message("moderation.banned")
            .replace("{user}", ctx.author.mention)
            .replace("{server}", ctx.guild.name)
            + "\n"
            + personality_message("moderation.reason")
            .replace("{reason}", "")
            .replace("{action}", "banning")
            .replace("{reason}", reason)
            + "\n"
            + personality_message("moderation.followrules").replace(
                "{server}", "other servers"
            )
            + "\n"
            + "-# This automated message was sent because a moderator banned you using Vivia."
        )
    except:
        await ctx.send("I couldn't DM the user.", ephemeral=True)
    viviatools.log(
        f"{ctx.author.name} banned {user} from {ctx.guild} ({ctx.guild.id})",
        logging.DEBUG,
    )


@commands.hybrid_command(name="unban")
@app_commands.describe(user="The user to unban.")
@viviatools.block_in_dms
async def unban(
    ctx: commands.Context, user: discord.User, reason: str = "No reason provided."
):
    """
    Unbans a user.

    Args:
        - user (discord.User): The user to unban.
        - reason (str): The reason for the unban.
    """

    if not ctx.author.guild_permissions.ban_members:
        await ctx.send(personality_message("errors.nopermissions"), ephemeral=True)
        return

    if user is None:
        await ctx.send(personality_message("errors.targetnone"), ephemeral=True)
        return

    if user == ctx.me:
        await ctx.send(
            personality_message("moderation.moderatevivia").replace(
                "{action}", "unban"
            ),
            ephemeral=True,
        )
        return

    if user == ctx.author:
        await ctx.send(
            personality_message("moderation.moderateself").replace("{action}", "unban"),
            ephemeral=True,
        )
        return

    if user.guild_permissions.administrator:
        await ctx.send(
            personality_message("moderation.moderateadmin")
            .replace("{user}", user.name)
            .replace("{action}", "unban"),
            ephemeral=True,
        )
        return

    if (
        user.top_role >= ctx.author.top_role
        and not ctx.author.guild_permissions.administrator
    ):
        await ctx.send(
            personality_message("moderation.moderatehigher")
            .replace("{user}", user.name)
            .replace("{action}", "unban"),
            ephemeral=True,
        )
        return

    await ctx.guild.unban(user, reason=f"Unbanned by {ctx.author}: {reason}")
    await ctx.send(
        personality_message("moderation.unban").replace("{user}", user.mention),
        ephemeral=True,
    )
    try:
        await user.send(
            f"# You've been unbanned from {ctx.guild} ({ctx.guild.id})\n\n"
            + personality_message("moderation.unbanned")
            .replace("{user}", ctx.author.mention)
            .replace("{server}", ctx.guild.name)
            + "\n"
            + personality_message("moderation.reason")
            .replace("{reason}", "")
            .replace("{action}", "unbanning")
            .replace("{reason}", "")
            + "\n"
            + personality_message("moderation.followrules").replace(
                "{server}", ctx.guild.name
            )
            + "\n"
            + "-# This automated message was sent because a moderator unbanned you using Vivia."
        )
    except:
        await ctx.send("I couldn't DM the user.", ephemeral=True)
    viviatools.log(
        f"{ctx.author.name} unbanned {user} from {ctx.guild} ({ctx.guild.id})",
        logging.DEBUG,
    )
