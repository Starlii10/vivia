"""
    This is the purge command, part of the ViviaBase extension package.

    Vivia is licensed under the MIT License. For more information, see the LICENSE file.
    TL:DR: you can use Vivia's code as long as you keep the original license intact.
    Vivia is made open source in the hopes that you'll find her code useful.

    If you'd like to contribute, please check out the GitHub repository at https://github.com/starlii10/vivia.

    Have a great time using Vivia!
"""

from discord.ext import commands
from discord import Message, app_commands
from extras.viviatools import personalityMessage, adminOnly

async def setup(bot: commands.Bot): # for extension loading
    bot.add_command(purge)

@commands.hybrid_command(
    name="purge",
    description="Purges (deletes) messages between start and end."
)
@app_commands.describe(
    start="Message ID or link to start of range",
    end="Message ID or link to end of range"
)
@adminOnly
async def purge(ctx: commands.Context, start: int = None, end: int = None):
    """
        Purges (deletes) messages between start and end.

        # Args:
            - start (int, optional): The ID of the message to start purging from. Defaults to None.
            - end (int, optional): The ID of the message to end purging at. Defaults to None.

        # Notes:
            - If both start and end are None, all messages in the channel are purged.
            - If start is None, all messages up to the end are purged.
            - If end is None, all messages starting from the start are purged.
    """

    await ctx.send(personalityMessage("purging") + "\n-# This may take a while. Vivia will most likely get rate limited...")

    if start == None and end == None:
        await ctx.channel.purge()
    else:
        # IDs to objects
        if start != None:
            start = await ctx.channel.fetch_message(start)
        if end != None:
            end = await ctx.channel.fetch_message(end)

        # Convert to timestamps
        if start != None:
            start = start.created_at
        if end != None:
            end = end.created_at
            
        # Purge
        await ctx.channel.purge(
            after=start,
            before=end
        )
    await ctx.send(personalityMessage("purge"))