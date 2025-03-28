#!/usr/bin/env python
"""
    This is a simple ping command, part of the ViviaBase extension package.

    Vivia is licensed under the MIT License. For more information, see the LICENSE file.
    TL:DR: you can use Vivia's code as long as you keep the original license intact.
    Vivia is made open source in the hopes that you'll find her code useful.

    If you'd like to contribute, please check out the GitHub repository at https://github.com/starlii10/vivia.

    Have a great time using Vivia!
"""

from discord.ext import commands
from extras.viviatools import personality_message, bot

if __name__ == "__main__":
    raise Exception("Vivia extensions should not be run as a script.")

async def setup(bot: commands.Bot):
    """
        The main setup function for an extension.
    """
    bot.add_command(ping)

@commands.hybrid_command(
    name="ping",
    description="Shows the bot's latency.",
)
async def ping(ctx: commands.Context):
    """
        Shows the bot's latency.
    """
    await ctx.send(personality_message("base.ping")
                   .replace("{ping}", str(bot.latency * 1000) + "ms"))
