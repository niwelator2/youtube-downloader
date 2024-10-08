import os
import threading
import queue
import time
from utils.utils import clean_video_title
from yt_dlp import YoutubeDL
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, ID3NoHeaderError, ID3FileType
from mutagen.easyid3 import EasyID3
import traceback

import tkinter as tk
import subprocess
import logging
from concurrent.futures import ThreadPoolExecutor

# Set up logging
logging.basicConfig(filename="download.log", level=logging.INFO)

# Parameter to update progress bar
update_interval = 1

# Create queues for message and download management
message_queue = queue.Queue()


# Function to display messages in the UI
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


# Function to update the progress bar in the UI
def update_progress_bar(
    percent, current_video, progress_var, progress_bar, progress_label, window
):
    progress_var.set(percent)
    progress_bar["value"] = percent
    progress_label.config(text=f"Progress: {percent:.2f}% (Video {current_video})")
    window.update_idletasks()


# Function to handle the download of a single video
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
        if d["status"] == "downloading":
            percent = d["downloaded_bytes"] / d["total_bytes"] * 100
            progress_var.set(percent)
            progress_bar.update()
            progress_label.config(text=f"Downloading {current_video}: {percent:.2f}%")
            window.update_idletasks()

    ydl_opts = {
    "outtmpl": os.path.join(save_directory, "%(title)s.%(ext)s"),
    "progress_hooks": [on_progress],
    "format": (
        "bestaudio[ext=mp3]" if download_type == "MP3" else "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]"
    ),  # Select MP3 for audio or MP4 for video
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "320",  # Set quality for MP3
        }
    ] if download_type == "MP3" else [],
    "noplaylist": False,
}

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            video_title = clean_video_title(info_dict["title"])

            if video_title in downloaded_titles:
                display_message("Skipping duplicate video", "", text_area)
                return

            downloaded_titles.add(video_title)

            # Handle MP3 metadata
            if download_type == "MP3":
                audio_file_path = os.path.join(save_directory, f"{video_title}.mp3")
                if os.path.exists(audio_file_path):
                    display_message(f"Audio already exists. Skipping", f"{video_title}", text_area)
                    return

                metadata = extract_metadata(info_dict)
                set_mp3_metadata(audio_file_path, metadata)

            # Handle MP4 metadata
            elif download_type == "MP4":
                video_file_path = os.path.join(save_directory, f"{video_title}.mp4")
                if os.path.exists(video_file_path):
                    display_message(f"Video already exists.", f"{video_title}", text_area)
                    return

                metadata = extract_metadata(info_dict)
                set_mp4_metadata(video_file_path, metadata)

            else:
                display_message("Invalid download type. Choose 'MP4' or 'MP3'.", "", text_area)
                return

            display_message("Download completed!", f"{video_title}", text_area)
            update_progress_bar(
                100, current_video, progress_var, progress_bar, progress_label, window
            )

    except Exception as e:
        error_message = f"An error has occurred: {str(e)}"
        logging.error(f"{error_message}\n{traceback.format_exc()}")



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
        window.after(
            1000, lambda: check_download_progress(save_directory, text_area, window)
        )
    except Exception as e:
        logging.error(f"An error has occurred: {str(e)}")
        display_message(f"An error has occurred: {str(e)}", "", text_area)


def check_download_progress(save_directory, text_area, window):
    if os.listdir(save_directory):
        display_message("Start downloading playlist!", "", text_area)
    else:
        window.after(
            1000, lambda: check_download_progress(save_directory, text_area, window)
        )


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
        threading.Thread(
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
        ).start()
    except Exception as e:
        logging.error(f"An error has occurred: {str(e)}")
        display_message(f"An error has occurred: {str(e)}", "", text_area)


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
        # Initialize YoutubeDL
        with YoutubeDL({}) as ydl:
            try:
                # Extract playlist info
                playlist_info = ydl.extract_info(playlist_link, download=False)
            except Exception as e:
                logging.error(f"Failed to extract playlist info: {str(e)}")
                display_message(f"Failed to extract playlist info: {str(e)}", "", text_area)
                return
            
            # Check for entries in playlist
            if "entries" not in playlist_info:
                display_message("No videos found in the playlist.", "", text_area)
                return
            
            playlist_video_urls = []
            for entry in playlist_info["entries"]:
                if entry and "url" in entry:
                    playlist_video_urls.append(entry["url"])
                else:
                    logging.warning(f"Entry missing 'url': {entry}")
                    display_message("Skipping entry due to missing URL", "", text_area)
        
        # Proceed with downloading videos
        total_videos = len(playlist_video_urls)
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
                for current_video, video_url in enumerate(playlist_video_urls, 1)
            ]
            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    display_message(f"Error in downloading: {str(e)}", "", text_area)

        display_message("Playlist download completed!", "", text_area)

    except Exception as e:
        logging.error(f"An error has occurred: {str(e)}")
        display_message(f"An error has occurred: {str(e)}", "", text_area)



# Metadata extraction and setting functions
def extract_metadata(info_dict):
    metadata = {
        "Title": info_dict.get("title", ""),
        "Length (seconds)": info_dict.get("duration", 0),
        "Views": info_dict.get("view_count", 0),
        "Age Restricted": info_dict.get("age_restricted", False),
        "Rating": info_dict.get("average_rating", None),
        "Description": info_dict.get("description", ""),
        "Publish Date": info_dict.get("upload_date", ""),
        "Author": info_dict.get("uploader", ""),
    }
    return metadata


def set_mp3_metadata(file_path, metadata):
    try:
        audio = MP3(file_path, ID3=EasyID3)
        audio["title"] = metadata["Title"]
        audio["artist"] = metadata["Author"]
        audio["album"] = metadata["Description"]
        audio["date"] = metadata["Publish Date"]
        audio["tracknumber"] = str(metadata["Length (seconds)"])
        if metadata["Rating"] is not None:
            audio["RATING"] = str(metadata["Rating"])
        audio["VIEWS"] = str(metadata["Views"])
        audio.save()
        logging.info(f"Metadata set successfully for {file_path}")
    except Exception as e:
        error_message = f"Failed to set metadata for {file_path}: {str(e)}"
        logging.error(error_message)


def set_mp4_metadata(file_path, metadata):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Input file {file_path} not found")

        ffmpeg_cmd = [
            "ffmpeg",
            "-i",
            file_path,
            "-c",
            "copy",  # Avoid re-encoding
            "-metadata",
            f'title={metadata["Title"]}',
            "-metadata",
            f'artist={metadata["Author"]}',
            "-metadata",
            f'date={metadata["Publish Date"]}',
            "-metadata",
            f'description={metadata["Description"]}',
            "-metadata",
            f'comment={metadata.get("Comments", "")}',  
            "-y",
            f"{file_path}_temp.mp4",
        ]

        subprocess.run(ffmpeg_cmd, check=True)

        os.remove(file_path)
        os.rename(f"{file_path}_temp.mp4", file_path)
        logging.info(f"Metadata set successfully for {file_path}")

    except FileNotFoundError as fnf_error:
        logging.error(fnf_error)

    except subprocess.CalledProcessError as cpe_error:
        logging.error(f"FFmpeg failed to set metadata: {cpe_error}")

    except Exception as e:
        logging.error(f"Failed to set metadata: {e}")
