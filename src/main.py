#!/usr/bin/env python3

"""
This program is inspired by an article from heise.de (german language):
https://www.heise.de/ratgeber/Python-Eigene-KI-Programmierhilfe-entwickeln-9330993.html

In contrast to the code in the article, the new API (> 1.0.0) is used here.

Version: 3.0
Python 3.12+
Date created: November 8th, 2023
Date modified: April 25th, 2025
"""

import tkinter as tk
import logging
import os

from markdown import markdown
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from os.path import expanduser

# from tkinter import messagebox
from tkinter import ttk

from src import error_window
from src import setup_ai

# from src import about_window


# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

api_file_path = expanduser("~") + "/Documents/API/openai-api-file.bin"


class MainWindow:
    def __init__(self, app_window):
        self.window = app_window
        self.window.title("AI Chatbot (Python)")
        self.window.lift()

        # Customize macOS menu bar (optional)
        menu_bar = tk.Menu(self.window)
        self.window.config(menu=menu_bar)

        # Add "File" with "Quit" button to menu bar.
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Quit", command=self.window.quit)

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
        self.text_widget = tk.Text(
            self.text_frame,
            wrap="word",
            bg="#f9f9f9",
            height=15,
            font=("Helvetica", 16),
        )
        self.text_widget.grid(row=0, column=0, sticky="nsew")

        self.text_widget.tag_configure("bold", font=("Helvetica", 16, "bold"))
        self.text_widget.tag_configure("italic", font=("Helvetica", 16, "italic"))
        self.text_widget.tag_configure("h1", font=("Helvetica", 18, "bold"))
        self.text_widget.tag_configure("h2", font=("Helvetica", 16, "bold"))
        self.text_widget.tag_configure(
            "inlinecode", font=("Courier", 16), background="#e8e8e8"
        )
        self.text_widget.tag_configure(
            "codeblock",
            font=("Courier", 14),
            background="#f0f0f0",
            lmargin1=10,
            lmargin2=10,
        )

        # Create a frame for an input field
        self.input_frame = ttk.Frame(window)
        self.input_frame.grid(row=1, column=0, sticky="ew")

        # Add an entry widget to the input_frame
        self.input_field = ttk.Entry(
            self.input_frame, foreground="blue", background="white"
        )
        self.input_field.bind("<Return>", lambda event: self.send_message())
        self.input_field.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

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

        # Configure a grid to ensure the Text widget and button_frame fill the window
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.text_frame.grid_rowconfigure(0, weight=1)
        self.text_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)

    def send_message(self) -> None:
        """
        Get input from the user, fetch answers and show them in a text field.
        """

        # Check if the api file is available
        if os.path.isfile(api_file_path):
            logging.debug(f"The file '{api_file_path}' exists and is readable.")
            try:
                with open(api_file_path, encoding="utf-8") as binary_file:
                    binary_file.read()
            except FileNotFoundError as ex:
                print(ex)

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

            self.show_text(response)

        else:
            error_window.show_error(f"Can't find API file!\n({api_file_path})")

    def show_text(self, md_text):

        self.text_widget.insert("end", "Chatbot:\n")

        html = markdown(md_text, extensions=["fenced_code", "codehilite"])
        soup = BeautifulSoup(html, "html.parser")

        def render_element(el, current_tags=()):
            if isinstance(el, NavigableString):
                if el.strip() != "":
                    self.text_widget.insert("end", el, current_tags)
            elif el.name in ["strong", "b"]:
                for child in el.contents:
                    render_element(child, current_tags + ("bold",))
            elif el.name in ["em", "i"]:
                for child in el.contents:
                    render_element(child, current_tags + ("italic",))
            elif el.name == "h1":
                for child in el.contents:
                    render_element(child, current_tags + ("h1",))
                self.text_widget.insert("end", "\n")
            elif el.name == "h2":
                for child in el.contents:
                    render_element(child, current_tags + ("h2",))
                self.text_widget.insert("end", "\n")
            elif el.name == "code":
                # Check if the code is a code block or inline code
                if el.parent.name == "pre":
                    self.text_widget.insert(
                        "end", el.get_text(), current_tags + ("codeblock",)
                    )
                    self.text_widget.insert("end", "\n")
                else:
                    self.text_widget.insert(
                        "end", el.get_text(), current_tags + ("inlinecode",)
                    )
            elif el.name == "pre":
                for child in el.contents:
                    render_element(child, current_tags)
                self.text_widget.insert("end", "\n")
            elif el.name == "p":
                for child in el.contents:
                    render_element(child, current_tags)
                self.text_widget.insert("end", "\n\n")
            else:
                for child in el.contents:
                    render_element(child, current_tags)

        for elem in soup.body or soup:
            render_element(elem)

        self.text_widget.insert("end", "\n \n")

    # def show_custom_about(self):
    #     about_message = "PythonBot\nVersion 0.1.3\n2025 Bodo Schönfeld"
    #     messagebox.showinfo("About", about_message)

    def quit_program(self):
        self.window.destroy()

    def mainloop(self):
        self.window.mainloop()


if __name__ == "__main__":
    window = tk.Tk()
    main_window = MainWindow(window)
    main_window.mainloop()
