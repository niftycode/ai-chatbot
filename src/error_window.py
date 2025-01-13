#!/usr/bin/env python3

"""
Version: 1.0
Python 3.12+
Date created: November 15th, 2024
Date modified: -
"""

import tkinter as tk
from tkinter import messagebox


def show_error(message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error", message)
    root.destroy()
