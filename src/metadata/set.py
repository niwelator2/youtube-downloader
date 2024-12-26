import json
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, ID3NoHeaderError, COMM
from mutagen.mp4 import MP4, MP4Cover
import requests

# Function to save metadata to the downloaded file and print to console
def save_metadata(file_path, info, download_type):
    metadata = {
        "title": info["title"],
        "uploader": info["uploader"],
        "album": info.get("album", ""),
        "genre": info.get("genre", ""),
        "upload_date": info.get("upload_date", ""),
        "description": info.get("description", ""),
        "thumbnail": info.get("thumbnail", "")
    }
    
    metadata_json = json.dumps(metadata, indent=4)
    
    # Print metadata to console
    #print(f"Metadata for {file_path}:")
    #print(metadata_json)

    if download_type == "MP3":
        try:
            audio = MP3(file_path, ID3=EasyID3)
        except ID3NoHeaderError:
            audio = MP3(file_path)
            audio.add_tags()

        # Clear existing tags to avoid conflicts
        for tag in audio.keys():
            del audio[tag]

        # Set new tags
        audio["title"] = info["title"]
        audio["artist"] = info["uploader"]
        audio["album"] = info.get("album", "")
        audio["genre"] = info.get("genre", "")
        audio["date"] = info.get("upload_date", "")
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
        
        # Embed metadata JSON as a custom tag
        video["\xa9cmt"] = metadata_json
        video.save()
