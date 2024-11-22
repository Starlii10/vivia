"""
    This is the namegenerator command, part of the ViviaBase extension package.

    Vivia is licensed under the MIT License. For more information, see the LICENSE file.
    TL:DR: you can use Vivia's code as long as you keep the original license intact.
    Vivia is made open source in the hopes that you'll find her code useful.

    If you'd like to contribute, please check out the GitHub repository at https://github.com/starlii10/vivia.

    Have a great time using Vivia!
"""

import json
import logging
import os
import random
from discord.ext import commands
from discord import app_commands
from extras.viviatools import log, personalityMessage, config

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
    with open(os.path.join("data", "names.json"), "r") as f:
        names = json.load(f)
        all_names = names['first']['male'] + names['first']['female']
        match type:
            case "first":
                match gender:
                    case "male":
                        name = names['first']['male'][random.randint(0, len(names['first']['male']) - 1)]
                    case "female":
                        name = names['first']['female'][random.randint(0, len(names['first']['female']) - 1)]
                    case _:
                        name = all_names[random.randint(0, len(all_names) - 1)]
            case "middle":
                name = names['middle'][random.randint(0, len(names['middle']) - 1)]
            case "last":
                name = names['last'][random.randint(0, len(names['last']) - 1)]
            case "full":
                match gender:
                    case "male":
                        name = names['first']['male'][random.randint(0, len(names['first']['male']) - 1)] + " "+ names['middle'][random.randint(0, len(names['middle']) - 1)] + " " + names['last'][random.randint(0, len(names['last']) - 1)]
                    case "female":
                        name = names['first']['female'][random.randint(0, len(names['first']['female']) - 1)] + " "+ names['middle'][random.randint(0, len(names['middle']) - 1)] + " " + names['last'][random.randint(0, len(names['last']) - 1)]
                    case _:
                        name = all_names[random.randint(0, len(all_names) - 1)] + " "+ names['middle'][random.randint(0, len(names['middle']) - 1)] + " " + names['last'][random.randint(0, len(names['last']) - 1)]
            
        if config["Advanced"]["Debug"] == "True":
            log(f"Generated name: {name}", logging.DEBUG)
    await ctx.send(personalityMessage("base.namegeneration").replace("{name}", name))