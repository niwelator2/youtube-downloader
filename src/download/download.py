import os
import threading
import queue
import time
import traceback
import logging
import tkinter as tk
from yt_dlp import YoutubeDL
from utils.utils import clean_video_title
from utils.ydl_opts import (
    get_ydl_opts_playlist,
    get_ydl_opts_single_mp3,
    get_ydl_opts_single_mp4,
)

logging.basicConfig(
    filename="download.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Thread-safe queue for UI updates
message_queue = queue.Queue()

def log_message(message):
    """Logs messages and adds them to queue for UI updates."""
    logging.info(message)
    message_queue.put(message)

def update_text_area(text_area):
    """Fetch messages from the queue and display them in the UI."""
    while not message_queue.empty():
        message = message_queue.get()
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, f"{message}\n")
        text_area.see(tk.END)
        text_area.config(state=tk.DISABLED)
        message_queue.task_done()

def update_progress_bar(percent, progress_var, progress_bar, progress_label):
    """Efficiently update the progress bar in the UI."""
    progress_var.set(percent)
    progress_bar["value"] = percent
    progress_label.config(text=f"Progress: {percent:.2f}%")

def download_single_video(link, download_type, save_directory, downloaded_titles, text_area, progress_var, progress_bar, progress_label):
    """Downloads a single video and updates UI progress."""
    ydl_opts = get_ydl_opts_single_mp3 if download_type == "MP3" else get_ydl_opts_single_mp4
    
    ydl_opts = ydl_opts(text_area)
    ydl_opts["progress_hooks"] = [lambda d: update_progress_bar((d["downloaded_bytes"] / d["total_bytes"]) * 100 if d.get("total_bytes") else 0, progress_var, progress_bar, progress_label)]
    ydl_opts["outtmpl"] = os.path.join(save_directory, "%(title)s.%(ext)s")

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            video_title = clean_video_title(info_dict["title"])

            if video_title in downloaded_titles:
                log_message(f"Skipping duplicate video: {video_title}")
                return

            downloaded_titles.add(video_title)
            log_message(f"Download completed: {video_title}")
            update_progress_bar(100, progress_var, progress_bar, progress_label)

    except Exception as e:
        log_message(f"Error downloading {link}: {str(e)}\n{traceback.format_exc()}")

def download_playlist_threaded(playlist_link, download_type, save_directory, text_area, progress_var, progress_bar, progress_label):
    """Handles playlist download in a separate thread."""
    threading.Thread(target=start_download_playlist_threaded_inner, args=(playlist_link, download_type, save_directory, text_area, progress_var, progress_bar, progress_label)).start()

def start_download_playlist_threaded_inner(playlist_link, download_type, save_directory, text_area, progress_var, progress_bar, progress_label):
    """Processes and downloads videos from a playlist."""
    try:
        ydl_opts = get_ydl_opts_playlist(download_type)

        with YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(playlist_link, download=False)
            valid_video_urls = [entry["url"] for entry in playlist_info["entries"] if entry and "url" in entry]

        if not valid_video_urls:
            log_message("No valid videos found in the playlist.")
            return

        downloaded_titles = set()
        total_videos = len(valid_video_urls)

        for current_video, video_url in enumerate(valid_video_urls, start=1):
            try:
                download_single_video(video_url, download_type, save_directory, downloaded_titles, text_area, progress_var, progress_bar, progress_label)
            except Exception as e:
                log_message(f"Failed to download {video_url}: {str(e)}")

            update_progress_bar((current_video / total_videos) * 100, progress_var, progress_bar, progress_label)

        log_message("Playlist download completed!")

    except Exception as e:
        log_message(f"Error processing playlist: {str(e)}\n{traceback.format_exc()}")