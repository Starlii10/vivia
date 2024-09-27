"""
    This is the channelmaker command, part of the ViviaBase extension package.

    Vivia is licensed under the MIT License. For more information, see the LICENSE file.
    TL:DR: you can use Vivia's code as long as you keep the original license intact.
    Vivia is made open source in the hopes that you'll find her code useful.

    If you'd like to contribute, please check out the GitHub repository at https://github.com/starlii10/vivia.

    Have a great time using Vivia!
"""

import json
import logging
from discord.ext import commands
from discord import app_commands
from extras.viviatools import has_bot_permissions, log, personalityMessage, serverConfig

async def setup(bot: commands.Bot): # for extension loading
    bot.add_command(channelmaker)

@commands.hybrid_command(
    name = "channelmaker",
)
@app_commands.choices(type=[
    app_commands.Choice(name="text",value="text"),
    app_commands.Choice(name="voice",value="voice"),
    app_commands.Choice(name="forum",value="forum"),
])
async def channelmaker(ctx: commands.Context, channel_config: str, type: str="text"):
    """
    Makes a bunch of channels from JSON.

    ## Args:
        - channel_config (str): The JSON string containing the channel configuration.
        - type (str): The type of channel to make. Defaults to "text".
    ## Notes:
        - Only users with bot permissions can use this command.
        - The channelmaker JSON configuration looks like this: {"categories":{"test":["test"]}}
        - For more info, read the channelmakerhelpmsg.txt file or run /help channelmaker when the bot is running.
    """
    if has_bot_permissions(ctx.author, ctx.guild):
        await ctx.send("Making channels! (This may take a moment.)")
        try:
            try:
                channels = json.loads(channel_config) # Channels is a list of categories, each category is a list of channels
            except Exception:
                await ctx.send(f"I couldn't parse that JSON.\n\nIf you need help with using this command, run /help channelmaker.")
                return
            for category in channels['categories']:
                if not category in ctx.guild.categories:
                    # Create the category
                    target = await ctx.guild.create_category(category, reason=f"Created by /channelmaker - run by {ctx.author}")
                else:
                    target = ctx.guild.categories.get(category)
                for channel in channels['categories'][category]:
                    # Create the channel
                    match type:
                        case "text":
                            await ctx.guild.create_text_channel(channel, category=target, reason=f"Created by /channelmaker - run by {ctx.author}")
                        case "voice":
                            await ctx.guild.create_voice_channel(channel, category=target, reason=f"Created by /channelmaker - run by {ctx.author}")
                        case "forum":
                            await ctx.guild.create_forum(channel, category=target, reason=f"Created by /channelmaker - run by {ctx.author}")
        except Exception as e:
            await ctx.send(personalityMessage("error"))
            if serverConfig(ctx.guild.id)['verboseErrors']:
                await ctx.send(str(e) + "\n-# To disable these messages, run /config verboseErrors false")
            await log(f"Error while making channels in server {str(ctx.guild.name)} ({str(ctx.guild.id)}): {type(e)}: {str(e)}", severity=logging.ERROR)
    else:
        await ctx.send("That's for authorized users, not you...", ephemeral=True)