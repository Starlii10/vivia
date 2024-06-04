# Vivia

A friendly companion for your Discord server.

## How to Run

You'll need to [create a Discord application](https://discord.com/developers/applications) first. Once that's done, you should get a token for the bot.
Clone this repo and place the token in a file named `token.env` in the root directory, like this:

`token="replace_with_your_token"`

Also modify any channel or user IDs in the Python code that you'd like to change.
Then simply invite the bot to a server, and in the root, run

`python bot.py`

This should start up the bot. If you specified a channel for an awake message, it'll send the message there.
