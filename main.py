import os
import requests
from pytube import YouTube
import tkinter as tk
from tkinter import ttk
from tkinter import Label, Entry, Button, OptionMenu, StringVar, filedialog
from google.oauth2 import credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Define your Google API credentials (client_id and client_secret)
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

# Path to credentials file (store your credentials here)
CREDENTIALS_FILE = 'credentials.json'

# Create or load the OAuth2 credentials
def get_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        credentials = flow.run_local_server()
        return credentials
    else:
        raise Exception("Credentials file not found. Please provide your OAuth2 credentials.")

# Authenticate and get YouTube data
def authenticate_and_get_youtube_data():
    credentials = get_credentials()

    # Perform YouTube-related tasks here using the authenticated credentials
    # For example, list user's YouTube videos, upload videos, etc.
    # Ensure you use YouTube Data API for these tasks.

def on_progress(stream, chunk, bytes_remaining):
    # Calculate the percentage of completion
    bytes_downloaded = stream.filesize - bytes_remaining
    percent = (bytes_downloaded / stream.filesize) * 100
    # Update the progress label
    update_progress_bar(percent)

def update_progress_bar(percent):
    progress_label.config(text=f"Progress: {percent:.2f}%")

def download_video():
    link = link_entry.get()
    download_type = download_type_var.get()
    save_directory = save_directory_entry.get()

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    try:
        YouTube.allow_oauth_cache = True
        youtube_object = YouTube(link, on_progress_callback=on_progress)
        video_title = youtube_object.title

        if download_type == 'MP4':
            stream = youtube_object.streams.get_highest_resolution()
            print("Downloading video:", video_title)
            video_file = stream.download(output_path=save_directory, filename=video_title)
            new_file = os.path.join(save_directory, f"{video_title}.mp4")
            os.rename(video_file, new_file)

        elif download_type == 'MP3':
            stream = youtube_object.streams.filter(only_audio=True).first()
            print("Downloading audio (MP3):", video_title)
            audio_file = stream.download(output_path=save_directory, filename=video_title)
            new_file = os.path.join(save_directory, f"{video_title}.mp3")
            os.rename(audio_file, new_file)

        elif download_type == 'Audio':
            stream = youtube_object.streams.filter(only_audio=True).first()
            print("Downloading audio (without conversion):", video_title)
            audio_file = stream.download(output_path=save_directory, filename=video_title + ".mp4")
            new_file = os.path.join(save_directory, f"{video_title}.mp3")
            os.rename(audio_file, new_file)

        else:
            print("Invalid download type. Choose 'MP4', 'MP3', or 'Audio'.")
            return

        print("Download completed!")
    except Exception as e:
        print("An error has occurred:", str(e))

def select_save_directory():
    directory = filedialog.askdirectory()
    if directory:
        save_directory_entry.delete(0, tk.END)
        save_directory_entry.insert(0, directory)

# Create the main window
window = tk.Tk()
window.title("YouTube Downloader")
window.geometry('640x240')

# Create and pack GUI elements with styling
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12))
style.configure("TEntry", font=("Helvetica", 12))
style.configure("TMenubutton", font=("Helvetica", 12))

Label(window, text="YouTube Video URL:").pack(pady=10)
link_entry = Entry(window, width=50)
link_entry.pack()

Label(window, text="Download Type:").pack()
download_type_var = StringVar(window)
download_type_var.set("MP4")
download_type_menu = OptionMenu(window, download_type_var, "MP4", "MP3", "Audio")
download_type_menu.pack()

Label(window, text="Save Directory:").pack()
save_directory_entry = Entry(window, width=50)
save_directory_entry.pack()

Button(window, text="Select Directory", command=select_save_directory).pack()
download_button = Button(window, text="Download", command=download_video)
download_button.pack()

# Create a Label to display progress
progress_label = Label(window, text="Progress: 0.00%")
progress_label.pack(pady=10)

# Start the Tkinter main loop
window.mainloop()
