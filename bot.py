import discord
from discord.ext import tasks, commands
import requests
import sys
import json
from datetime import datetime
import dotenv
import random

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    """
    Function called when the bot starts up
    """
    print(f'Logged in as {bot.user}')
    # Start the check
    check_and_notify.start()

    # Send awake message
    awake_channel = bot.get_channel(1246216252276477962) # Awake channel
    await awake_channel.send("I'm awake! <:jb_yay:1246215956355878993>\n\n" + datetime.now().strftime("%H:%M:%S" + " UTC"))
    
    # say whatever here
    # await bot.get_channel(1243032295481282657).send("yes")

@bot.event
async def on_member_join(member):
    """
    Function called when a member joins the server
    """
    welcome_channel = bot.get_channel(1246532114266980433) # Welcome channel
    await welcome_channel.send(member.mention + ", welcome")

@bot.event
async def on_message(message):
    """
    Function called when a message is sent
    """
    if message.author == bot.user:
        return
    if "regina" in message.content:
        await message.channel.send("\"BRO, STOP CALLING US YOU DONT EVEN WORK HERE?\"\n\nbut really RC is great")
        await message.pin()

@bot.command()
async def WakeUp(ctx):
    print("Someone tried to wake me up... but I'm already awake!")
    await ctx.send("But I'm already awake!")

@bot.command()
async def quote(ctx):
    with open('quotes.json') as f:
        quotes = json.load(f)
        quote = random.choice(quotes['quotes'])
        print(quote)
        await ctx.send(quote)

@bot.command()
async def GetStarliisAttention(ctx):
    print("STARLII!!!")
    await ctx.send("<@1141181390445101176>")

@bot.command()
async def awoofy(ctx):
    await ctx.send("Awoofy mentioned <:jb_yay:1246215956355878993>")

@tasks.loop(seconds=10)
async def check_and_notify():
    """
        Sends a message to a channel if the specified Twitch channel is live.
    """

    # todo: allow for multiple Twitch channels

    check_and_notify.has_sent_message = getattr(check_and_notify, 'has_sent_message', False)
    
    if get_twitch_live('jeloetta'): # Replace "jeloetta" with any Twitch channel name
        if not check_and_notify.has_sent_message:
            channel = bot.get_channel(1243032295481282657)  # Replace with your channel ID
            await channel.send("Hey @everyone, [Jeloetta](https://twitch.tv/jeloetta) is streaming " + requests.get("https://decapi.me/twitch/game/jeloetta").text + "! They'd be delighted to hang out with you!")
            # We've sent the message, set the flag
            check_and_notify.has_sent_message = True
    else:
        # Channel went offline, reset the flag
        check_and_notify.has_sent_message = False

# Gets the live status of the specified Twitch channel
def get_twitch_live(channelName):
    """
    Retrieves the live status of a Twitch channel.

    Args:
        channelName (str): The name of the Twitch channel.

    Returns:
        bool: True if the channel is live, False otherwise or if an error occurs.

    Notes:
        This function uses decapi.me to access the Twitch API.
    """
    try:
        result = requests.get("https://decapi.me/twitch/uptime/" + channelName)
        if(result.ok):
            if ("offline" in result.text):
                return False
            else:
                return True
        else:
            print("Error: " + str(result.status_code), file=sys.stderr)
            return False
    except Exception as e:
        print("Error: " + str(e), file=sys.stderr)
        return False

# Gets info about the specified Twitch channel (returns JSON)
def get_stream_info(channelName):
    """
    Retrieves information about a Twitch stream.

    Args:
        channelName (str): The name of the Twitch channel.

    Returns:
        str: A JSON string containing the stream information. If an error occurs, 
             the string will contain an error message.
    """
    try:
        # Get the stream info
        channel = channelName

        game = requests.get("https://decapi.me/twitch/game/" + channelName)
        if game.ok:
            game = game.text
        else:
            print("Error: " + str(game.status_code), file=sys.stderr)
            game = "Error: " + str(game.status_code)

        title = requests.get("https://decapi.me/twitch/title/" + channelName)
        if title.ok:
            title = title.text
        else:
            print("Error: " + str(title.status_code), file=sys.stderr)
            title = "Error: " + str(title.status_code)

        viewers = requests.get("https://decapi.me/twitch/viewercount/" + channelName)
        if viewers.ok:
            viewers = viewers.text
        else:
            print("Error: " + str(viewers.status_code), file=sys.stderr)
            viewers = "Error: " + str(viewers.status_code)
            
        uptime = requests.get("https://decapi.me/twitch/uptime/" + channelName)
        if uptime.ok:
            uptime = uptime.text
        else:
            print("Error: " + str(uptime.status_code), file=sys.stderr)
            uptime = "Error: " + str(uptime.status_code)

        # Create a dictionary
        stream_info = {
            "channel": channel,
            "game": game,
            "title": title,
            "viewers": viewers,
            "uptime": uptime
        }

        # Convert the dictionary to JSON
        json_data = json.dumps(stream_info)
        return json_data
    
    except Exception as e:
        print("Error: " + str(e), file=sys.stderr)
        return "Error: " + str(e)

bot.run(dotenv.get_key("token.env", "token"))
