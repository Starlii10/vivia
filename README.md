# Vivia

A friendly companion for your Discord server.

## Add to Server

<https://discord.com/oauth2/authorize?client_id=1243029835790422116>

## How to Run

Vivia's code can be run locally to create your own personal instance of the bot.

You'll need to [create a Discord application](https://discord.com/developers/applications) first. Once that's done, you should get a token for the bot.
Clone this repo and place the token in a file named `token.env` in the root directory, like this:

`token="replace_with_your_token"`

Run `pip install -r requirements.txt` in the root to install dependencies. After that, run `python bot.py` to start up the bot.

For AI functionality, you'll want to install the `llama-cpp-python` package. Since the installation options can vary between computers, you should look at their [installation guide](https://github.com/abetlen/llama-cpp-python/blob/main/README.md#installation).

If you want Vivia to be able to read images via OCR, you will want the `pytesseract` package. This requires the Tesseract engine to already be installed on your computer.
