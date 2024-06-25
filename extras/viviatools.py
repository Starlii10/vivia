#!/usr/bin/env python

"""
    This script is part of Vivia.

    Vivia is licensed under the MIT License. For more information, see the LICENSE file.
    TL:DR: you can use Vivia's code as long as you keep the original license intact.
    Vivia is made open source in the hopes that you'll find her code useful.

    If you'd like to contribute, please check out the GitHub repository at https://github.com/starlii10/vivia.

    Have a great time using Vivia!
"""

import json
import random

def generate_name(type, gender):
    """
    Generator for names.

    Args:
        type (str): The type of name to generate.
        gender (str): The gender of the name to generate.

    Returns:
        str: The generated name.

    Notes:
        - This function assumes that the names.json file is in the same directory as the script.
    """
    with open('names.json') as f:
        names = json.load(f)
        all_names = names['first']['male'] + names['first']['female']
        match type:
            case "first":
                match gender:
                    case "male":
                        return names['first']['male'][random.randint(0, len(names['first']['male']) - 1)]
                    case "female":
                        return names['first']['female'][random.randint(0, len(names['first']['female']) - 1)]
                    case _:
                        return all_names[random.randint(0, len(all_names) - 1)]
            case "middle":
                return names['middle'][random.randint(0, len(names['middle']) - 1)]
            case "last":
                return names['last'][random.randint(0, len(names['last']) - 1)]
            case "full":
                match gender:
                    case "male":
                        return names['first']['male'][random.randint(0, len(names['first']['male']) - 1)] + " "+ names['middle'][random.randint(0, len(names['middle']) - 1)] + " " + names['last'][random.randint(0, len(names['last']) - 1)]
                    case "female":
                        return names['first']['female'][random.randint(0, len(names['first']['female']) - 1)] + " "+ names['middle'][random.randint(0, len(names['middle']) - 1)] + " " + names['last'][random.randint(0, len(names['last']) - 1)]
                    case _:
                        return all_names[random.randint(0, len(all_names) - 1)] + " "+ names['middle'][random.randint(0, len(names['middle']) - 1)] + " " + names['last'][random.randint(0, len(names['last']) - 1)]
