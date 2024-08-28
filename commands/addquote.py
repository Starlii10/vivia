"""
    This is the addquote command used in Vivia.

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
from discord import app_commands
from extras.viviatools import has_bot_permissions, log, config, add_custom_quote

async def setup(bot: commands.Bot): # for extension loading
    bot.add_command(addquote)

@commands.hybrid_command(
    name="addquote",
)
@app_commands.describe(
    quote="The quote to add.",
    author="The author of the quote.",
    date="The date of the quote.",
)
async def addquote(ctx: commands.Context, quote: str, author: str, date: str):
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
    if has_bot_permissions(ctx.author, ctx.guild):
        try:
            add_custom_quote(f'"{quote}" - {author}, {date}', ctx.guild.id)
        except Exception as e:
            await ctx.send(f'Something went wrong. Maybe try again?')
            if config["General"]["VerboseErrors"]:
                await ctx.send(f"{type(e)}: {e}\n-# To disable these messages, run /config verboseErrors false")
            await log(f'Failed to add "{quote} - {author}, {date}" to the custom quote list for server {ctx.guild.name} ({ctx.guild.id}): {type(e)}: {e}', severity=logging.ERROR)
            return
        await ctx.send(f'"{quote}" - {author}, {date} was added to the list.')
        await log(f"{ctx.author} added \"{quote} - {author}, {date}\" to the custom quote list for server {ctx.guild.name} ({ctx.guild.id})")
    else:
        await ctx.send("That's for authorized users, not you...")