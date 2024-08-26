"""
    This is the namegenerator command used in Vivia.

    Vivia is licensed under the MIT License. For more information, see the LICENSE file.
    TL:DR: you can use Vivia's code as long as you keep the original license intact.
    Vivia is made open source in the hopes that you'll find her code useful.

    If you'd like to contribute, please check out the GitHub repository at https://github.com/starlii10/vivia.

    Have a great time using Vivia!
"""

from discord.ext import commands
from discord import app_commands
from extras.viviatools import generate_name

async def setup(bot: commands.Bot): # for extension loading
    bot.add_command(namegenerator)

@commands.hybrid_command(
    name = "namegenerator",
)
@app_commands.choices(type=[
    app_commands.Choice(name="first",value="first"),
    app_commands.Choice(name="middle",value="middle"),
    app_commands.Choice(name="last",value="last"),
    app_commands.Choice(name="full",value="full"),
])
@app_commands.choices(gender=[
    app_commands.Choice(name="male",value="male"),
    app_commands.Choice(name="female",value="female"),
    app_commands.Choice(name="none",value="none"),
])
@app_commands.describe(
    type = "The type of name to generate.",
    gender = "The gender of the name.",
)
async def namegenerator(ctx: commands.Context, type: str="first", gender: str="none"):
    """
    Generator for names.
    """
    name = generate_name(type, gender)
    await ctx.send(name)