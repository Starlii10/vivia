"""
    This is the help command, part of the ViviaBase extension package.

    Vivia is licensed under the MIT License. For more information, see the LICENSE file.
    TL:DR: you can use Vivia's code as long as you keep the original license intact.
    Vivia is made open source in the hopes that you'll find her code useful.

    If you'd like to contribute, please check out the GitHub repository at https://github.com/starlii10/vivia.

    Have a great time using Vivia!
"""

if __name__ == "__main__":
    raise Exception("Vivia extensions should not be run as a script.")

import logging
from discord.ext import commands
from discord import app_commands
from extras.viviatools import helpMsg,personalityMessage, loaded_extensions, failed_extensions, log

async def setup(bot: commands.Bot): # for extension loading
    bot.add_command(help)

@commands.hybrid_command()
@app_commands.describe(
    extension="The name of the extension you want help with. "
)
async def help(ctx: commands.Context, extension: str = "core"):
    """
        Help command.
    """
    await ctx.author.send(helpMsg(extension))
    await ctx.send(personalityMessage("base.helpsent").replace("{user}", str(ctx.author)), ephemeral=True)