"""
    This is the purge command, part of the ViviaBase extension package.

    Vivia is licensed under the MIT License. For more information, see the LICENSE file.
    TL:DR: you can use Vivia's code as long as you keep the original license intact.
    Vivia is made open source in the hopes that you'll find her code useful.

    If you'd like to contribute, please check out the GitHub repository at https://github.com/starlii10/vivia.

    Have a great time using Vivia!
"""

from discord.ext import commands
from discord import app_commands
from extras.viviatools import personalityMessage, adminOnly

async def setup(bot: commands.Bot): # for extension loading
    bot.add_command(purge)

@commands.hybrid_command()
@app_commands.describe(
    start="Message ID or link to start of range",
    end="Message ID or link to end of range"
)
@adminOnly
async def purge(ctx: commands.Context, start: int | str = None, end: int | str = None):
    """
        Purges messages between start and end.
    """
    if start is None and end is None:
        await ctx.channel.purge(limit=None)
    else:
        if start is None:
            await ctx.channel.purge(limit=end)
        elif end is None:
            await ctx.channel.purge(limit=start)
        else:
            await ctx.channel.purge(limit=end - start + 1)
    await ctx.send(personalityMessage("purge"))