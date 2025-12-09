import os


# Single video MP3 options
def get_ydl_opts_single_mp3(save_directory, progress_hook):
    """
    Returns yt-dlp options for downloading a single video as MP3.
    
    :param save_directory: Directory where the file will be saved
    :param progress_hook: Callback function for progress updates
    :return: A dictionary containing yt-dlp options
    """
    ydl_opts = {
        "outtmpl": os.path.join(save_directory, "%(title)s.%(ext)s"),
        "progress_hooks": [progress_hook],
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


# Single video MP4 options
def get_ydl_opts_single_mp4(save_directory, progress_hook):
    """
    Returns yt-dlp options for downloading a single video as MP4.
    
    :param save_directory: Directory where the file will be saved
    :param progress_hook: Callback function for progress updates
    :return: A dictionary containing yt-dlp options
    """
    ydl_opts = {
        "outtmpl": os.path.join(save_directory, "%(title)s.%(ext)s"),
        "progress_hooks": [progress_hook],
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
        "noplaylist": True,
    }
    return ydl_opts


def get_ydl_opts_playlist(download_type, save_directory, progress_hook):
    """
    Returns yt-dlp options for downloading playlists in the specified format.

    :param download_type: The format of the download, either "MP3" or "MP4".
    :param save_directory: Directory where the playlist will be saved
    :param progress_hook: Callback function for progress updates
    :return: A dictionary containing yt-dlp options.
    """
    if download_type == "MP3":
        ydl_opts = {
            "format": "bestaudio[ext=m4a]/best",
            "outtmpl": os.path.join(save_directory, "%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s"),
            "progress_hooks": [progress_hook],
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
            "outtmpl": os.path.join(save_directory, "%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s"),
            "progress_hooks": [progress_hook],
            "noplaylist": False,  # Ensure the entire playlist is downloaded
        }
    else:
        raise ValueError("Invalid download type. Use 'MP3' or 'MP4'.")

    return ydl_opts
