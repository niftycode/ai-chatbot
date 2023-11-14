#!/usr/bin/env python3

"""
Tkinter GUI
Version: 1.0
Python 3.12
Date created: November 8th, 2023
Date modified: November 14th, 2023
"""

import tkinter as tk
import setup_ai as chatbot

from tkinter import ttk


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("AI Chatbot")
        self.geometry("800x600")

        # Create a frame
        # All widgets will be part of this frame.
        self.content = ttk.Frame()

        # Add widgets
        self.text_area = tk.Text(self, bg="white")
        # self.text_area.pack()

        self.input_field = ttk.Entry(self, width=100)
        # self.input_field.pack()

        self.chat_button = ttk.Button(self, text="Chat", command=lambda: self.send_message())
        self.quit_button = ttk.Button(self, text="Quit", command=lambda: self.quit_program())
        # self.send_button.pack()

        # Define a grid (3 columns, 3 rows)
        self.text_area.grid(column=0, row=1, columnspan=1, rowspan=3)
        self.input_field.grid(column=0, row=2, columnspan=1, rowspan=3)
        self.chat_button.grid(column=0, row=3, columnspan=1, rowspan=1)
        self.quit_button.grid(column=2, row=3, columnspan=1, rowspan=1)



    def send_message(self) -> None:
        """
        Get input from the user, fetch answers and show them in a text field.
        """

        # Get input and delete the input field
        user_input = self.input_field.get()
        self.input_field.delete(0, "end")

        # Show the input in the text field
        self.text_area.insert("end", f"You: {user_input}\n")
        self.text_area.insert("end", "\n")  # Leerzeile für bessere Lesbarkeit
        chatbot.collect_input(user_input)

        # Fetch the answer
        response = chatbot.get_completion_from_messages(chatbot.context)
        chatbot.collect_responses(response)

        # Show the answer in the text field
        self.text_area.insert("end", f"Chatbot: {response}\n")
        self.text_area.insert("end", "\n \n")  # Zwei Leerzeilen für bessere Lesbarkeit


# input_field.bind_all("<Return>", send_message)

if __name__ == "__main__":
    main_window = MainWindow()
    main_window.mainloop()
