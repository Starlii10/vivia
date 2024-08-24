"""
    This is the quote command used in Vivia.

    Vivia is licensed under the MIT License. For more information, see the LICENSE file.
    TL:DR: you can use Vivia's code as long as you keep the original license intact.
    Vivia is made open source in the hopes that you'll find her code useful.

    If you'd like to contribute, please check out the GitHub repository at https://github.com/starlii10/vivia.

    Have a great time using Vivia!
"""

import json
import logging
import random
import discord
from discord.ext import commands
from bot import serverConfig, tree, log
from extras.viviatools import viviaTools

@tree.command(
    name="quote",
    description="Say a random (slightly chaotic) quote."
)
async def quote(interaction: discord.Interaction):
    """
    Sends a random (slightly chaotic) quote.
    """
    try:
        with open('data/quotes.json') as f:
            with open(f'data/servers/{interaction.guild.id}/quotes.json') as g:
                default_quotes = json.load(f)
                custom_quotes = json.load(g)
                quotes = default_quotes['quotes'] + custom_quotes['quotes']
                quote = random.choice(quotes)
                await interaction.response.send_message(quote)
    except Exception as e:
        await interaction.response.send_message("Something went wrong. Maybe try again?")
        if serverConfig(interaction.guild.id)['verboseErrors']:
            await interaction.followup.send(f"{type(e)}: {e}\n-# To disable these messages, run /config verboseErrors false")
        await log(f"Couldn't send a quote for server {interaction.guild.name} ({interaction.guild.id}): {type(e)}: {e}", severity=logging.ERROR)