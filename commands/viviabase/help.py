"""
    This is the help command used in Vivia.

    Vivia is licensed under the MIT License. For more information, see the LICENSE file.
    TL:DR: you can use Vivia's code as long as you keep the original license intact.
    Vivia is made open source in the hopes that you'll find her code useful.

    If you'd like to contribute, please check out the GitHub repository at https://github.com/starlii10/vivia.

    Have a great time using Vivia!
"""

from discord.ext import commands
from discord import app_commands
from extras.viviatools import helpMsg, channelmakerHelpMsg, setupHelpMsg, personalityMessage

async def setup(bot: commands.Bot): # for extension loading
    bot.add_command(help)

@commands.hybrid_command(
    name="help",
)
@app_commands.choices(message=[
    app_commands.Choice(name="general", value="general"),
    app_commands.Choice(name="channelmaker", value="channelmaker"),
    app_commands.Choice(name="setup", value="setup"),
])
@app_commands.describe(message="The message to send to the user.")
async def help(ctx: commands.Context, message: str="general"):
    match message:
        case "general":
            await ctx.author.send(helpMsg)
        case "channelmaker":
            await ctx.author.send(channelmakerHelpMsg)
        case "setup":
            await ctx.author.send(setupHelpMsg)
        case _:
            await ctx.author.send(helpMsg)
    await ctx.send(personalityMessage("helpsent").replace("{user}", ctx.author.mention), ephemeral=True)