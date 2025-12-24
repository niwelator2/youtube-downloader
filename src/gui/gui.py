import os
import tkinter as tk
from tkinter import ttk, Entry, Button, OptionMenu, StringVar, DoubleVar
from download import download_single_video, download_playlist_threaded
from utils.utils import select_save_directory, load_last_directory

def setup_gui():
    """Creates and configures the YouTube Downloader GUI."""
    window = tk.Tk()
    window.title("YouTube Downloader v2.3")
    window.geometry("800x400")

    # Set window icon
    script_dir = os.path.dirname(os.path.abspath(__file__))
    window.iconbitmap(os.path.join(script_dir, "icon", "logo.ico"))

    # Progress bar
    progress_var = DoubleVar()
    progress_label = ttk.Label(window, text="Progress: 0.00%")
    progress_bar = ttk.Progressbar(window, length=400, mode="determinate", variable=progress_var)

    progress_label.pack(pady=5)
    progress_bar.pack(pady=10, fill=tk.X)

    # Text area for system messages
    text_area = tk.Text(window, wrap=tk.WORD, state=tk.DISABLED, height=6, width=80)
    text_area.pack(pady=5, fill=tk.BOTH, expand=True)

    # Notebook for tab separation
    notebook = ttk.Notebook(window)
    notebook.pack(pady=10, fill=tk.BOTH, expand=True)

    # --- Helper Functions for UI Creation ---
    def create_tab(title):
        """Creates and adds a new tab to the notebook."""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text=title)
        return tab

    def create_entry_row(tab, label_text, row):
        """Creates an entry row with a label."""
        ttk.Label(tab, text=label_text).grid(row=row, column=0, padx=10, pady=5, sticky="w")
        entry = Entry(tab, width=50)
        entry.grid(row=row, column=1, padx=10, pady=5, sticky="w")
        return entry

    # --- Single Video Download Tab ---
    single_tab = create_tab("Single Video Download")
    link_entry = create_entry_row(single_tab, "YouTube URL:", 0)
    save_directory_entry = create_entry_row(single_tab, "Save Directory:", 1)

    download_type_var = StringVar(single_tab, "MP4")
    OptionMenu(single_tab, download_type_var, "MP4", "MP3").grid(row=2, column=1, padx=10, pady=5, sticky="w")

    Button(single_tab, text="Select Directory", command=lambda: select_save_directory(save_directory_entry, load_last_directory())).grid(row=1, column=2, padx=10, pady=5, sticky="w")
    Button(single_tab, text="Download Video", command=lambda: download_single_video(link_entry.get(), download_type_var.get(), save_directory_entry.get(), set(), text_area, progress_var, progress_bar, progress_label)).grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    # --- Playlist Download Tab ---
    playlist_tab = create_tab("Playlist Download")
    playlist_link_entry = create_entry_row(playlist_tab, "Playlist URL:", 0)
    playlist_save_directory_entry = create_entry_row(playlist_tab, "Save Directory:", 1)

    download_type_playlist_var = StringVar(playlist_tab, "MP4")
    OptionMenu(playlist_tab, download_type_playlist_var, "MP4", "MP3").grid(row=2, column=1, padx=10, pady=5, sticky="w")

    Button(playlist_tab, text="Select Directory", command=lambda: select_save_directory(playlist_save_directory_entry, load_last_directory())).grid(row=1, column=2, padx=10, pady=5, sticky="w")
    Button(playlist_tab, text="Download Playlist", command=lambda: download_playlist_threaded(playlist_link_entry.get(), download_type_playlist_var.get(), playlist_save_directory_entry.get(), text_area, progress_var, progress_label, progress_bar)).grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    return window

if __name__ == "__main__":
    window.mainloop()
