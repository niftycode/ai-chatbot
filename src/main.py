#!/usr/bin/env python3

"""
This program is inspired by an article from heise.de (german language):
https://www.heise.de/ratgeber/Python-Eigene-KI-Programmierhilfe-entwickeln-9330993.html

In contrast to the code in the article, the new API (> 1.0.0) is used here.

Version: 3.0
Python 3.12+
Date created: November 8th, 2023
Date modified: November 14th, 2024
"""

import tkinter as tk
import logging

from src import setup_ai
from tkinter import ttk

logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.INFO)


class MainWindow:
    def __init__(self, app_window):
        self.window = app_window
        self.window.title("AI Chatbot (Python)")
        self.window.lift()

        window_width = 800
        window_height = 600

        # Get the screen dimension
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Find the center point
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        # Set the position of the window to the center of the screen
        self.window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        # Window is resizable?
        self.window.resizable(True, True)

        # Create a frame for the Text widget
        self.text_frame = ttk.Frame(self.window, padding=(10, 10, 10, 10))
        self.text_frame.grid(row=0, column=0, sticky="nsew")

        # Add a Text widget to the frame
        self.text_widget = tk.Text(self.text_frame, height=15, font=("Helvetica", 16))
        self.text_widget.grid(row=0, column=0, sticky="nsew")

        # Create a frame for an input field
        self.input_frame = ttk.Frame(window)
        self.input_frame.grid(row=1, column=0, sticky="ew")

        # Add entry widget to the input_frame
        self.input_field = ttk.Entry(
            self.input_frame, foreground="blue", background="white"
        )
        self.input_field.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.input_field.bind("<Return>", self.on_shortcut)

        # Create a frame for buttons
        self.button_frame = ttk.Frame(window)
        self.button_frame.grid(row=2, column=0, sticky="ew")

        # Add buttons to the button_frame
        self.chat_button = ttk.Button(
            self.button_frame, text="Chat", command=self.send_message
        )
        self.chat_button.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        self.quit_button = ttk.Button(
            self.button_frame, text="Quit", command=self.quit_program
        )
        self.quit_button.grid(row=0, column=2, sticky="e", padx=10, pady=10)

        # Configure grid to ensure the Text widget and button_frame fill the window
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.text_frame.grid_rowconfigure(0, weight=1)
        self.text_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)

    def on_shortcut(self, event):
        logging.debug("Enter key pressed")

    def send_message(self) -> None:
        """
        Get input from user, fetch answers and show them in a text field.
        """

        # Get input and delete the input field
        user_input = self.input_field.get()
        self.input_field.delete(0, "end")

        # Show the input in the text field
        self.text_widget.insert("end", f"You: {user_input}\n")
        self.text_widget.insert("end", "\n")
        setup_ai.collect_input(user_input)

        # Fetch the answer
        response = setup_ai.get_completion_from_messages(setup_ai.context)
        setup_ai.collect_responses(response)

        logging.debug(response)

        # Show the answer in the text field
        self.text_widget.insert("end", f"Chatbot: {response}\n")
        self.text_widget.insert("end", "\n \n")

    def quit_program(self):
        self.window.destroy()

    def mainloop(self):
        self.window.mainloop()


if __name__ == "__main__":
    window = tk.Tk()
    main_window = MainWindow(window)
    main_window.mainloop()
