import os
from utils.utils import on_progress, select_save_directory

# Function to get the save directory from the entry widget
def get_save_directory(entry_widget):
    return entry_widget.get()

# Single video MP3 options with cookies
def get_ydl_opts_single_mp3(entry_widget, cookies_path=None):
    ydl_opts = {
        "outtmpl": os.path.join(get_save_directory(entry_widget), "%(title)s.%(ext)s"),
        "progress_hooks": [on_progress],
        "format": "bestaudio[ext=m4a]/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            },
        ],
        "noplaylist": True,
    }
    
    return ydl_opts

# Single video MP4 options with cookies
def get_ydl_opts_single_mp4(entry_widget, cookies_path=None):
    ydl_opts = {
        "outtmpl": os.path.join(get_save_directory(entry_widget), "%(title)s.%(ext)s"),
        "progress_hooks": [on_progress],
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
        "noplaylist": True,
    }
    return ydl_opts

def get_ydl_opts_playlist(download_type):
    """
    Returns yt-dlp options for downloading playlists in the specified format.

    :param download_type: The format of the download, either "MP3" or "MP4".
    :return: A dictionary containing yt-dlp options.
    """
    if download_type == "MP3":
        ydl_opts = {
            "format": "bestaudio[ext=m4a]/best",
            "outtmpl": "%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s",
            "progress_hooks": [on_progress],
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                },
            ],
            "noplaylist": False,  # Ensure the entire playlist is downloaded
        }
    elif download_type == "MP4":
        ydl_opts = {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
            "outtmpl": "%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s",
            "progress_hooks": [on_progress],
            "noplaylist": False,  # Ensure the entire playlist is downloaded
        }
    else:
        raise ValueError("Invalid download type. Use 'MP3' or 'MP4'.")

    return ydl_opts

