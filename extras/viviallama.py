#!/usr/bin/env python

"""
    This is a wrapper for LLaMa used in Vivia.

    Vivia is licensed under the MIT License. For more information, see the LICENSE file.
    TL:DR: you can use Vivia's code as long as you keep the original license intact.
    Vivia is made open source in the hopes that you'll find her code useful.

    If you'd like to contribute, please check out the GitHub repository at https://github.com/starlii10/vivia.

    This uses the llama-cpp-python package, licensed under the MIT License. This is not a required dependency for Vivia.
    Note that you should compile it according to the hardware you're running Vivia on for maximum performance.
    For more info, see https://github.com/abetlen/llama-cpp-python?tab=readme-ov-file#are-there-pre-built-binaries--binary-wheels-available

    This uses a LLaMa model in models/llama-model.gguf, which can be changed by the user.
    Vivia does not provide a default model. Please ensure that a supported model file exists in the models directory.
    Usage of a model is governed by that model's respective license.

    OCR is provided by pytesseract, licensed under the Apache License 2.0. This is not a required dependency for Vivia.
    For more information, see their LICENSE file at https://github.com/madmaze/pytesseract/blob/master/LICENSE.
    You must install the tesseract-ocr package to use it, otherwise Vivia will not be able to read images.

    Have a great time using Vivia!
"""

import json
import mimetypes
import os
import sys
from PIL import Image
import traceback
import discord
import numpy as np
import requests

print("Attempting to load LLaMa - this may take a moment")

# Variable initialization
aiDisabled = False
imageReadingDisabled = False
attachment_messages = []

# Delete tempchats folder if it exists
if os.path.exists("data/tempchats"):
    # Just like the terminal title, VSCode hates when I do it like this. Too bad, I can't write cross-platform code very well
    if sys.platform == "win32":
        os.system("rmdir /S /Q data/tempchats")  # Windows
    else:
        os.system("rm -rf data/tempchats")  # Linux/Unix/Mac/Insert-Non-Windows-OS-Here

# Load LLaMa
try:
    from llama_cpp import Llama
except:
    print("Couldn't load llama-cpp-python. This is not a fatal error, however Vivia will not be able to generate responses unless it is installed.", file=sys.stderr)
    print("Please install it according to their installation guide. See https://github.com/abetlen/llama-cpp-python/blob/main/README.md#installation.", file=sys.stderr)
    aiDisabled = True
else:
    try:
        model = Llama(
            model_path="extras/models/llama-model.gguf",
            n_ctx=0,
            n_gpu_layers=-1
        )
    except Exception as e:
        print(f"Couldn't load LLaMa model. This can be caused by an invalid model path, no supported devices to run LLaMa on, or an error in the model.", file=sys.stderr)
        print("This is not a fatal error, however Vivia will not be able to generate responses unless it is installed.", file=sys.stderr)
        print(f"{type(e)}: {e}\n{traceback.format_exc()}", file=sys.stderr)
        aiDisabled = True

# Load pytesseract
try:
    import pytesseract
except:
    print("Couldn't load pytesseract. This is not a fatal error, however Vivia will not be able to read images unless it is installed.", file=sys.stderr)
    imageReadingDisabled = True

async def createResponse(prompt: str, username: str, internal_name: str, attachments: list[discord.Attachment] = []):
    if not aiDisabled:
        print(f"Response generation requested by {internal_name} ({username}) - generating now! (This may take a moment)")

        # Read messages from memory file
        if not os.path.exists(f"data/tempchats/{internal_name}/messages.txt"):
            os.makedirs(f"data/tempchats/{internal_name}")
            with open(f"data/tempchats/{internal_name}/messages.txt", "w") as file:
                json.dump([], file)
        with open(f"data/tempchats/{internal_name}/messages.txt", "r") as file:
            additional_messages = json.load(file)

        # Read message attachments
        if len(attachments) > 0:
            print("Reading message attachments...")
            for attachment in attachments:
                attachment_messages.append(await processAttachment(attachment, internal_name))
            print("Attachments read.")

        # Combine the additional messages with the system prompt and user prompt
        generation = model.create_chat_completion(messages=additional_messages + [
            {"role": "system", "content": open("data/system-prompt.txt", "r").read().replace("{username}", username)},
        ] + [{"role": "user", "content": prompt}] + [{"role": "user", "content": attachment_messages}])
        response = generation['choices'][0]['message']['content']
        print("Response generated successfully.")

        # Write messages to memory file
        with open(f"data/tempchats/{internal_name}/messages.txt", "w") as file:
            json.dump(additional_messages + [{"role": "user", "content": prompt}] + [{"role": "assistant", "content": f"{response}"}], file)
        
        return response
    else:
        # Return an error message if LLaMa failed to load
        print(f"Ignoring generation request by {internal_name} ({username}) due to previous errors while loading LLaMa", file=sys.stderr)
        return("Something's wrong with my programming, so I can't respond. Sorry.")

async def processAttachment(attachment, internal_name):
    # Download attachment
    try:
        await attachment.save(f"data/tempchats/{internal_name}/{attachment.filename}")
    except Exception as e:
        print(f"Error downloading {attachment.filename}. Ignoring.\n{type(e)}: {e}")
        return {"role": "user", "content": f"An attachment that failed to download."}

    # Check if the attachment is text
    match mimetypes.guess_type(f"data/tempchats/{internal_name}/{attachment.filename}")[0].split("/")[0]:
        case "text":
            with open(f"data/tempchats/{internal_name}/{attachment.filename}", "r") as file:
                return {"role": "user", "content": "An attached text file: " + file.read()}
        case "image":
            # Attempt OCR on the attachment
            if not imageReadingDisabled:
                print(f"Attachment {attachment.filename} is not text. Attempting OCR...")
                try:
                    img = np.array(Image.open(f"data/tempchats/{internal_name}/{attachment.filename}"))
                    text = pytesseract.image_to_string(f"data/tempchats/{internal_name}/{attachment.filename}")
                    if text:
                        print(f"Found text in {attachment.filename}: {text}")
                        return {"role": "user", "content": "An attached image with the text: " + text}
                    else:
                        print(f"Couldn't find text in {attachment.filename}. Skipping.")
                        return {"role": "user", "content": f"An image that couldn't be read: {attachment.filename}"}
                except Exception as e:
                    print(f"Error performing OCR on {attachment.filename}. Skipping.\n{type(e)}: {e}", file=sys.stderr)
                    return {"role": "user", "content": f"An image that couldn't be read due to errors: {attachment.filename}"}
            else:
                print(f"Attachment {attachment.filename} is not text. Skipping OCR due to previous errors loading pytesseract.", file=sys.stderr)
                return {"role": "user", "content": f"An image that couldn't be read due to errors: {attachment.filename}"}
        case _:
            print(f"Attachment {attachment.filename} is unrecognized. Skipping.")
            return {"role": "user", "content": f"An unrecognized attachment: {attachment.filename}"}