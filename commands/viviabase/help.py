"""
    This is the help command, part of the ViviaBase extension package.

    Vivia is licensed under the MIT License. For more information, see the LICENSE file.
    TL:DR: you can use Vivia's code as long as you keep the original license intact.
    Vivia is made open source in the hopes that you'll find her code useful.

    If you'd like to contribute, please check out the GitHub repository at https://github.com/starlii10/vivia.

    Have a great time using Vivia!
"""

from discord.ext import commands
from discord import app_commands
from extras.viviatools import helpMsg,personalityMessage, loaded_extensions, failed_extensions

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
    # we need to account for custom extensions too
    if extension in loaded_extensions or extension in failed_extensions:
        await ctx.send(helpMsg(extension))
    else:
        await ctx.send(personalityMessage("extensionnotloaded"))