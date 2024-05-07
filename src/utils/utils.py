# utils.py

import os
from tkinter import filedialog, messagebox
import tkinter as tk

def select_save_directory(entry_widget, initial_dir=None):
    directory = filedialog.askdirectory(initialdir=initial_dir)
    if directory:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, directory)
        set_last_directory(directory)


def set_last_directory(directory):
    with open(".last_directory", "w") as f:
        f.write(directory)


def load_last_directory():
    try:
        with open(".last_directory", "r") as f:
            return f.read()
    except FileNotFoundError:
        return None

def show_error_message(message):
    messagebox.showerror("Error", message)