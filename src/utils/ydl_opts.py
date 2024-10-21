import os

# Single video MP3 options
ydl_opts_single_mp3 = {
    "outtmpl": os.path.join(save_directory, "%(title)s.%(ext)s"),
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

# Single video MP4 options
ydl_opts_single_mp4 = {
    "outtmpl": os.path.join(save_directory, "%(title)s.%(ext)s"),
    "progress_hooks": [on_progress],
    "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
    "noplaylist": True,
}

# Playlist (multiple videos) MP3 options
ydl_opts_multi_mp3 = {
    "outtmpl": os.path.join(save_directory, "%(title)s.%(ext)s"),
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

# Playlist (multiple videos) MP4 options
ydl_opts_multi_mp4 = {
    "outtmpl": os.path.join(save_directory, "%(title)s.%(ext)s"),
    "progress_hooks": [on_progress],
    "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
    "noplaylist": False,
}
