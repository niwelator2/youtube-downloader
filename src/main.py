# main.py

import tkinter as tk
from gui.gui import setup_gui
from download import download_single_video_threaded, download_playlist_threaded
from utils.utils import load_last_directory

def main():
    try:
        # Set up GUI
        window, text_area, progress_var, progress_label, progress_bar = setup_gui()

        # Start the Tkinter main loop
        window.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
