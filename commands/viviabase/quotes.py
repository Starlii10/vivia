#!/usr/bin/env python
"""
    This is the quote extension, part of the ViviaBase extension package.

    Vivia is licensed under the MIT License. For more information, see the LICENSE file.
    TL:DR: you can use Vivia's code as long as you keep the original license intact.
    Vivia is made open source in the hopes that you'll find her code useful.

    If you'd like to contribute, please check out the GitHub repository at https://github.com/starlii10/vivia.

    Have a great time using Vivia!
"""

if __name__ == "__main__":
    raise Exception("Vivia extensions should not be run as a script.")

import json
import logging
import os
import random
import discord
from discord.ext import commands
from discord import app_commands
from extras import viviatools
from extras.viviatools import log, config, add_custom_quote, personalityMessage, serverConfig

async def setup(bot: commands.Bot):
    bot.add_command(addquote)
    bot.add_command(removequote)
    bot.add_command(quote)
    bot.add_command(listquotes)
    bot.tree.add_command(contextmenu_addquote)

@commands.hybrid_command(
    name="addquote",
)
@app_commands.describe(
    quote="The quote's text.",
    author="The author of the quote.",
    date="The date that the quote was made.",
)
@viviatools.blockInDMs
@viviatools.adminOnly
async def addquote(ctx: commands.Context, quote: str, author: str, date: str):
    """
    Adds a quote to the list.

    ## Args:
        - quote (str): The quote to add.
        - author (str): The author of the quote.
        - date (str): The date of the quote.
    ## Notes:
        - Only users with bot permissions can use this command.
        - The quote will be formatted as `"quote" - author, date`.
        - This adds the quote to the custom quote list for the server the command was used in.
    """

    try:
        add_custom_quote(f'"{quote}" - {author}, {date}', ctx.guild.id)
    except Exception as e:
        await ctx.send(personalityMessage("errors.error"))
        if config["General"]["VerboseErrors"]:
            await ctx.send(f"{type(e)}: {e}\n-# To disable these messages, run /config verboseErrors false")
        await log(f'Failed to add "{quote} - {author}, {date}" to the custom quote list for server {ctx.guild.name} ({ctx.guild.id}): {type(e)}: {e}', severity=logging.ERROR)
        return
    await ctx.send(f'"{quote}" - {author}, {date} was added to the list.')
    await log(f"{ctx.author} added \"{quote} - {author}, {date}\" to the custom quote list for server {ctx.guild.name} ({ctx.guild.id})", severity=logging.DEBUG)

@commands.hybrid_command(
    name="quote",
    description="Sends a random (slightly insane) quote."
)
async def quote(ctx: commands.Context):
    """
    Sends a random (slightly insane) quote.
    """
    try:
        with open(os.path.join('data', 'quotes.json')) as f:
            if ctx.guild:
                with open(os.path.join('data', 'servers', str(ctx.guild.id), 'quotes.json')) as g:
                    default_quotes = json.load(f)
                    custom_quotes = json.load(g)
                    quotes = default_quotes['quotes'] + custom_quotes['quotes']
                    quote = random.choice(quotes)
                    await ctx.send(quote)
            else:
                quote = random.choice(json.load(f)['quotes'])
                await ctx.send(quote)
    except Exception as e:
        await ctx.send(personalityMessage("errors.error"))
        if ctx.guild:
            if serverConfig(ctx.guild.id)['verboseErrors']:
                await ctx.send(f"{type(e)}: {e}\n-# To disable these messages, run /config verboseErrors false")
        await log(f"Couldn't send a quote for server {ctx.guild.name} ({ctx.guild.id}): {type(e)}: {e}", severity=logging.ERROR)

@commands.hybrid_command(
    name="listquotes",
    description="Sends a list of all quotes."
)
@app_commands.describe(
    customonly="Whether to only list custom quotes."
)
async def listquotes(ctx: commands.Context, customonly: bool = False):
    """
    Sends a list of all quotes.
    """
    try:
        if customonly:
            if ctx.guild:
                with open(f'data/servers/{ctx.guild.id}/quotes.json') as f:
                    quotes = json.load(f)['quotes']
                    quotes = '\n'.join(quotes)
                    await ctx.send(quotes)
            else:
                await ctx.send(personalityMessage("errors.error")
                                + "\n-# `customonly` flag only works in a server.")
                return
        else:
            with open('data/quotes.json') as f:
                if ctx.guild:
                    with open(f'data/servers/{ctx.guild.id}/quotes.json') as g:
                        default_quotes = json.load(f)
                        custom_quotes = json.load(g)
                        quotes = default_quotes['quotes'] + custom_quotes['quotes']
                        quotes = '\n'.join(quotes)
                        await ctx.send(quotes)
                else:
                    quotes = json.load(f)['quotes']
                    quotes = '\n'.join(quotes)
                    await ctx.send(quotes)
    except Exception as e:
        await ctx.send(personalityMessage("errors.error"))
        if ctx.guild:
            if serverConfig(ctx.guild.id)['verboseErrors']:
                await ctx.send(f"{type(e)}: {e}\n-# To disable these messages, run /config verboseErrors false")
        await log(f"Couldn't list quotes for server {ctx.guild.name} ({ctx.guild.id}): {type(e)}: {e}", severity=logging.ERROR)

@commands.hybrid_command(
    name = "removequote",
)
@app_commands.describe(
    quote = "The quote to remove."
)
@viviatools.blockInDMs
@viviatools.adminOnly
async def removequote(ctx: commands.Context, quote: str):
    """
    Removes a quote from the custom quote list for the server it is run in.

    ## Args:
        - quote (str): The quote to remove.
    ## Notes:
        - Only users with bot permissions can use this command.
    """

    try:
        with open(os.path.join('data', 'servers', str(ctx.guild.id), 'quotes.json')) as f:
            quotes = json.load(f)
            if quote in quotes['quotes']:
                quotes['quotes'].remove(quote)
            else:
                await ctx.send("That quote isn't in the list, though...")
                return
        with open(os.path.join('data', 'quotes.json'), 'w') as f:
            json.dump(quotes, f)
    except Exception as e:
        await ctx.send(personalityMessage("errors.error"))
        if serverConfig(ctx.guild.id)['verboseErrors']:
            await ctx.send(f"{type(e)}: {e}\n-# To disable these messages, run /config verboseErrors false")
        await log(f'Failed to remove "{quote}" from the list for server {ctx.guild.name} ({ctx.guild.id}): {type(e)}: {e}', severity=logging.ERROR)
        return
    await ctx.send(f'"{quote}" was removed from the list.')
    await log(f"{ctx.author} removed \"{quote}\" from the list for server {ctx.guild.name} ({ctx.guild.id})", severity=logging.DEBUG)

@app_commands.context_menu(name="Add Custom Quote")
@viviatools.blockInDMs
@viviatools.adminOnly
async def contextmenu_addquote(interaction: discord.Interaction, message: discord.Message):
    add_custom_quote(f"\"{message.content}\" - {message.author.display_name}, {message.created_at.strftime('%Y-%m-%d')}", interaction.guild.id)
    await interaction.response.send_message(f"\"{message.content}\" - {message.author.display_name}, {message.created_at.strftime('%Y-%m-%d')} was added to the list.", ephemeral=True)
