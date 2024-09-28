"""
    This is a simple ping command, part of the ViviaBase extension package.

    Vivia is licensed under the MIT License. For more information, see the LICENSE file.
    TL:DR: you can use Vivia's code as long as you keep the original license intact.
    Vivia is made open source in the hopes that you'll find her code useful.

    If you'd like to contribute, please check out the GitHub repository at https://github.com/starlii10/vivia.

    Have a great time using Vivia!
"""

from discord.ext import commands
from extras.viviatools import personalityMessage, bot_ref

async def setup(bot: commands.Bot):
    bot.add_command(ping)

@commands.hybrid_command(
    name="ping",
    description="Shows the bot's latency.",
)
async def ping(ctx: commands.Context):
    await ctx.send(personalityMessage("ping").replace("{ping}", str(bot_ref.latency * 1000) + "ms"))