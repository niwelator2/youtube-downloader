import os
import threading
import queue
import re
from pytube import YouTube, Playlist
from googleapiclient.discovery import build

import requests
from bs4 import BeautifulSoup
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TDRC

import tkinter as tk
from tkinter import (
    ttk,
    Label,
    Entry,
    Button,
    OptionMenu,
    StringVar,
    DoubleVar,
    filedialog,
    messagebox,
)


# Parametr to update progress bar
update_interval = 1
# Create a queue for message display
message_queue = queue.Queue()
download_queue = queue.Queue()


def display_message(message, video_title=None):
    message_queue.put((message, video_title))
    display_messages_from_queue()


def display_messages_from_queue():
    while not message_queue.empty():
        message, video_title = message_queue.get()
        title = "System message"
        if video_title:
            title = video_title
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, f"{title}: {message}\n")
        text_area.see(tk.END)
        text_area.config(state=tk.DISABLED)
        message_queue.task_done()


# This def tells how much bytes of the song is left to download
def on_progress(stream, chunk, bytes_remaining, current_video):
    bytes_downloaded = stream.filesize - bytes_remaining
    percent = (bytes_downloaded / stream.filesize) * 100
    update_progress_bar(percent, current_video)


def update_progress_bar(percent, current_video):
    progress_var.set(percent)
    progress_bar["value"] = percent
    progress_label.config(text=f"Progress: {percent:.2f}% (Video {current_video})")
    window.update_idletasks()


def clean_video_title(title):
    return "".join(c if c.isalnum() or c in [" ", "_", "-"] else "_" for c in title)


def extract_video_id(url):
    video_id_match = re.search(r"(?<=v=)[\w-]+", url)
    if video_id_match:
        return video_id_match.group(0)
    else:
        return None


def get_video_metadata(api_key, video_url):
    youtube = build("youtube", "v3", developerKey=api_key)
    video_id = extract_video_id(video_url)
    if video_id:
        request = youtube.videos().list(part="snippet", id=video_id)
        response = request.execute()
        if response["items"]:
            video_info = response["items"][0]["snippet"]
            title = video_info["title"]
            description = video_info["description"]
            upload_date = video_info["publishedAt"]
            return {
                "title": title,
                "description": description,
                "upload_date": upload_date,
            }
    return None


def save_data_to_mp3(link, mp3_file_path):
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, "html.parser")

        api_key = "YOUR_API_KEY"  # Replace with your actual API key
        metadata = get_video_metadata(api_key, link)
        if metadata:
            print("Title:", metadata["title"])
            print("Description:", metadata["description"])
            print("Upload Date:", metadata["upload_date"])
        else:
            print("Video not found or invalid URL.")

        # Find tags containing album, artist, and release date information
        album_tag = soup.find("meta", property="og:album")
        artist_tag = soup.find("meta", property="og:artist")
        release_date_tag = soup.find("meta", property="og:release_date")

        # Extract content from tags if found
        album = album_tag["content"] if album_tag else None
        artist = artist_tag["content"] if artist_tag else None
        release_date = release_date_tag["content"] if release_date_tag else None

        # Load the MP3 file using mutagen
        audio = MP3(mp3_file_path, ID3=ID3)

        # Create a new ID3 tag if one doesn't exist
        if not audio.tags:
            audio.add_tags()

        # Set metadata
        if album:
            audio.tags.add(TALB(encoding=3, text=album))
        if artist:
            audio.tags.add(TPE1(encoding=3, text=artist))
        if release_date:
            audio.tags.add(TDRC(encoding=3, text=release_date))

        # Save the changes to the MP3 file
        audio.save()

        display_message("Metadata saved to MP3 file successfully", "")

    except Exception as e:
        error_message = f"An error occurred while saving metadata to MP3 file: {str(e)}"
        display_message(error_message, "")


def show_error_message(message):
    messagebox.showerror("Error", message)


