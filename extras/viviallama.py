#!/usr/bin/env python

"""
    This is a wrapper for LLaMa used in Vivia.

    Vivia is licensed under the MIT License. For more information, see the LICENSE file.
    TL:DR: you can use Vivia's code as long as you keep the original license intact.
    Vivia is made open source in the hopes that you'll find her code useful.

    If you'd like to contribute, please check out the GitHub repository at https://github.com/starlii10/vivia.

    This uses the llama-cpp-python package, licensed under the MIT License. This is not a required dependency for Vivia.
    For more information, see their LICENSE file at https://github.com/abetlen/llama-cpp-python/blob/main/LICENSE.md.
    Note that you should compile it according to the hardware you're running Vivia on for maximum performance.
    For more info, see https://github.com/abetlen/llama-cpp-python?tab=readme-ov-file#are-there-pre-built-binaries--binary-wheels-available

    This uses a LLaMa model in models/llama-model.gguf, which can be changed by the user.
    Vivia does not provide a default model. Please ensure that a supported model file exists in the models directory.
    Usage of a model is governed by that model's respective license.   

    Have a great time using Vivia!
"""

import json
import mimetypes
import os
import sys
import traceback
import discord
import requests

print("Attempting to load LLaMa - this may take a moment")

aiDisabled = False
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
                print(f"Downloading {attachment.filename}...")
                # Download attachment
                try:
                    await attachment.save(f"data/tempchats/{internal_name}/{attachment.filename}")
                except Exception as e:
                    print(f"Error downloading {attachment.filename}. Ignoring.\n{type(e)}: {e}")
                    additional_messages.append({"role": "user", "content": f"An attachment that failed to download."})
                    continue
                print(f"Downloaded {attachment.filename}.")

                # Check if the attachment is text
                if mimetypes.guess_type(f"data/tempchats/{internal_name}/{attachment.filename}")[0].startswith("text"):
                    print(f"Attachment {attachment.filename} is text")
                    with open(f"data/tempchats/{internal_name}/{attachment.filename}", "r") as file:
                        additional_messages.append({"role": "user", "content": "An attached text file: " + file.read()})
                        print(f"Attachment {attachment.filename} has been processed.")
                else:
                    # TODO: OCR for images
                    print(f"Attachment {attachment.filename} is not text. Skipping.")
                    


        # Combine the additional messages with the system prompt and user prompt
        generation = model.create_chat_completion(messages=additional_messages + [
            {"role": "system", "content": open("data/system-prompt.txt", "r").read().replace("{username}", username)},
        ] + [{"role": "user", "content": prompt}])
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

