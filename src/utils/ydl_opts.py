import os
from utils.utils import on_progress, select_save_directory

# Function to get the save directory from the entry widget
def get_save_directory(entry_widget):
    return entry_widget.get()  # Retrieve the value from the entry widget

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

# Playlist (multiple videos) MP3 options with cookies
def get_ydl_opts_multi_mp3(entry_widget, cookies_path=None):
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
        "noplaylist": False,
    }    
    return ydl_opts

# Playlist (multiple videos) MP4 options with cookies
def get_ydl_opts_multi_mp4(entry_widget, cookies_path=None):
    ydl_opts = {
        "outtmpl": os.path.join(get_save_directory(entry_widget), "%(title)s.%(ext)s"),
        "progress_hooks": [on_progress],
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
        "noplaylist": False,
    }
    return ydl_opts
