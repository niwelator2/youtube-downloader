# utils/utils.py
import logging
import os
import queue
import threading
from tkinter import filedialog, messagebox
import tkinter as tk
import re

message_queue = queue.Queue()


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


def clean_video_title(title):
    # Remove invalid characters for file names and trim spaces
    return re.sub(r'[<>:"/\\|?*]', "", title).strip()


class UILogHandler(logging.Handler):
    def __init__(self, text_area):
        super().__init__()
        self.text_area = text_area

    def emit(self, record):
        log_message = self.format(record)
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, log_message + "\n")
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)


# Configure logging to send output to the UI
def setup_ui_logger(text_area):
    handler = UILogHandler(text_area)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)


# Function to display messages in the UI
def display_message(message, video_title, text_area, download_type):
    message_queue.put((message, video_title, download_type))
    threading.Thread(target=display_messages_from_queue, args=(text_area,)).start()


def display_messages_from_queue(text_area):
    while not message_queue.empty():
        message, video_title, download_type = message_queue.get()
        title = "System message"
        if video_title:
            title = f"{video_title} ({download_type})"
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, f"{title}: {message}\n")
        text_area.see(tk.END)
        text_area.config(state=tk.DISABLED)
        message_queue.task_done()


def check_download_progress(save_directory, text_area, window):
    if os.listdir(save_directory):
        display_message("Start downloading playlist!", "", text_area)
    else:
        window.after(
            1000, lambda: check_download_progress(save_directory, text_area, window)
        )
