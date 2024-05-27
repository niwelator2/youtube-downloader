import os
import tkinter as tk
from tkinter import PhotoImage, ttk, Label, Entry, Button, OptionMenu, StringVar, DoubleVar, filedialog, messagebox
from download import download_single_video_threaded, download_playlist_threaded
from utils.utils import select_save_directory, load_last_directory, show_error_message

def setup_gui():
    window = tk.Tk()
    window.title("YouTube Downloader v2.3")
    window.geometry("800x400")
    
    # Construct the absolute path to the icon file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(script_dir, "icon", "logo.ico")
    window.iconbitmap(icon_path)

    # Create a Label to display progress
    progress_var = DoubleVar()
    progress_label = Label(window, text="Progress: 0.00%")
    progress_label.pack(pady=5)

    # Create a text area for system messages
    text_area = tk.Text(window, wrap=tk.WORD, state=tk.DISABLED, height=6, width=80)
    text_area.pack(pady=5, fill=tk.BOTH, expand=True)

    # Create a notebook to organize the single video and playlist download sections
    notebook = ttk.Notebook(window)
    notebook.pack(pady=10, fill=tk.BOTH, expand=True)

    # Single video download tab
    single_tab = ttk.Frame(notebook)
    notebook.add(single_tab, text="Single Video Download")

    Label(single_tab, text="YouTube URL:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    link_entry = Entry(single_tab, width=50)
    link_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    Label(single_tab, text="Download Type:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    download_type_var = StringVar(single_tab)
    download_type_var.set("MP4")
    download_type_menu = OptionMenu(single_tab, download_type_var, "MP4", "MP3")
    download_type_menu.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    Label(single_tab, text="Save Directory:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    save_directory_entry = Entry(single_tab, width=50)
    save_directory_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    select_directory_button = Button(
        single_tab,
        text="Select Directory",
        command=lambda: select_save_directory(
            save_directory_entry, load_last_directory()
        ),
    )
    select_directory_button.grid(row=2, column=2, padx=10, pady=5, sticky="w")

    download_button = Button(
        single_tab,
        text="Download Single Video",
        command=lambda: download_single_video_threaded(
            link_entry.get(), download_type_var.get(), save_directory_entry.get(), 1, text_area, progress_var, progress_bar, progress_label, window
        ),
    )
    download_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    open_directory_button = Button(
        single_tab,
        text="Open Directory",
        command=lambda: open_directory(save_directory_entry),
    )
    open_directory_button.grid(row=3, column=2, padx=10, pady=5)

    # Playlist download tab
    playlist_tab = ttk.Frame(notebook)
    notebook.add(playlist_tab, text="Playlist Download")

    Label(playlist_tab, text="YouTube Playlist URL:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    playlist_link_entry = Entry(playlist_tab, width=50)
    playlist_link_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    Label(playlist_tab, text="Download Type:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    download_type_playlist_var = StringVar(playlist_tab)
    download_type_playlist_var.set("MP4")
    download_type_playlist_menu = OptionMenu(playlist_tab, download_type_playlist_var, "MP4", "MP3")
    download_type_playlist_menu.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    Label(playlist_tab, text="Save Directory:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    playlist_save_directory_entry = Entry(playlist_tab, width=50)
    playlist_save_directory_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    select_playlist_directory_button = Button(
        playlist_tab,
        text="Select Directory",
        command=lambda: select_save_directory(
            playlist_save_directory_entry, load_last_directory()
        ),
    )
    select_playlist_directory_button.grid(row=2, column=2, padx=10, pady=5, sticky="w")

    download_playlist_button = Button(
        playlist_tab,
        text="Download Playlist",
        command=lambda: download_playlist_threaded(
            playlist_link_entry.get(),
            download_type_playlist_var.get(),
            playlist_save_directory_entry.get(),
            text_area, progress_var, progress_label, progress_bar, window
        ),
    )
    download_playlist_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    open_playlist_directory_button = Button(
        playlist_tab,
        text="Open Directory",
        command=lambda: open_directory(playlist_save_directory_entry),
    )
    open_playlist_directory_button.grid(row=3, column=2, padx=10, pady=5)

    # Progress bar
    progress_bar = ttk.Progressbar(
        window, length=400, mode="determinate", variable=progress_var
    )
    progress_bar.pack(pady=10, fill=tk.X)

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
        text_area.config(state=tk.NORMAL)
        text_area.delete(1.0, tk.END)
        text_area.config(state=tk.DISABLED)

    reset_button = Button(window, text="Reset Values", command=reset_values)
    reset_button.pack(pady=5)

    def open_directory(entry):
        directory = entry.get()
        if os.path.exists(directory):
            os.startfile(directory)
        else:
            show_error_message(f"Directory not found: {directory}")

    return window, text_area, progress_var, progress_label, progress_bar

if __name__ == "__main__":
    window, text_area, progress_var, progress_label, progress_bar = setup_gui()
    window.mainloop()
