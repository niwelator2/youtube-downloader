import os
import tkinter as tk
from tkinter import PhotoImage, ttk, Label, Entry, Button, OptionMenu, StringVar, DoubleVar, filedialog, messagebox
from download import download_single_video_threaded, download_playlist_threaded
from utils.utils import select_save_directory, load_last_directory, show_error_message

def setup_gui():
    window = tk.Tk()
    window.title("YouTube Downloader")
    window.geometry("800x320")
    
    # Construct the absolute path to the icon file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(script_dir, "icon", "logo.ico")
    window.iconbitmap(icon_path)

    # Create a Label to display progress
    progress_var = DoubleVar()
    progress_label = Label(window, text="Progress: 0.00%")
    progress_label.pack(pady=10)
    # Create a text area for system message
    text_area = tk.Text(window, wrap=tk.WORD, state=tk.DISABLED, height=3, width=20)
    text_area.pack(fill=tk.BOTH, expand=True)
    # Left section for single video download
    left_frame = ttk.Frame(window)
    left_frame.pack(side="left", padx=20)

    Label(left_frame, text="YouTube URL:").pack(pady=10)
    link_entry = Entry(left_frame, width=50)
    link_entry.pack()

    Label(left_frame, text="Download Type:").pack()
    download_type_var = StringVar(left_frame)
    download_type_var.set("MP4")
    download_type_menu = OptionMenu(left_frame, download_type_var, "MP4", "MP3")
    download_type_menu.pack()

    Label(left_frame, text="Save Directory:").pack()
    save_directory_entry = Entry(left_frame, width=50)
    save_directory_entry.pack()
    select_directory_button = Button(
        left_frame,
        text="Select Directory",
        command=lambda: select_save_directory(
            save_directory_entry, load_last_directory()
        ),
    )
    select_directory_button.pack()

    download_button = Button(
        left_frame,
        text="Download Single Video",
        command=lambda: download_single_video_threaded(
            link_entry.get(), download_type_var.get(), save_directory_entry.get(), 1, text_area, progress_var, progress_bar, progress_label, window
        ),
    )
    download_button.pack(pady=1)

    def open_directory():
        directory = save_directory_entry.get()
        if os.path.exists(directory):
            os.startfile(directory)
        else:
            show_error_message(f"Directory not found: {directory}")

    directory_button = Button(
        left_frame,
        text="Open Directory",
        command=lambda: open_directory(),
    )
    directory_button.pack(pady=2)

    # Right section for playlist download
    right_frame = ttk.Frame(window)
    right_frame.pack(side="right", padx=20)

    Label(right_frame, text="YouTube Playlist URL:").pack(pady=10)
    playlist_link_entry = Entry(right_frame, width=50)
    playlist_link_entry.pack()

    Label(right_frame, text="Download Type:").pack()
    download_type_playlist_var = StringVar(right_frame)
    download_type_playlist_var.set("MP4")
    download_type_menu = OptionMenu(
        right_frame, download_type_playlist_var, "MP4", "MP3"
    )
    download_type_menu.pack()

    Label(right_frame, text="Save Directory:").pack()
    playlist_save_directory_entry = Entry(right_frame, width=50)
    playlist_save_directory_entry.pack()

    select_playlist_directory_button = Button(
        right_frame,
        text="Select Directory",
        command=lambda: select_save_directory(
            playlist_save_directory_entry, load_last_directory()
        ),
    )
    select_playlist_directory_button.pack()

    download_button2 = Button(
        right_frame,
        text="Download Playlist",
        command=lambda: download_playlist_threaded(
            playlist_link_entry.get(),
            download_type_playlist_var.get(),
            playlist_save_directory_entry.get(),
            text_area, progress_var, progress_label, progress_bar, window
        ),
    )
    download_button2.pack(pady=1)

    def open_playlist_directory():
        directory = playlist_save_directory_entry.get()
        if os.path.exists(directory):
            os.startfile(directory)
        else:
            show_error_message(f"Directory not found: {directory}")

    playlist_directory_button = Button(
        right_frame,
        text="Open Playlist Directory",
        command=open_playlist_directory,
    )
    playlist_directory_button.pack(pady=2)

    # Progress bar
    progress_bar = ttk.Progressbar(
        window, length=200, mode="determinate", variable=progress_var
    )
    progress_bar.pack(pady=10)

    last_directory = load_last_directory()
    if last_directory:
        save_directory_entry.insert(0, last_directory)
        playlist_save_directory_entry.insert(0, last_directory)

    def reset_values():
        link_entry.delete(0, tk.END)
        playlist_link_entry.delete(0, tk.END)
        save_directory_entry.delete(0, tk.END)
        playlist_save_directory_entry.delete(0, tk.END)
        progress_var.set(0.0)
        progress_label.config(text="Progress: 0.00%")
        text_area.config(state=tk.DISABLED)

    reset_button = Button(window, text="Reset Values", command=reset_values)
    reset_button.pack()

    return window, text_area, progress_var, progress_label, progress_bar
