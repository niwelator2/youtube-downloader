import os
import threading
import queue
from yt_dlp import YoutubeDL
import tkinter as tk
import logging
from concurrent.futures import ThreadPoolExecutor

from utils.utils import (
    clean_video_title,
    display_message,
    show_error_message,
    check_download_progress,
)
from ydl_opts.setup import get_ydl_opts


# Set up logging
logging.basicConfig(filename="download.log", level=logging.INFO)

# Parameter to update progress bar
update_interval = 1

# Create queues for message and download management

download_queue = queue.Queue()


# Function to update the progress bar in the UI
def update_progress_bar(
    percent, current_video, progress_var, progress_bar, progress_label, window
):
    progress_var.set(percent)
    progress_bar["value"] = percent
    progress_label.config(text=f"Progress: {percent:.2f}% (Video {current_video})")
    window.update_idletasks()


def download_single_video(
    link,
    download_type,
    save_directory,
    current_video,
    downloaded_titles,
    text_area,
    progress_var,
    progress_bar,
    progress_label,
    window,
):
    def on_progress(d):
        if d["status"] == "downloading" and d.get("total_bytes"):
            percent = (d["downloaded_bytes"] / d["total_bytes"]) * 100
            update_progress_bar(
                percent,
                current_video,
                progress_var,
                progress_bar,
                progress_label,
                window,
            )

    ydl_opts = get_ydl_opts(download_type, save_directory, on_progress)

    try:
        # Extract video info
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                link, download=False
            )  # Extract info only, no download yet
            title = clean_video_title(info["title"])

            # Determine file extension based on download type
            file_extension = "mp3" if download_type == "MP3" else "mp4"
            file_path = os.path.join(save_directory, f"{title}.{file_extension}")

            # Check if file already exists on disk
            if os.path.exists(file_path):
                display_message(
                    f"File already exists. Skipping download.",
                    title,
                    text_area,
                    download_type,
                )
                update_progress_bar(
                    0, current_video, progress_var, progress_bar, progress_label, window
                )
                return

            # Check if title is already in downloaded_titles
            if title in downloaded_titles:
                display_message(
                    f"Video already downloaded in this session. Skipping.",
                    title,
                    text_area,
                    download_type,
                )
                update_progress_bar(
                    0, current_video, progress_var, progress_bar, progress_label, window
                )
                return

            # Start download process
            ydl.download([link])

            # Add to downloaded_titles to avoid duplicate downloads in-session
            downloaded_titles.add(title)

            # Display completion message
            display_message("Download completed!", title, text_area, download_type)
            update_progress_bar(
                100, current_video, progress_var, progress_bar, progress_label, window
            )

    except Exception as e:
        logging.error(f"Failed to download video {link}: {e}")
        display_message(f"Error: {e}", "", text_area, download_type)


# Function to download a single video in a separate thread
def download_single_video_threaded(
    link,
    download_type,
    save_directory,
    current_video,
    text_area,
    progress_var,
    progress_bar,
    progress_label,
    window,
):
    try:
        download_thread = threading.Thread(
            target=download_single_video,
            args=(
                link,
                download_type,
                save_directory,
                current_video,
                set(),
                text_area,
                progress_var,
                progress_bar,
                progress_label,
                window,
            ),
        )
        download_thread.start()
    except Exception as e:
        error_message = f"An error has occurred: {str(e)}"
        logging.error(error_message)
        show_error_message(error_message)


# Function to download a playlist using a thread pool
def start_download_playlist_threaded_inner(
    playlist_link,
    download_type,
    save_directory,
    text_area,
    progress_var,
    progress_label,
    progress_bar,
    window,
):
    try:
        playlist = Playlist(playlist_link)
        total_videos = len(playlist.video_urls)
        downloaded_titles = set()

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(
                    download_single_video_threaded,
                    video_url,
                    download_type,
                    save_directory,
                    current_video,
                    text_area,
                    progress_var,
                    progress_bar,
                    progress_label,
                    window,
                )
                for current_video, video_url in enumerate(playlist.video_urls, 1)
            ]
            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    display_message(f"Error in downloading: {str(e)}", "", text_area)

        display_message("Playlist download completed!", "", text_area)

    except Exception as e:
        error_message = f"An error has occurred: {str(e)}"
        logging.error(error_message)
        display_message(error_message, "", text_area)
        show_error_message(error_message)


# Function to handle threaded playlist download
def download_playlist_threaded(
    playlist_link,
    download_type,
    save_directory,
    text_area,
    progress_var,
    progress_label,
    progress_bar,
    window,
):
    try:
        playlist_download_thread = threading.Thread(
            target=start_download_playlist_threaded_inner,
            args=(
                playlist_link,
                download_type,
                save_directory,
                text_area,
                progress_var,
                progress_label,
                progress_bar,
                window,
            ),
        )
        playlist_download_thread.start()
        window.after(
            1000, lambda: check_download_progress(save_directory, text_area, window)
        )
    except Exception as e:
        error_message = f"An error has occurred: {str(e)}"
        logging.error(error_message)
        show_error_message(error_message)
