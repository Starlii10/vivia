"""
    This is the leveling system, part of the ViviaBase extension package.

    Vivia is licensed under the MIT License. For more information, see the LICENSE file.
    TL:DR: you can use Vivia's code as long as you keep the original license intact.
    Vivia is made open source in the hopes that you'll find her code useful.

    If you'd like to contribute, please check out the GitHub repository at https://github.com/starlii10/vivia.

    Have a great time using Vivia!
"""

if __name__ == "__main__":
    raise Exception("Vivia extensions should not be run as a script.")

import json
import random
import discord
from discord.ext import commands
from discord import app_commands
from extras.viviatools import adminOnly, personalityMessage, perServerFile, blockInDMs

async def setup(bot):
    await bot.add_cog(leveling(bot))


class leveling(commands.Cog):
    """
    The leveling system.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("leveling_message")
    async def on_message(self, message: discord.Message):
        # Don't give leveling experience to bots
        if message.author.bot:
            return

        # Make sure we're in a guild
        if not message.guild:
            return

        # Create server leveling data if it doesn't exist
        if not perServerFile(message.guild.id, "leveling.json"):
            with perServerFile(message.guild.id, "leveling.json", "{}") as f:
                json.dump({"leveling": {}}, f)

        # Get leveling data
        with perServerFile(message.guild.id, "leveling.json") as f:
            leveling = json.load(f)
            if not str(message.author.id) in leveling["leveling"]:
                leveling["leveling"][str(message.author.id)] = {
                    "level": 1,
                    "xp": 0
                }
            # Give random amount of XP
            leveling["leveling"][str(message.author.id)]["xp"] += random.randint(1, 5)


        # Check if the user has leveled up
        with perServerFile(message.guild.id, "leveling.json") as f:
            leveling = json.load(f)
            if leveling["leveling"][str(message.author.id)]["xp"] >= leveling["leveling"][str(message.author.id)]["level"] * 5:
                leveling["leveling"][str(message.author.id)]["level"] += 1
                # Add leftover XP
                leveling["leveling"][str(message.author.id)]["xp"] = 0 - (leveling["leveling"][str(message.author.id)]["level"] * 5 - leveling["leveling"][str(message.author.id)]["xp"])
                await message.reply(personalityMessage("leveling.levelup").replace("{level}", str(leveling["leveling"][str(message.author.id)]["level"])))
        
        # Save leveling data
        with perServerFile(message.guild.id, "leveling.json") as f:
            json.dump(leveling, f)
    
    @blockInDMs
    @commands.hybrid_command(
        name = "level",
        description = "Checks your current level."
    )
    async def level(self, ctx: commands.Context):
        """
        Checks your current level.
        """

        await ctx.send(personalityMessage("leveling.level").replace("{level}", str(ctx.author.level)))
    
    @blockInDMs
    @adminOnly
    @commands.hybrid_command(
        name = "setlevel",
        description = "Sets a user's level."
    )
    async def setlevel(self, ctx: commands.Context, user: discord.User, level: int):
        """
        Sets a user's level.
        """

        with perServerFile(ctx.guild.id, "leveling.json") as f:
            leveling = json.load(f)
            leveling["leveling"][str(user.id)]["level"] = level
            json.dump(leveling, f)

        await ctx.send(personalityMessage("leveling.setlevel").replace("{user}", user.mention).replace("{level}", str(level)))

    @blockInDMs
    @adminOnly
    @commands.hybrid_command(
        name = "resetlevel",
        description = "Resets a user's level."
    )
    async def resetlevel(self, ctx: commands.Context, user: discord.User):
        """
        Resets a user's level.
        """

        with perServerFile(ctx.guild.id, "leveling.json") as f:
            leveling = json.load(f)
            leveling["leveling"][str(user.id)]["level"] = 1
            leveling["leveling"][str(user.id)]["xp"] = 0
            json.dump(leveling, f)

        await ctx.send(personalityMessage("leveling.resetuserlevel").replace("{user}", user.mention))
    
    @blockInDMs
    @adminOnly
    @commands.hybrid_command(
        name = "resetlevels",
        description = "Resets all users' levels."
    )
    async def resetlevels(self, ctx: commands.Context):
        """
        Resets all users' levels.
        """

        with perServerFile(ctx.guild.id, "leveling.json") as f:
            leveling = json.load(f)
            leveling["leveling"] = {}
            json.dump(leveling, f)

        await ctx.send(personalityMessage("leveling.resetlevels"))