#!/usr/bin/env python3

"""
Description goes here...
Version: 1.0
Python 3.11
Date created: October 18th, 2023
Date modified: November 10th, 2023
"""

import openai
import io
import logging

from os.path import expanduser


logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.INFO)

api_file_path = expanduser("~") + "/Documents/API/openai-api-file.bin"

with open(api_file_path, encoding="utf-8") as binary_file:
    # Read the whole file at once
    api_key = binary_file.read()

logging.debug(str(api_key))

'''
prompt = "Can you write a function in Python to perform the addition of two numbers?"

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


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,  # Differenziertheit der Antwort (1 = hoch)
    )
    return response.choices[0].message["content"]  # type: ignore
'''