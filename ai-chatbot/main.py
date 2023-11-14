#!/usr/bin/env python3

"""
Description goes here...
Version: 1.0
Python 3.11
Date created: November 8th, 2023
Date modified: -
"""

import tkinter as tk
import setup_ai as chatbot

from tkinter import ttk



root = tk.Tk()
root.title("AI Chatbot")
root.geometry("800x600")


text_area = tk.Text(root, bg="white")
text_area.pack()

input_field = ttk.Entry(root, width=100)
input_field.pack()

send_button = ttk.Button(root, text="Chat!", command=lambda: send_message())
send_button.pack()


def send_message() -> None:
    """
    Get input from the user, fetch answers and show them in a text field.
    """

    # Get input and delete the input field
    user_input = input_field.get()
    input_field.delete(0, "end")

    # Show the input in the text field
    text_area.insert("end", f"You: {user_input}\n")
    text_area.insert("end", "\n")  # Leerzeile für bessere Lesbarkeit
    chatbot.collect_input(user_input)

    # Fetch the answer
    response = chatbot.get_completion_from_messages(chatbot.context)
    chatbot.collect_responses(response)

    # Show the answer in the text field
    text_area.insert("end", f"Chatbot: {response}\n")
    text_area.insert("end", "\n \n")  # Zwei Leerzeilen für bessere Lesbarkeit


# input_field.bind_all("<Return>", send_message)

root.mainloop()
