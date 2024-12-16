import os
import threading
import queue
import time
from utils.utils import clean_video_title, on_progress
from yt_dlp import YoutubeDL
import traceback
from utils.ydl_opts import (
    get_ydl_opts_playlist,
    get_ydl_opts_single_mp3,
    get_ydl_opts_single_mp4,
)
import tkinter as tk
import logging


logging.basicConfig(
    filename="download.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Queues for thread-safe communication
message_queue = queue.Queue()

# Update interval for the progress bar
UPDATE_INTERVAL = 1


# Function to log and display messages in the UI
def log_and_display_message(message, video_title, text_area):
    logging.info(message)
    display_message(message, video_title, text_area)


# Function to display messages in the text area
def display_message(message, video_title, text_area):
    message_queue.put((message, video_title))
    threading.Thread(target=display_messages_from_queue, args=(text_area,)).start()


def display_messages_from_queue(text_area):
    while not message_queue.empty():
        message, video_title = message_queue.get()
        title = "System message" if not video_title else video_title
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, f"{title}: {message}\n")
        text_area.see(tk.END)
        text_area.config(state=tk.DISABLED)
        message_queue.task_done()


# Function to update the progress bar
def update_progress_bar(
    percent, current_video, progress_var, progress_bar, progress_label, window
):
    progress_var.set(percent)
    progress_bar["value"] = percent
    progress_label.config(text=f"Progress: {percent:.2f}% (Video {current_video})")
    window.update_idletasks()


# Function to download a single video
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
    if download_type == "MP3":
        ydl_opts = get_ydl_opts_single_mp3
    elif download_type == "MP4":
        ydl_opts = get_ydl_opts_single_mp4
    else:
        display_message("Invalid download type. Choose 'MP4' or 'MP3'.", "", text_area)
        return

    def on_progress_hook(d):
        if d["status"] == "downloading" and d.get("total_bytes"):
            percent = d["downloaded_bytes"] / d["total_bytes"] * 100
            update_progress_bar(
                percent,
                current_video,
                progress_var,
                progress_bar,
                progress_label,
                window,
            )

    ydl_opts = ydl_opts(text_area)
    ydl_opts["progress_hooks"] = [on_progress_hook]
    ydl_opts["outtmpl"] = os.path.join(save_directory, "%(title)s.%(ext)s")

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            video_title = clean_video_title(info_dict["title"])

            if video_title in downloaded_titles:
                display_message("Skipping duplicate video", video_title, text_area)
                return

            downloaded_titles.add(video_title)
            display_message("Download completed!", video_title, text_area)
            update_progress_bar(
                100, current_video, progress_var, progress_bar, progress_label, window
            )

    except Exception as e:
        error_message = f"An error has occurred: {str(e)}"
        logging.error(f"{error_message}\n{traceback.format_exc()}")
        display_message(error_message, "", text_area)


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
        threading.Thread(
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
        ).start()
    except Exception as e:
        logging.error(f"An error has occurred: {str(e)}")
        display_message(f"An error has occurred: {str(e)}", "", text_area)


# Function to save valid URLs to a file
def save_valid_urls(valid_video_urls, save_directory):
    valid_urls_file = os.path.join(save_directory, "valid_video_urls.txt")
    try:
        with open(valid_urls_file, "w") as f:
            for url in valid_video_urls:
                f.write(f"{url}\n")
    except Exception as e:
        logging.error(f"Failed to save valid URLs: {e}")


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
        logging.info(f"Processing playlist: {playlist_link}")

        ydl_opts = get_ydl_opts_playlist(download_type)

        with YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(playlist_link, download=False)

            if (
                not playlist_info
                or "entries" not in playlist_info
                or not playlist_info["entries"]
            ):
                display_message("No videos found in the playlist.", "", text_area)
                return

            valid_video_urls = [
                entry["url"]
                for entry in playlist_info["entries"]
                if entry and "url" in entry
            ]

            if not valid_video_urls:
                display_message("No valid videos found in the playlist.", "", text_area)
                return

            save_valid_urls(valid_video_urls, save_directory)

            total_videos = len(valid_video_urls)
            downloaded_titles = set()

            for current_video, video_url in enumerate(valid_video_urls, start=1):
                try:
                    download_single_video(
                        video_url,
                        download_type,
                        save_directory,
                        current_video,
                        downloaded_titles,
                        text_area,
                        progress_var,
                        progress_bar,
                        progress_label,
                        window,
                    )
                except Exception as e:
                    logging.error(f"Error downloading video {video_url}: {e}")
                    display_message(f"Failed to download: {video_url}", "", text_area)

                update_progress_bar(
                    (current_video / total_videos) * 100,
                    current_video,
                    progress_var,
                    progress_bar,
                    progress_label,
                    window,
                )

            display_message("Playlist download completed!", "", text_area)

    except Exception as e:
        logging.error(f"An error has occurred: {str(e)}\n{traceback.format_exc()}")
        display_message(f"An error has occurred: {str(e)}", "", text_area)
