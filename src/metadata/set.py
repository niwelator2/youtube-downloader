import json
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, ID3NoHeaderError, APIC
from mutagen.mp4 import MP4, MP4Cover
import requests


def save_metadata(file_path, info, download_type):
    metadata = {
        "title": info["title"],
        "uploader": info["uploader"],
        "album": info.get("album", ""),
        "genre": info.get("genre", ""),
        "upload_date": info.get("upload_date", ""),
        "description": info.get("description", ""),
        "thumbnail": info.get("thumbnail", ""),
    }

    metadata_json = json.dumps(metadata, indent=4)

    # MP3 Handling
    if download_type == "MP3":
        try:
            # Load the MP3 file with EasyID3 for metadata tags manipulation
            audio = MP3(file_path, ID3=EasyID3)
        except ID3NoHeaderError:
            # If no ID3 header, add one
            audio = MP3(file_path)
            audio.add_tags()

        # Set the metadata tags using EasyID3
        audio["title"] = info["title"]
        audio["artist"] = info["uploader"]
        audio["album"] = info.get("album", "")
        audio["genre"] = info.get("genre", "")
        audio["date"] = info.get("upload_date", "")
        audio.save()

        # Add cover art using ID3's APIC frame
        if metadata["thumbnail"]:
            try:
                # Fetch cover image data
                cover_data = requests.get(metadata["thumbnail"]).content

                # Open the file with ID3 for adding cover art
                id3 = ID3(file_path)

                # Create APIC frame for cover art and add it to the tags
                apic = APIC(
                    encoding=3,  # UTF-8 encoding
                    mime="image/jpeg",  # MIME type for the image (JPEG)
                    type=3,  # Front cover
                    desc="Cover",
                    data=cover_data,
                )

                # Add the APIC frame (cover art) to the ID3 tags
                id3.add(apic)
                id3.save()

            except Exception as e:
                print(f"Error adding cover art to MP3: {e}")

    # MP4 Handling
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
