"""
    This is the removequote command used in Vivia.

    Vivia is licensed under the MIT License. For more information, see the LICENSE file.
    TL:DR: you can use Vivia's code as long as you keep the original license intact.
    Vivia is made open source in the hopes that you'll find her code useful.

    If you'd like to contribute, please check out the GitHub repository at https://github.com/starlii10/vivia.

    Have a great time using Vivia!
"""

import json
import logging
from discord.ext import commands
from discord import app_commands
from extras.viviatools import has_bot_permissions, log, config, serverConfig

async def setup(bot: commands.Bot): # for extension loading
    bot.add_command(removequote)

@commands.hybrid_command(
    name = "removequote",
)
@app_commands.describe(
    quote = "The quote to remove."
)
async def removequote(ctx: app_commands.Context, quote: str):
    """
    Removes a quote from the list.

    ## Args:
        - quote (str): The quote to remove.
    ## Notes:
        - Only users with bot permissions can use this command.
        - This removes the quote from the custom quote list.
    """
    if has_bot_permissions(ctx.author, ctx.guild):
        try:
            with open(f'data/servers/{str(ctx.guild.id)}/quotes.json') as f:
                quotes = json.load(f)
                if quote in quotes['quotes']:
                    quotes['quotes'].remove(quote)
                else:
                    await ctx.send("That quote isn't in the list, though...")
                    return
            with open('quotes.json', 'w') as f:
                json.dump(quotes, f)
        except Exception as e:
            await ctx.send(f'Something went wrong. Maybe try again?')
            if config["General"]["VerboseErrors"]:
                await ctx.send(f"{type(e)}: {e}\n-# To disable these messages, run /config verboseErrors false")
            await log(f'Failed to remove "{quote}" from the list for server {ctx.guild.name} ({ctx.guild.id}): {type(e)}: {e}', severity=logging.ERROR)
            return
        await ctx.send(f'"{quote}" was removed from the list.')
        await log(f"{ctx.author} removed \"{quote}\" from the list")
    else:
        await ctx.send("That's for authorized users, not you...")