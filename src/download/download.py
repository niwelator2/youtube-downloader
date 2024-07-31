import os
import threading
import queue
from pytube import YouTube, Playlist
from download.metadata import extract_metadata, set_mp3_metadata, set_mp4_metadata
from utils.utils import show_error_message, clean_video_title
import tkinter as tk
import subprocess  # For handling MP4 metadata with ffmpeg

# Parameter to update progress bar
update_interval = 1
# Create a queue for message display
message_queue = queue.Queue()
download_queue = queue.Queue()


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


# def on_progress(
#     stream,
#     chunk,
#     bytes_remaining,
#     current_video,
#     progress_var,
#     progress_bar,
#     progress_label,
#     window,
# ):
#     bytes_downloaded = stream.filesize - bytes_remaining
#     percent = (bytes_downloaded / stream.filesize) * 100
#     update_progress_bar(
#         percent, current_video, progress_var, progress_bar, progress_label, window
#     )


def update_progress_bar(
    percent, current_video, progress_var, progress_bar, progress_label, window
):
    progress_var.set(percent)
    progress_bar["value"] = percent
    progress_label.config(text=f"Progress: {percent:.2f}% (Video {current_video})")
    window.update_idletasks()



def download_single_video(link, current_video, progress_var, progress_bar, progress_label, window):
    def on_progress(stream, chunk, bytes_remaining, current_video, progress_var, progress_bar, progress_label, window):
        # Implementation for updating progress (progress_var, progress_bar, etc.)
        # Example: Updating the progress bar and label
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        progress_var.set(percentage_of_completion)
        progress_bar.update()
        progress_label.config(text=f"Downloading {current_video}: {percentage_of_completion:.2f}%")
        window.update_idletasks()

    try:
        youtube_object = YouTube(
            link,
            on_progress_callback=lambda stream, chunk, bytes_remaining: on_progress(
                stream, chunk, bytes_remaining, current_video, progress_var, progress_bar, progress_label, window
            )
        )
        
        video_title = clean_video_title(youtube_object.title)
        
        if youtube_object.age_restricted:
            display_message(f"This video is age-restricted. Skipping.", "", text_area)
            return

        if video_title in downloaded_titles:
            display_message(f"Skipping duplicate video", "", text_area)
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
            new_file = os.path.join(save_directory, f"{video_title}.mp4")
            os.rename(video_file, new_file)

            # Save metadata for MP4
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
            metadata = extract_metadata(youtube_object)
            audio_file = stream.download(
                output_path=save_directory, filename=video_title
            )
            new_file = os.path.join(save_directory, f"{video_title}.mp3")
            os.rename(audio_file, new_file)

            # Save metadata for MP3
            set_mp3_metadata(new_file, metadata)

        else:
            display_message(
                f"Invalid download type. Choose 'MP4' or 'MP3'. ", "", text_area
            )
            error_message = "Invalid download type. Choose 'MP4' or 'MP3'."
            show_error_message(error_message)
            return

        display_message(f"Download completed!", f"{video_title}", text_area)
        update_progress_bar(
            100, current_video, progress_var, progress_bar, progress_label, window
        )

    except Exception as e:
        error_message = f"An error has occurred: {str(e)}"
        show_error_message(error_message)


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

        window.after(1000, lambda: check_download_progress(save_directory, text_area))
    except Exception as e:
        error_message = f"An error has occurred: {str(e)}"
        show_error_message(error_message)


def check_download_progress(save_directory, text_area, window):
    if os.listdir(save_directory):
        display_message(f"Start downloading playlist!", "", text_area)
    else:
        window.after(1000, lambda: check_download_progress(save_directory, text_area))


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
        show_error_message(error_message)


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
        current_video = 1

        for video_url in playlist.video_urls:
            download_single_video_threaded(
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
            percent_complete = (current_video / total_videos) * 100
            update_progress_bar(
                percent_complete,
                current_video,
                progress_var,
                progress_bar,
                progress_label,
                window,
            )
            current_video += 1

        display_message(f"Playlist download completed!", "", text_area)
    except Exception as e:
        error_message = f"An error has occurred: {str(e)}"
        show_error_message(error_message)
