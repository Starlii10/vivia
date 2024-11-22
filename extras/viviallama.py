#!/usr/bin/env python

"""
    A wrapper for llama-cpp, powering Vivia's AI functionality.

    Vivia is licensed under the MIT License. For more information, see the LICENSE file.
    TL:DR: you can use Vivia's code as long as you keep the original license intact.
    Vivia is made open source in the hopes that you'll find her code useful.

    If you'd like to contribute, please check out the GitHub repository at https://github.com/starlii10/vivia.

    This uses the llama-cpp-python package, licensed under the MIT License. This is not a required dependency for Vivia.
    Note that you should compile it according to the hardware you're running Vivia on for maximum performance.
    For more info, see https://github.com/abetlen/llama-cpp-python?tab=readme-ov-file#are-there-pre-built-binaries--binary-wheels-available

    This uses a LLaMa model in extras/models/llama-model.gguf, which can be changed by the user.
    Vivia does not provide a default model. Please ensure that a supported model file exists in the models directory.
    Usage of a model is governed by that model's respective license.

    OCR is provided by pytesseract, licensed under the Apache License 2.0. This is not a required dependency for Vivia.
    For more information, see their LICENSE file at https://github.com/madmaze/pytesseract/blob/master/LICENSE.
    You must install the external tesseract-ocr package, otherwise Vivia will not be able to utilize pytesseract.

    Have a great time using Vivia!
"""

import configparser
import json
import logging
import mimetypes
import os
import shutil
import sys
import traceback
from PIL import Image
import cv2
import discord
import numpy as np

if __name__ == "__main__":
    print("This is a helper script for Vivia that should not be run directly.", sys.stderr)
    print("To run Vivia, please use \"python bot.py\" in the root directory.", sys.stderr)
    sys.exit(1)

from extras import viviatools
from extras.viviatools import personalityMessage

viviatools.log("Attempting to load LLaMa - this may take a moment", logging.INFO)

# Variable initialization
aiDisabled = False
imageReadingDisabled = False
attachment_messages = []

# Config loading
config = configparser.ConfigParser()
config.read("config.ini")

# Delete tempchats folder if it exists
if os.path.exists("data/tempchats"):
    shutil.rmtree("data/tempchats")
    viviatools.log("Deleted temporary chat files", logging.DEBUG)

# Load LLaMa
try:
    from llama_cpp import Llama
except:
    viviatools.log("Couldn't load llama-cpp-python. This is not a fatal error, however Vivia will not be able to generate responses unless it is installed.", logging.ERROR)
    viviatools.log("Please install it according to their installation guide. See https://github.com/abetlen/llama-cpp-python/blob/main/README.md#installation.", logging.ERROR)
    viviatools.log("AI functionality will be disabled for this session.", logging.ERROR)
    aiDisabled = True
else:
    try:
        model = Llama(
            model_path="extras/models/llama-model.gguf",
            n_ctx=0,
            n_gpu_layers=-1
        )
    except Exception as e:
        viviatools.log(f"Couldn't load LLaMa model. This can be caused by an invalid model path, no supported devices to run LLaMa on, or an error in the model.", logging.ERROR)
        viviatools.log("This is not a fatal error, however Vivia will not be able to generate responses unless it is installed.", logging.ERROR)
        viviatools.log("Please ensure that a supported model file exists in the models directory, and that LLaMa is installed correctly.", logging.ERROR)
        viviatools.log("AI functionality will be disabled for this session.", logging.ERROR)
        viviatools.log("".join(traceback.format_exception(e)), logging.ERROR)
        aiDisabled = True

# Load pytesseract
try:
    import pytesseract
except:
    viviatools.log("Couldn't load pytesseract. This is not a fatal error, however Vivia will not be able to read images unless it is installed.", logging.ERROR)
    viviatools.log("This may be caused by the missing tesseract-ocr package. Pytesseract requires tesseract-ocr, which does not come with the package and must be installed manually.", logging.ERROR)
    viviatools.log("Ensure both pytesseract and tesseract-ocr are installed.")
    viviatools.log("OCR functionality will be disabled for this session.", logging.ERROR)
    imageReadingDisabled = True

