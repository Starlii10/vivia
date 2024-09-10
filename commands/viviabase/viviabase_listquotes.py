"""
    This is the listquotes command used in Vivia.

    Vivia is licensed under the MIT License. For more information, see the LICENSE file.
    TL:DR: you can use Vivia's code as long as you keep the original license intact.
    Vivia is made open source in the hopes that you'll find her code useful.

    If you'd like to contribute, please check out the GitHub repository at https://github.com/starlii10/vivia.

    Have a great time using Vivia!
"""

from discord.ext import commands
import json
import logging
from extras.viviatools import serverConfig, log

async def setup(bot: commands.Bot): # for extension loading
    bot.add_command(listquotes)

@commands.hybrid_command(
    name="listquotes"
)
async def listquotes(ctx: commands.Context):
    """
    Sends a list of all quotes.
    """
    try:
        with open('data/quotes.json') as f:
            with open(f'data/servers/{ctx.guild.id}/quotes.json') as g:
                default_quotes = json.load(f)
                custom_quotes = json.load(g)
                quotes = default_quotes['quotes'] + custom_quotes['quotes']
                await ctx.send(quotes)
    except Exception as e:
        await ctx.send("Something went wrong. Maybe try again?")
        if serverConfig(ctx.guild.id)['verboseErrors']:
            await ctx.send(f"{type(e)}: {e}\n-# To disable these messages, run /config verboseErrors false")
        await log(f"Couldn't list quotes for server {ctx.guild.name} ({ctx.guild.id}): {type(e)}: {e}", severity=logging.ERROR)