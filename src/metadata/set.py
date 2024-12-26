import tkinter as tk
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4, MP4Cover
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TCON, TDRC, COMM
import requests


# Function to save metadata to the downloaded file
def save_metadata(file_path, info, download_type):
    if download_type == "MP3":
        audio = MP3(file_path, ID3=ID3)
        # Add ID3 tag if it doesn't exist
        audio.add_tags()

        audio["TIT2"] = TIT2(encoding=3, text=info["title"])
        audio["TPE1"] = TPE1(encoding=3, text=info["uploader"])
        audio["TALB"] = TALB(encoding=3, text=info.get("album", ""))
        audio["TCON"] = TCON(encoding=3, text=info.get("genre", ""))
        audio["TDRC"] = TDRC(encoding=3, text=info.get("upload_date", ""))
        audio["COMM"] = COMM(encoding=3, text=info.get("description", ""))
        audio.save()
    elif download_type == "MP4":
        video = MP4(file_path)
        video["\xa9nam"] = info["title"]
        video["\xa9ART"] = info["uploader"]
        video["\xa9alb"] = info.get("album", "")
        video["\xa9gen"] = info.get("genre", "")
        video["\xa9day"] = info.get("upload_date", "")
        video["desc"] = info.get("description", "")

        # Add cover art if available
        if "thumbnail" in info:
            cover_data = requests.get(info["thumbnail"]).content
            video["covr"] = [MP4Cover(cover_data, imageformat=MP4Cover.FORMAT_JPEG)]

        video.save()
