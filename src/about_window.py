#!/usr/bin/env python3

"""
Version: 1.0
Python 3.12+
Date created: May 1st, 2025
Date modified: -
"""

import tkinter as tk

from tkinter import ttk


# Not currently in use!
def show_custom_about(self):
    about = tk.Toplevel()
    about.title("About this app")
    about.resizable(False, False)

    # App name
    tk.Label(about, text="PythonBot", font=("Helvetica", 16, "bold")).pack(pady=(10, 0))

    # Version
    tk.Label(about, text="Version ...").pack()

    # Copyright
    tk.Label(about, text="© 2025 my name").pack(pady=(0, 10))

    # Separator
    ttk.Separator(about, orient="horizontal").pack(fill="x", padx=10)

    # Description
    description = tk.Label(
        about,
        text="app description\n\n" "Created by ...",
        justify="center",
    )
    description.pack(pady=10)

    # OK button
    ttk.Button(about, text="OK", command=about.destroy).pack(pady=(0, 10))
