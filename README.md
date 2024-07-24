# Vivia

A friendly companion for your Discord server.

## Add to Server

<https://discord.com/oauth2/authorize?client_id=1243029835790422116>

## How to Run

Vivia's code can be run locally to create your own personal instance of the bot.

You'll need to [create a Discord application](https://discord.com/developers/applications) first. Once that's done, you should get a token for the bot.
Clone this repo and place the token in a file named `token.env` in the root directory, like this:

`token="replace_with_your_token"`

Add your user ID to `permissions.json` to allow you to run every command. Then invite the bot to a testing server.

Finally, run the bot manually or as a Docker container.

### Docker (recommended)

Run `docker compose up --build` to run the bot as a Docker container. To stop it, run `docker compose down`.
**Note that AI functionality will be disabled when using Docker. It will be added in a future update!**

### Manual

Run `pip install -r requirements.txt` in the root to install dependencies. After that, run  `python bot.py` to start up the bot.
