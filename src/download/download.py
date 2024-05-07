# download.py

import os
import threading
import queue
from pytube import YouTube, Playlist # type: ignore
from utils.utils import (
    show_error_message,
    clean_video_title,
)
import tkinter as tk
from tkinter import text_area
import gui.gui as gui


# Parametr to update progress bar
update_interval = 1
# Create a queue for message display
message_queue = queue.Queue()
download_queue = queue.Queue()
def display_message(message, video_title):
    message_queue.put((message, video_title))

    # Start a separate thread to handle displaying messages
    threading.Thread(target=display_messages_from_queue).start()


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


def on_progress(stream, chunk, bytes_remaining, current_video):
    bytes_downloaded = stream.filesize - bytes_remaining
    percent = (bytes_downloaded / stream.filesize) * 100
    update_progress_bar(percent, current_video)


def update_progress_bar(percent, current_video):
    progress_var.set(percent)
    progress_bar["value"] = percent
    progress_label.config(text=f"Progress: {percent:.2f}% (Video {current_video})")
    window.update_idletasks()


def download_single_video(
    link, download_type, save_directory, current_video, downloaded_titles
):
    """
    Downloads a single video from a given link based on the specified download type.

    Parameters:
        link (str): The link to the video.
        download_type (str): The type of download to perform. Valid options are "MP4" or "MP3".
        save_directory (str): The directory where the downloaded video or audio file will be saved.
        current_video (int): The index of the current video in the list of videos to download.
        downloaded_titles (set): A set of titles of videos that have already been downloaded.

    Returns:
        None

    Raises:
        Exception: If an error occurs during the download process.
    """
    try:
        youtube_object = YouTube(
            link,
            on_progress_callback=lambda stream, chunk, bytes_remaining: on_progress(
                stream, chunk, bytes_remaining, current_video
            ),
        )
        video_title = clean_video_title(youtube_object.title)

        if youtube_object.age_restricted:
            display_message(f"This video is age-restricted. Skipping.", "")
            return

        if video_title in downloaded_titles:
            display_message(f"Skipping duplicate video", "")
            return

        downloaded_titles.add(video_title)

        if download_type == "MP4":
            video_file_path = os.path.join(save_directory, f"{video_title}.mp4")
            if os.path.exists(video_file_path):
                display_message(f"Video already exists.", f"{video_title}")
                return
            stream = youtube_object.streams.get_highest_resolution()
            display_message(f"Downloading video", f"{video_title}")
            video_file = stream.download(
                output_path=save_directory, filename=video_title
            )
            new_file = os.path.join(save_directory, f"{video_title}.mp4")
            os.rename(video_file, new_file)

        elif download_type == "MP3":
            audio_file_path = os.path.join(save_directory, f"{video_title}.mp3")
            if os.path.exists(audio_file_path):
                display_message(f"Audio already exists. Skipping", f"{video_title}")
                return
            stream = youtube_object.streams.filter(only_audio=True).first()
            display_message("Downloading video", f"{video_title}")
            audio_file = stream.download(
                output_path=save_directory, filename=video_title
            )
            new_file = os.path.join(save_directory, f"{video_title}.mp3")
            os.rename(audio_file, new_file)

        else:
            display_message(f"Invalid download type. Choose 'MP4' or 'MP3'. ", "")
            error_message = "Invalid download type. Choose 'MP4' or 'MP3'."
            show_error_message(error_message)
            return

        display_message(f"Download completed!", "")
        update_progress_bar(100, current_video)

    except Exception as e:
        error_message = f"An error has occurred: {str(e)}"
        show_error_message(error_message)


def download_playlist_threaded(playlist_link, download_type, save_directory):
    """
    Downloads a playlist in a separate thread using the given playlist link, download type, and save directory.
    Parameters:
        playlist_link (str): The link to the playlist to be downloaded.
        download_type (str): The type of download to be performed.
        save_directory (str): The directory where the downloaded playlist will be saved.
    Returns:
        None
    """
    try:
        playlist_download_thread = threading.Thread(
            target=start_download_playlist_threaded_inner,
            args=(playlist_link, download_type, save_directory),
        )
        playlist_download_thread.start()

        # Schedule check for updates in GUI from the main thread
        window.after(1000, lambda: check_download_progress(save_directory))
    except Exception as e:
        error_message = f"An error has occurred: {str(e)}"
        show_error_message(error_message)


def check_download_progress(save_directory):
    if os.listdir(save_directory):
        display_message(f"Start downloading playlist!", "")
    else:
        # Schedule another check after 1 second
        window.after(1000, lambda: check_download_progress(save_directory))


def add_to_queue(link, download_type, save_directory):
    download_queue.put((link, download_type, save_directory))
    display_message(f"Link add to queue: {link}", "")


def download_single_video_threaded(link, download_type, save_directory, current_video):
    try:
        download_single_video(link, download_type, save_directory, current_video, set())
        if not download_queue.empty():
            start_next_download_from_queue()
    except Exception as e:
        error_message = f"An error has occurred: {str(e)}"
        show_error_message(error_message)


def start_next_download_from_queue():
    """
    Function to start the next download from the queue.
    """
    try:
        link, download_type, save_directory, current_video = download_queue.get()
        download_single_video(link, download_type, save_directory, current_video, set())
        download_queue.task_done()
        if not download_queue.empty():
            start_next_download_from_queue()
    except Exception as e:
        error_message = f"An error has occurred: {str(e)}"
        show_error_message(error_message)


def start_download_playlist_threaded_inner(
    playlist_link, download_type, save_directory
):
    """
    A function that starts downloading videos from a playlist in a threaded manner.

    Args:
        playlist_link (str): The link to the playlist.
        download_type (str): The type of download (e.g., audio, video).
        save_directory (str): The directory where the downloaded files will be saved.

    Returns:
        None
    """
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

        display_message(f"Playlist download completed!", "")
    except Exception as e:
        error_message = f"An error has occurred: {str(e)}"
        show_error_message(error_message)

