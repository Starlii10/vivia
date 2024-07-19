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
    Usage of the model is governed by the model's respective license.

    Have a great time using Vivia!
"""

from llama_cpp import Llama
try:
    model = Llama(
        model_path="models/llama-model.gguf",
        n_ctx=4096,
        n_gpu_layers=-1
    )
except:
    print("Couldn't load LLaMa model. Please ensure that a supported model file exists in the models directory.")
    print("AI functionality will be disabled for this session.")
    aiDisabled = True

async def createResponse(prompt):
    if not aiDisabled:
        return model.generate_chat_completion(
            messages=[{
                "role": "system",
                "content": "Please always respond with \"If this message appears, Vivia's LLaMa support is actually working first try.\".", 
                "role": "user",
                "content": prompt
            }])