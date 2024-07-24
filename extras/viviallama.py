#!/usr/bin/env python

"""
    This is a wrapper for LLaMa used in Vivia.

    Vivia is licensed under the MIT License. For more information, see the LICENSE file.
    TL:DR: you can use Vivia's code as long as you keep the original license intact.
    Vivia is made open source in the hopes that you'll find her code useful.

    If you'd like to contribute, please check out the GitHub repository at https://github.com/starlii10/vivia.

    This uses the llama-cpp-python package, licensed under the MIT License.
    For more information, see their LICENSE file at https://github.com/abetlen/llama-cpp-python/blob/main/LICENSE.md.

    This uses a LLaMa model in models/llama-model.gguf, which can be changed by the user.
    Vivia does not provide a default model. Please ensure that a supported model file exists in the models directory.
    Usage of a model is governed by that model's respective license.   

    Have a great time using Vivia!
"""

import json
import os

print("Attempting to load LLaMa - this may take a moment")

aiDisabled = False
# Delete tempchats folder if it exists
if os.path.exists("data/tempchats"):
    os.system("rm -rf data/tempchats")

try:
    from llama_cpp import Llama
except:
    print("Couldn't load llama-cpp-python. Make sure it's installed.")
    print("AI functionality will be disabled for this session.")
    aiDisabled = True
else:
    try:
        model = Llama(
            model_path="extras/models/llama-model.gguf",
            n_ctx=0,
            n_gpu_layers=-1
        )
    except Exception as e:
        print("Couldn't load LLaMa model. Please ensure that a supported model file exists in the models directory.")
        print("AI functionality will be disabled for this session.")
        print(e)
        aiDisabled = True

async def createResponse(prompt: str, username: str, internal_name: str):
    if not aiDisabled:
        print("Response generation requested - generating...")

        # Read messages from memory file
        if not os.path.exists(f"data/tempchats/{internal_name}/messages.txt"):
            os.makedirs(f"data/tempchats/{internal_name}")
            with open(f"data/tempchats/{internal_name}/messages.txt", "w") as file:
                json.dump([], file)
        with open(f"data/tempchats/{internal_name}/messages.txt", "r") as file:
            additional_messages = json.load(file)
        
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
        print("AI functionality is disabled for this session due to problems with LLaMa. Ignoring generation request.")
        return("Something's wrong with my programming, so I can't respond. Sorry.")