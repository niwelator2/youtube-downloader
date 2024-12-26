import os


def get_ydl_opts(download_type, save_directory, on_progress=None):
    """
    Generates the options for YouTube-DLP based on the download type.

    Args:
        download_type (str): Either "MP3" or "MP4".
        save_directory (str): The directory where the downloaded files will be saved.
        on_progress (function): A callback function for tracking download progress.

    Returns:
        dict: The options for YouTube-DLP.
    """
    if download_type == "MP3":
        return {
            "outtmpl": os.path.join(save_directory, "%(title)s.%(ext)s"),
            "format": "bestaudio/best",
            "progress_hooks": [on_progress] if on_progress else [],
            "noplaylist": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }
    elif download_type == "MP4":
        return {
            "outtmpl": os.path.join(save_directory, "%(title)s.%(ext)s"),
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "progress_hooks": [on_progress] if on_progress else [],
            "noplaylist": True,
        }
    else:
        raise ValueError(f"Invalid download type: {download_type}")
