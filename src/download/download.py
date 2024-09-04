import os
import threading
import queue
from pytube import YouTube, Playlist
from utils.utils import show_error_message, clean_video_title
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
download_queue = queue.Queue()


# Function to display messages in the UI
def display_message(message, video_title, text_area):
    message_queue.put((message, video_title))
    threading.Thread(target=display_messages_from_queue, args=(text_area,)).start()


def display_messages_from_queue(text_area):
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
    def on_progress(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        progress_var.set(percentage_of_completion)
        progress_bar.update()
        progress_label.config(
            text=f"Downloading {current_video}: {percentage_of_completion:.2f}%"
        )
        window.update_idletasks()

    try:
        youtube_object = YouTube(link, on_progress_callback=on_progress)

        video_title = clean_video_title(youtube_object.title)

        if youtube_object.age_restricted:
            display_message("This video is age-restricted. Skipping.", "", text_area)
            return

        if video_title in downloaded_titles:
            display_message("Skipping duplicate video", "", text_area)
            return

        downloaded_titles.add(video_title)

        if download_type == "MP4":
            video_file_path = os.path.join(save_directory, f"{video_title}.mp4")
            if os.path.exists(video_file_path):
                display_message(f"Video already exists.", f"{video_title}", text_area)
                return

            stream = youtube_object.streams.get_highest_resolution()
            display_message(f"Downloading video", f"{video_title}", text_area)
            video_file = stream.download(
                output_path=save_directory, filename=video_title
            )

            # Rename and set metadata
            new_file = os.path.join(save_directory, f"{video_title}.mp4")
            os.rename(video_file, new_file)
            metadata = extract_metadata(youtube_object)
            set_mp4_metadata(new_file, metadata)

        elif download_type == "MP3":
            audio_file_path = os.path.join(save_directory, f"{video_title}.mp3")
            if os.path.exists(audio_file_path):
                display_message(
                    f"Audio already exists. Skipping", f"{video_title}", text_area
                )
                return

            stream = youtube_object.streams.filter(only_audio=True).first()
            display_message("Downloading video", f"{video_title}", text_area)
            audio_file = stream.download(
                output_path=save_directory, filename=video_title
            )

            # Rename and set metadata
            new_file = os.path.join(save_directory, f"{video_title}.mp3")
            os.rename(audio_file, new_file)
            metadata = extract_metadata(youtube_object)
            set_mp3_metadata(new_file, metadata)

        else:
            display_message(
                "Invalid download type. Choose 'MP4' or 'MP3'.", "", text_area
            )
            show_error_message("Invalid download type. Choose 'MP4' or 'MP3'.")
            return

        display_message("Download completed!", f"{video_title}", text_area)
        update_progress_bar(
            100, current_video, progress_var, progress_bar, progress_label, window
        )

    except Exception as e:
        error_message = f"An error has occurred: {str(e)}"
        logging.error(error_message)
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


# Metadata extraction and setting functions
def extract_metadata(youtube_object):
    metadata = {
        "Title": youtube_object.title or "",
        "Length (seconds)": youtube_object.length or 0,
        "Views": youtube_object.views or 0,
        "Age Restricted": youtube_object.age_restricted or False,
        "Rating": round(youtube_object.rating, 2) if youtube_object.rating else None,
        "Description": youtube_object.description or "",
        "Publish Date": (
            str(youtube_object.publish_date) if youtube_object.publish_date else ""
        ),
        "Author": youtube_object.author or "",
    }
    return metadata


def set_mp3_metadata(file_path, metadata):
    try:
        import taglib

        audio_file = taglib.File(file_path)
        audio_file.tags["TITLE"] = [metadata["Title"]]
        audio_file.tags["ARTIST"] = [metadata["Author"]]
        audio_file.tags["COMMENT"] = [metadata["Description"]]
        audio_file.tags["DATE"] = [metadata["Publish Date"]]
        audio_file.tags["TRACKNUMBER"] = [str(metadata["Length (seconds)"])]
        if metadata["Rating"] is not None:
            audio_file.tags["RATING"] = [str(metadata["Rating"])]
        audio_file.tags["VIEWS"] = [str(metadata["Views"])]
        audio_file.save()
        logging.info(f"Metadata set successfully for {file_path}")
    except Exception as e:
        error_message = f"Failed to set metadata for {file_path}: {str(e)}"
        logging.error(error_message)
        show_error_message(error_message)


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
            "-y",  # Overwrite output files without asking
            f"{file_path}_temp.mp4",
        ]

        subprocess.run(ffmpeg_cmd, check=True)

        os.remove(file_path)
        os.rename(f"{file_path}_temp.mp4", file_path)
        logging.info(f"Metadata set successfully for {file_path}")

    except FileNotFoundError as fnf_error:
        logging.error(fnf_error)
        show_error_message(str(fnf_error))
    except subprocess.CalledProcessError as cpe_error:
        logging.error(f"FFmpeg failed to set metadata: {cpe_error}")
        show_error_message(f"FFmpeg failed to set metadata: {cpe_error}")
    except Exception as e:
        logging.error(f"Failed to set metadata: {e}")
        show_error_message(f"Failed to set metadata: {e}")