async def createResponse(
        prompt: str,
        username: str,
        internal_name: str,
        attachments: list[discord.Attachment] = [],
        user_status: str | None = None,
        current_status: str | None = None,
        server_name: str | None = None,
        channel_name: str | None = None,
        category_name: str | None = None):
    if not aiDisabled:
        viviatools.log(f"Response generation requested by {internal_name} ({username}) - generating now! (This may take a moment)", logging.DEBUG)

        # Read messages from memory file
        memory_file_path = os.path.join("data", "tempchats", internal_name, "messages.txt")
        if not os.path.exists(memory_file_path):
            os.makedirs(os.path.dirname(memory_file_path))
            with open(memory_file_path, "w") as file:
                json.dump([], file)
        additional_messages = json.load(open(memory_file_path, "r"))

        # Read message attachments
        if len(attachments) > 0:
            viviatools.log("Reading message attachments...", logging.DEBUG)
            for attachment in attachments:
                attachment_messages.append(await processAttachment(attachment, internal_name))
            viviatools.log("Attachments read.", logging.DEBUG)

        # Sysprompt processing. Terrible, ik. Too bad!
        sysprompt = [{"role": "system", "content": {
            add_info_to_sysprompt(open(os.path.join("data", "system-prompt.txt"), "r").read(), 
                                  internal_name, 
                                  username, 
                                  user_status, 
                                  current_status, 
                                  server_name, 
                                  channel_name, 
                                  category_name)}}]

        # Combine the additional messages with the system prompt and user prompt
        generation = model.create_chat_completion(messages=additional_messages + sysprompt +
                                                  [{"role": "user", "content": prompt}] + [{"role": "user", "content": attachment_messages}])
        response = generation['choices'][0]['message']['content']
        viviatools.log(f"Response generated successfully for user {internal_name} ({username}).", logging.DEBUG)
        
        # Write messages to memory file
        with open(os.path.join("data", "tempchats", internal_name, "messages.txt"), "w") as file:
            json.dump(additional_messages + [{"role": "user", "content": prompt}] + [{"role": "assistant", "content": f"{response}"}], file)

        return response
    else:
        # Return an error message if LLaMa failed to load
        viviatools.log(f"Ignoring generation request by {internal_name} ({username}) due to previous errors while loading LLaMa", logging.WARNING)
        return(personalityMessage("ai.cannotrespond"))

async def processAttachment(attachment, internal_name):
    # Download attachment
    try:
        viviatools.log(f"Downloading {attachment.filename}", logging.DEBUG)
        await attachment.save(os.path.join("data", "tempchats", internal_name, attachment.filename))
    except Exception as e:
        viviatools.log(f"Error downloading {attachment.filename}. Ignoring.\n{str(type(e))}: {e}", logging.WARNING)
        return {"role": "user", "content": f"An attachment that failed to download: {attachment.filename}"}

    # Check if the attachment is text
    match mimetypes.guess_type(os.path.join("data", "tempchats", internal_name, attachment.filename))[0].split("/")[0]:
        case "text":
            with open(os.path.join("data", "tempchats", internal_name, attachment.filename), "r") as file:
                viviatools.log(f"Attachment {attachment.filename} read as text", logging.DEBUG)
                return {"role": "user", "content": f"An attached text file: {attachment.filename}:\n{file.read()}"}
        case "image":
            # Attempt OCR on the attachment
            if not imageReadingDisabled:
                viviatools.log(f"Attachment {attachment.filename} is not text. Attempting OCR...", logging.DEBUG)
                try:
                    # Load image
                    img = np.array(Image.open(os.path.join("data", "tempchats", internal_name, attachment.filename)))
                    
                    # Process image
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                    noise_reduced = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
                    
                    # DEBUG - Save image
                    if config["Advanced"]["Debug"] == "True":
                        cv2.imwrite(os.path.join("extras", "ocr", attachment.filename), noise_reduced)
                        viviatools.log(f"Debug: Saved processed image {attachment.filename} to extras/ocr", logging.DEBUG)
                    
                    # Perform OCR
                    text = pytesseract.image_to_string(noise_reduced)
                    if text:
                        viviatools.log(f"Found text in {attachment.filename}: {text}", logging.DEBUG)
                        return {"role": "user", "content": f"An attached image ({attachment.filename}) with the text: {text}"}
                    else:
                        # OCR returned no text
                        viviatools.log(f"Couldn't find text in {attachment.filename}. Skipping.", logging.DEBUG)
                        return {"role": "user", "content": f"An image that couldn't be read: {attachment.filename}"}
                except Exception as e:
                    # OCR failed
                    viviatools.log(f"Error performing OCR on {attachment.filename}. Skipping.\n{str(type(e))}: {e}", logging.ERROR)
                    return {"role": "user", "content": f"An image ({attachment.filename}) that couldn't be read due to errors"}
            else:
                # Pytesseract didn't load, skip
                viviatools.log(f"Attachment {attachment.filename} is not text. Skipping OCR due to previous errors loading pytesseract.", logging.WARNING)
                return {"role": "user", "content": f"An image ({attachment.filename}) that couldn't be read due to errors"}
        case _:
            # Unrecognized attachment type
            viviatools.log(f"Attachment {attachment.filename} is unrecognized. Skipping.", logging.WARNING)
            return {"role": "user", "content": f"An unrecognized attachment ({attachment.filename})"}

def add_info_to_sysprompt(sysprompt, internal_name, username, discord_status_user, status_bot, server_name, channel_name, category_name):
    # This is a TERRIBLE way to do this. I know
    sysprompt = sysprompt.replace("{username}", username)
    sysprompt = sysprompt.replace("{discord_status_user}", discord_status_user)
    sysprompt = sysprompt.replace("{status_bot}", status_bot)
    sysprompt = sysprompt.replace("{server_name}", server_name)
    sysprompt = sysprompt.replace("{channel_name}", channel_name)
    sysprompt = sysprompt.replace("{category_name}", category_name)
    sysprompt = sysprompt.replace("{internal_name}", internal_name)
    return sysprompt