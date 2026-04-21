#!/usr/bin/env python3

"""
This program is inspired by an article from heise.de (german language):
https://www.heise.de/ratgeber/Python-Eigene-KI-Programmierhilfe-entwickeln-9330993.html

In contrast to the code in the article, the new API (> 1.0.0) is used here.

Version: 3.0
Python 3.12+
Date created: November 8th, 2023
Date modified: April 21st, 2026
"""

import tkinter as tk
import logging
import os
import threading

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
    """
    Main application window for the AI Chatbot.

    Provides the main GUI setup and controls for interacting with the AI chatbot.
    This class initializes the application window, configures menu bars, text
    inputs, and buttons, and manages user interaction through input fields and
    the output display area. It also centers the main window on the screen and
    styles various widgets for a better user experience.

    Attributes:
        window (tk.Tk): Main application window instance.
        text_frame (ttk.Frame): Frame containing the text display widget.
        text_widget (tk.Text): Text widget for displaying chat history and chatbot responses.
        input_frame (ttk.Frame): Frame containing the user input field.
        input_field (ttk.Entry): Entry widget for user input.
        button_frame (ttk.Frame): Frame containing buttons like "Chat" and "Quit".
        chat_button (ttk.Button): Button to submit user input and fetch chatbot response.
        quit_button (ttk.Button): Button to quit the application.
    """

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

        window_width = 1000
        window_height = 800

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
            spacing1=4,  # Distance in front of the block
            spacing2=2,  # Line spacing within the block
            spacing3=4  # Distance after the block
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
            font=("Courier", 16),
            foreground="purple",
            background="#f0f0f0",
            lmargin1=10,
            lmargin2=10,
            spacing1=4,  # Distance in front of the block
            spacing2=2,  # Line spacing within the block
            spacing3=4  # Distance after the block
        )
        self.text_widget.tag_configure("user_text", foreground="green")

        # Create a frame for an input field
        self.input_frame = ttk.Frame(self.window)
        self.input_frame.grid(row=1, column=0, sticky="ew")

        # Add an entry widget to the input_frame
        self.input_field = ttk.Entry(
            self.input_frame, foreground="blue", background="white"
        )
        self.input_field.bind("<Return>", lambda event: self.send_message())
        self.input_field.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        # Create a frame for buttons
        self.button_frame = ttk.Frame(self.window)
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
        Get input from the user, fetch answers, and show them in a text field.
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
            if not user_input.strip():
                return
            self.input_field.delete(0, "end")

            # Show the input in the text field
            self.text_widget.insert("end", f"You: {user_input}\n", "user_text")
            self.text_widget.insert("end", "\n")

            setup_ai.collect_input(user_input)

            # Disable chat button to prevent multiple simultaneous requests
            self.chat_button.config(state="disabled")

            # Start the API call in a separate thread
            api_thread = threading.Thread(
                target=self.fetch_ai_response, args=(setup_ai.context,)
            )
            api_thread.start()

        else:
            error_window.show_error(f"Can't find API file!\n({api_file_path})")

    def fetch_ai_response(self, context) -> None:
        """
        Fetch completion from AI in a separate thread and update the UI.
        """
        try:
            # Fetch the answer (blocking call)
            response = setup_ai.get_completion_from_messages(context)
            setup_ai.collect_responses(response)
            logging.debug(response)

            # Update the text widget in the main thread
            self.window.after(0, lambda: self.show_text(response))
        except Exception as e:
            logging.error(f"Error fetching AI response: {e}")
            self.window.after(
                0,
                lambda: error_window.show_error(f"Error fetching AI response: {e}"),
            )
        finally:
            # Re-enable the chat button in the main thread
            self.window.after(0, lambda: self.chat_button.config(state="normal"))

    def show_text(self, md_text):
        """
        Renders and displays Markdown text in a text widget by converting it to styled text.

        This method processes the provided Markdown text, converts it to styled HTML using
        Markdown processing libraries, and then parses the HTML to render the styled content
        into a text widget. Each HTML element in the Markdown is translated to a corresponding
        style or formatting in the text widget (e.g., headings, bold, italic, code blocks).
        The method ensures that Markdown syntax like fenced codes and highlighted code are
        properly processed and displayed.

        Args:
            md_text (str): Markdown-formatted string that needs to be rendered and displayed.
        """
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
                    code_text = el.get_text()
                    self.text_widget.insert(
                        "end", code_text, current_tags + ("codeblock",)
                    )
                    # Add a copy button for the code block
                    copy_button = ttk.Button(
                        self.text_widget,
                        text="Copy",
                        width=10,
                        command=lambda t=code_text: self.copy_to_clipboard(t),
                    )
                    self.text_widget.window_create("end", window=copy_button)
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

    def copy_to_clipboard(self, text):
        """
        Copies the given text to the system clipboard.

        Args:
            text (str): The text to be copied.
        """
        self.window.clipboard_clear()
        self.window.clipboard_append(text)

    def quit_program(self):
        """
        Destroys the main application window.

        This method is used to terminate the application by closing the primary
        window. It leverages the `destroy` method of the `tkinter` library to
        shut down the interface and safely exit the program.

        Raises:
            None
        """
        self.window.destroy()

    def mainloop(self):
        """
        Executes the main event loop for the graphical user interface (GUI).

        This method is responsible for starting the tkinter event loop, which
        continually listens for and processes user input such as mouse clicks
        or keypresses within the application window. The loop runs until the
        application window is closed.

        Returns:
            None
        """
        self.window.mainloop()


if __name__ == "__main__":
    window = tk.Tk()
    main_window = MainWindow(window)
    main_window.mainloop()