def download_single_video(
    link, download_type, save_directory, current_video, downloaded_titles
):
    try:
        youtube_object = YouTube(
            link,
            on_progress_callback=lambda stream, chunk, bytes_remaining: on_progress(
                stream, chunk, bytes_remaining, current_video
            ),
        )
        video_title = clean_video_title(youtube_object.title)
        if video_title in downloaded_titles:
            display_message("Skipping duplicate video", "")
            return

        downloaded_titles.add(video_title)

        if download_type == "MP4":
            video_file_path = os.path.join(save_directory, f"{video_title}.mp4")
            if os.path.exists(video_file_path):
                display_message("Video already exists.", f"{video_title}")
                return
            stream = youtube_object.streams.get_highest_resolution()
            display_message("Downloading video", f"{video_title}")
            video_file = stream.download(
                output_path=save_directory, filename=video_title
            )
            new_file = os.path.join(save_directory, f"{video_title}.mp4")
            os.rename(video_file, new_file)

        elif download_type == "MP3":
            audio_file_path = os.path.join(save_directory, f"{video_title}.mp3")
            if os.path.exists(audio_file_path):
                display_message("Audio already exists. Skipping", f"{video_title}")
                return
            stream = youtube_object.streams.filter(only_audio=True).first()
            display_message("Downloading video", f"{video_title}")
            audio_file = stream.download(
                output_path=save_directory, filename=video_title
            )
            new_file = os.path.join(save_directory, f"{video_title}.mp3")
            os.rename(audio_file, new_file)
            # Save metadata to the downloaded MP3 file
            save_data_to_mp3(link, new_file)

        else:
            error_message = "Invalid download type. Choose 'MP4' or 'MP3'."
            show_error_message(error_message)
            return

        display_message("Download completed!", "")
        update_progress_bar(100, current_video)

    except Exception as e:
        error_message = f"An error has occurred: {str(e)}"
        show_error_message(error_message)


def download_playlist_threaded(playlist_link, download_type, save_directory):
    try:
        playlist_download_thread = threading.Thread(
            target=start_download_playlist_threaded_inner,
            args=(playlist_link, download_type, save_directory),
        )
        playlist_download_thread.start()
    except Exception as e:
        error_message = f"An error has occurred: {str(e)}"
        show_error_message(error_message)


def start_download_playlist_threaded_inner(
    playlist_link, download_type, save_directory
):
    try:
        playlist = Playlist(playlist_link)
        total_videos = len(playlist.video_urls)
        current_video = 1

        for video_url in playlist.video_urls:
            download_single_video_threaded(
                video_url, download_type, save_directory, current_video
            )
            percent_complete = (current_video / total_videos) * 100
            update_progress_bar(percent_complete, current_video)
            current_video += 1

        display_message("Playlist download completed!", "")
    except Exception as e:
        error_message = f"An error has occurred: {str(e)}"
        show_error_message(error_message)


def add_to_queue(link, download_type, save_directory):
    download_queue.put((link, download_type, save_directory))
    display_message(f"Link added to queue: {link}")


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


def download_single_video_threaded(link, download_type, save_directory, current_video):
    try:
        download_single_video(link, download_type, save_directory, current_video, set())
        if not download_queue.empty():
            start_next_download_from_queue()
    except Exception as e:
        error_message = f"An error has occurred: {str(e)}"
        show_error_message(error_message)


def start_next_download_from_queue():
    try:
        link, download_type, save_directory, current_video = download_queue.get()
        download_single_video(link, download_type, save_directory, current_video, set())
        download_queue.task_done()
        if not download_queue.empty():
            start_next_download_from_queue()
    except Exception as e:
        error_message = f"An error has occurred: {str(e)}"
        show_error_message(error_message)


def setup_gui():
    window = tk.Tk()
    window.title("YouTube Downloader")
    window.geometry("800x300")

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
            link_entry.get(), download_type_var.get(), save_directory_entry.get(), 1
        ),
    )
    download_button.pack()

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
        ),
    )
    download_button2.pack()

    # Progress bar
    progress_bar = ttk.Progressbar(
        window, length=200, mode="determinate", variable=progress_var
    )
    progress_bar.pack(pady=10)

    last_directory = load_last_directory()
    if last_directory:
        save_directory_entry.insert(0, last_directory)
        playlist_save_directory_entry.insert(0, last_directory)

    # Function to reset all values
    def reset_values():
        link_entry.delete(0, tk.END)
        playlist_link_entry.delete(0, tk.END)
        save_directory_entry.delete(0, tk.END)
        playlist_save_directory_entry.delete(0, tk.END)
        progress_var.set(0.0)
        progress_label.config(text="Progress: 0.00%")
        text_area.config(state=tk.DISABLED)

    # Button to reset values
    reset_button = Button(window, text="Reset Values", command=reset_values)
    reset_button.pack()

    return window, text_area, progress_var, progress_label, progress_bar


# Call setup_gui to initialize GUI elements
window, text_area, progress_var, progress_label, progress_bar = setup_gui()

# Start the Tkinter main loop
window.mainloop()
