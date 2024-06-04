# this is a whole hecking lot of imports, and yes, every single one is used

import sys
import discord
from discord.ext import tasks, commands
import requests
import json
from datetime import datetime
import dotenv
import random
from os import system
import configparser
import logging
config = configparser.ConfigParser()

try:
    config.read("config.ini")
except:
    try:
        print("config.ini not found, creating new from default. If this is the first run please ignore this message")
        config.read("config.ini.example")
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    except:
        print("config.ini.example not found or couldn't be read")
        sys.exit(1)
else:
    print("config.ini found, loading it")


handler = logging.FileHandler(
    filename=config['Logging']['Filename'],
    encoding='utf-8',
    mode='w'
)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logging.basicConfig(level=logging.INFO)

system("title Navolt's Testing Bot")




intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='ntb!', intents=intents)
bot.remove_command("help")
tree = bot.tree

helpMsg = open("helpmsg.txt", "r").read()

@bot.event
async def on_ready():
    """
    Function called when the bot starts up
    """
    await log(f'Logged in as {bot.user}')

    # Start Jelo live pings
    if config['General']['LivePingsEnabled'] == "True":
        check_and_notify.start()

    # Send awake message
    if config['General']['AwakeMessageEnabled'] == "True":
        awake_channel = bot.get_channel(1246216252276477962) # Awake channel
        await awake_channel.send("I'm awake! <:jb_yay:1246215956355878993>\n\n" + datetime.now().strftime("%H:%M:%S" + " UTC"))
    
    # Change status
    await bot.change_presence(activity=discord.CustomActivity(name='ntb!help | ' + config['General']['StatusMessage']))

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

    # Process commands
    await bot.process_commands(message)

    if message.author == bot.user:
        return
    if "regina" in message.content:
        await message.channel.send("\"BRO, STOP CALLING US YOU DONT EVEN WORK HERE?\"\n\nbut really RC is great")

@tree.command(
    name="quote",
    description="Say a random quote."
)
async def quote(interaction):
    with open('quotes.json') as f:
        quotes = json.load(f)
        quote = random.choice(quotes['quotes'])
        await interaction.response.send(quote)

@bot.command()
async def GetStarliisAttention(ctx):
    await log("STARLII!!!")
    await ctx.send("<@1141181390445101176>")

@bot.command()
async def awoofy(ctx):
    await ctx.send("Awoofy mentioned <:jb_yay:1246215956355878993>")

async def log(message, severity=logging.INFO):
    """
    Outputs a message to the log.

    Args:
        message (str): The message to output.
        severity (int): The severity of the message (defaults to Info).

    Notes:
        This function will output to the console, log file, and to a Discord channel.
    """
    print(message)
    await bot.get_channel(1246546976124965015).send(message)
    logging.log(severity, message)

@bot.command()
async def help(ctx):
    await ctx.author.send(helpMsg)
    await ctx.send(f"Check your DMs {ctx.author.mention}")

@bot.command()
async def livePings(ctx):
    # turn on/off live pings (persistent)
    if config['General']['LivePingsEnabled'] == "True":
        config['General']['LivePingsEnabled'] = "False"
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        check_and_notify.cancel()
        await log("Live pings are now off")
        await ctx.send("Live pings are now off")
    else:
        config['General']['LivePingsEnabled'] = "True"
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        check_and_notify.start()
        await log("Live pings are now on")
        await ctx.send("Live pings are now on")

@bot.command()
async def awakeMessage(ctx):
    # turn on/off awake message (persistent)
    if config['General']['AwakeMessageEnabled'] == "True":
        config['General']['AwakeMessageEnabled'] = "False"
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        check_and_notify.cancel()
        await log("Awake message is now off")
        await ctx.send("Awake message is now off")
    else:
        config['General']['AwakeMessageEnabled'] = "True"
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        check_and_notify.start()
        await log("Awake message is now on")
        await ctx.send("Awake message is now on")

@tasks.loop(seconds=10)
async def check_and_notify():
    """
        Sends a message to a channel if the specified Twitch channel is live.
    """

    # todo: allow for multiple Twitch channels

    check_and_notify.has_sent_message = getattr(check_and_notify, 'has_sent_message', False)
    
    if await get_twitch_live('jeloetta'): # Replace "jeloetta" with any Twitch channel name
        if not check_and_notify.has_sent_message:
            await log("I'M DOING A DENUO!")
            channel = bot.get_channel(1243032295481282657)  # Replace with your channel ID
            await channel.send("Hey @everyone, [Jeloetta](https://twitch.tv/jeloetta) is streaming " + requests.get("https://decapi.me/twitch/game/jeloetta").text + "! They'd be delighted to hang out with you!")
            # We've sent the message, set the flag
            check_and_notify.has_sent_message = True
    else:
        # Channel went offline, reset the flag
        check_and_notify.has_sent_message = False

# Gets the live status of the specified Twitch channel
async def get_twitch_live(channelName):
    """
    Retrieves the live status of a Twitch channel.

    Args:
        channelName (str): The name of the Twitch channel.

    Returns:
        bool: True if the channel is live, False otherwise. Returns False if an error occurs.

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
            await log("Error: " + str(result.status_code), file=sys.stderr)
            return False
    except Exception as e:
        await log("Error: " + str(e), file=sys.stderr)
        return False

# Gets info about the specified Twitch channel (returns JSON)
async def get_stream_info(channelName):
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
            await log("Couldn't get game: " + str(game.status_code), file=sys.stderr)
            game = "Couldn't get game: " + str(game.status_code)

        title = requests.get("https://decapi.me/twitch/title/" + channelName)
        if title.ok:
            title = title.text
        else:
            await log("Couldn't get title: " + str(title.status_code), file=sys.stderr)
            title = "Couldn't get title: " + str(title.status_code)

        viewers = requests.get("https://decapi.me/twitch/viewercount/" + channelName)
        if viewers.ok:
            viewers = viewers.text
        else:
            await log("Couldn't get viewers: " + str(viewers.status_code), file=sys.stderr)
            viewers = "Couldn't get viewers: " + str(viewers.status_code)
            
        uptime = requests.get("https://decapi.me/twitch/uptime/" + channelName)
        if uptime.ok:
            uptime = uptime.text
        else:
            await log("Couldn't get uptime: " + str(uptime.status_code), file=sys.stderr)
            uptime = "Couldn't get uptime: " + str(uptime.status_code)

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
        await log("Error: " + str(e), file=sys.stderr)
        return "Error: " + str(e)

@bot.command()
async def sync(ctx):
    if ctx.author.id == 1141181390445101176:
        await bot.tree.sync()
        await log("Command tree synced")
    else:
        await ctx.send('You do not have permission to use this command.', ephemeral=True)

def has_bot_permissions(user):
    with open('permissions.json') as f:
        users = json.load(f)
    return user.id in users

bot.run(dotenv.get_key("token.env", "token"), log_handler=handler)
