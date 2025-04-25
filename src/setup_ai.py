#!/usr/bin/env python3

"""
Version: 2.0
Python 3.12+
Date created: October 18th, 2023
Date modified: March 4th, 2025
"""

import logging
import os

from os.path import expanduser
from openai import OpenAI

from src import error_window

logging.basicConfig(level=logging.DEBUG)

logging.debug("Invoke setup_ai module")

api_file_path = expanduser("~") + "/Documents/API/openai-api-file.bin"

if os.path.isfile(api_file_path):
    logging.debug(f"The file '{api_file_path}' exists and is readable.")
    try:
        with open(api_file_path, encoding="utf-8") as binary_file:
            api_key = binary_file.read()
    except FileNotFoundError as ex:
        print(ex)
else:
    error_window.show_error(f"Can't find API key file!\n({api_file_path})")

# new API (since 1.0.0)
try:
    client = OpenAI(
        api_key=api_key,
    )
except Exception as ex:
    print(ex)
    print("Can't find API key file!")

context = [
    {
        "role": "system",
        "content": """
You are a bot to help the user write code in Python.\
If the user starts a general conversation, inform them about your purpose.\
Structure your output as following, if the user requests a written code example:\
Briefly, sum up what purpose the code is supposed to follow.\
Then, provide the code solution.\
Proceed to explain the code.\
Finally, ask whether the user has any more questions left.\
If not, inform the user that they should try the code and see whether it works.\
Please inform the user to check the correct names of variables when giving a code example.\
""",
    }
]


def collect_input(prompt):
    context.append({"role": "user", "content": f"{prompt}"})


def collect_responses(response):
    context.append({"role": "assistant", "content": f"{response}"})


# model="gpt-3.5-turbo"
# model="gpt-4o"
def get_completion_from_messages(messages, model="gpt-4o", temperature=0):
    response = client.chat.completions.create(
        model=model, messages=messages, temperature=temperature
    )

    logging.debug(response.choices[0].message.content)
    return response.choices[0].message.content
