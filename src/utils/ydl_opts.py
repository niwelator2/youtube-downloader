import os

ydl_opts_single= {
    "outtmpl": os.path.join(save_directory, "%(title)s.%(ext)s"),
    "progress_hooks": [on_progress],
    "format": "bestaudio[ext=m4a]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        },
    ],
    "noplaylist": False,
}

ydl_opts_multi = {
    "outtmpl": os.path.join(save_directory, "%(title)s.%(ext)s"),
    "progress_hooks": [on_progress],
    "format": "bestaudio[ext=m4a]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        },
    ],
    "noplaylist": False,
}