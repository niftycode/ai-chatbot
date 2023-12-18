#!/usr/bin/env python3

"""
This program is inspired by an article from heise.de:
https://www.heise.de/ratgeber/Python-Eigene-KI-Programmierhilfe-entwickeln-9330993.html

In contrast to the code in the article, the new API (> 1.0.0) is used here.

Version: 2.0
Python 3.12
Date created: November 8th, 2023
Date modified: November 17th, 2023
"""

import tkinter as tk
import logging
import setup_ai as chatbot

from tkinter import ttk

# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)


class MainWindow:
    def __init__(self, window):
        self.window = window
        self.window.title("AI Chatbot (Python)")

        window_width = 600
        window_height = 400

        # Get the screen dimension
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Find the center point
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        # Set the position of the window to the center of the screen
        self.window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        # Window is not resizable
        self.window.resizable(False, False)

        # Create a frame
        # All widgets will be part of this frame.
        self.content = ttk.Frame(self.window, padding=(10, 10, 10, 10))

        # Add widgets
        self.text_area = tk.Text(self.content, bg="white")
        # self.text_area.pack()

        self.input_field = ttk.Entry(self.content)
        # self.input_field.pack()

        self.chat_button = ttk.Button(self.content, text="Chat", command=self.send_message)
        self.quit_button = ttk.Button(self.content, text="Quit", command=self.quit_program)

        # Define a grid (3 columns, 3 rows)
        self.content.grid(column=0, row=0, sticky="nsew")
        self.text_area.grid(column=0, row=1, columnspan=3, rowspan=1, sticky="nsew")
        self.input_field.grid(column=0, row=2, columnspan=3, rowspan=1, sticky="ew")
        self.chat_button.grid(column=0, row=3, columnspan=1, rowspan=1, sticky="w")
        self.quit_button.grid(column=2, row=3, columnspan=1, rowspan=1, sticky="e")

        # Note: We don't need columnconfigure(0, weight=1) or rowconfigure(0, weight=1)
        # because window.resizable is set to False.
    def send_message(self) -> None:
        """
        Get input from user, fetch answers and show them in a text field.
        """

        # Get input and delete the input field
        user_input = self.input_field.get()
        self.input_field.delete(0, "end")

        # Show the input in the text field
        self.text_area.insert("end", f"You: {user_input}\n")
        self.text_area.insert("end", "\n")
        chatbot.collect_input(user_input)

        # Fetch the answer
        response = chatbot.get_completion_from_messages(chatbot.context)
        chatbot.collect_responses(response)

        logging.debug(response)

        # Show the answer in the text field
        self.text_area.insert("end", f"Chatbot: {response}\n")
        self.text_area.insert("end", "\n \n")

    def quit_program(self):
        self.window.destroy()

    def mainloop(self):
        self.window.mainloop()

# input_field.bind_all("<Return>", send_message)


if __name__ == "__main__":
    window = tk.Tk()
    main_window = MainWindow(window)
    main_window.mainloop()
