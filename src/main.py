import tkinter as tk
from gui import setup_gui
import threading


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
