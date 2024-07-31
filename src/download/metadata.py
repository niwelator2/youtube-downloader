import os
import subprocess
import taglib

from utils.utils import show_error_message  # For handling MP3 metadata


def extract_metadata(youtube_object):
    metadata = {
        "Title": youtube_object.title or "",
        "Length (seconds)": youtube_object.length or 0,
        "Views": youtube_object.views or 0,
        "Age Restricted": youtube_object.age_restricted or False,
        "Rating": round(youtube_object.rating, 2) if youtube_object.rating else None,
        "Description": youtube_object.description or "",
        "Publish Date": (
            str(youtube_object.publish_date) if youtube_object.publish_date else ""
        ),
        "Author": youtube_object.author or "",
    }

    # metadata = { youtube_object.vid_info }



    return metadata


def set_mp3_metadata(file_path, metadata):
    try:
        audio_file = taglib.File(file_path)
        audio_file.tags["TITLE"] = [metadata["Title"]]
        audio_file.tags["ARTIST"] = [metadata["Author"]]
        audio_file.tags["COMMENT"] = [metadata["Description"]]
        audio_file.tags["DATE"] = [metadata["Publish Date"]]
        audio_file.tags["TRACKNUMBER"] = [str(metadata["Length (seconds)"])]
        if metadata["Rating"] is not None:
            audio_file.tags["RATING"] = [str(metadata["Rating"])]
        audio_file.tags["VIEWS"] = [str(metadata["Views"])]
        audio_file.save()
        print(f"Metadata set successfully for {file_path}")
    except Exception as e:
        error_message_setup_mp3_metadata = print(
            f"Failed to set metadata for {file_path}: {str(e)}"
        )
        show_error_message(error_message_setup_mp3_metadata)

def set_mp4_metadata(file_path, metadata):
    try:
        # Check if file exists
        print(file_path, metadata)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Input file {file_path} not found")

        # Construct the ffmpeg command
        ffmpeg_cmd = [
            "ffmpeg",
            "-i",
            file_path,
            "-metadata",
            f'title={metadata["Title"]}' if metadata["Title"] else "",
            "-metadata",
            f'artist={metadata["Author"]}' if metadata["Author"] else "",
            "-metadata",
            f'date={metadata["Publish Date"]}' if metadata["Publish Date"] else "",
            "-metadata",
            "copy",  # to avoid re-encoding
            f"{file_path}_temp.mp4",
        ]

        # Remove empty arguments
        ffmpeg_cmd = [arg for arg in ffmpeg_cmd if arg]

        # Run the ffmpeg command
        subprocess.run(ffmpeg_cmd, check=True)

        # Replace the original file with the updated file
        os.remove(file_path)
        os.rename(f"{file_path}_temp.mp4", file_path)

        print(f"Metadata set successfully for {file_path}")

    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except subprocess.CalledProcessError as cpe_error:
        print(f"FFmpeg failed to set metadata for {file_path}: {cpe_error}")
    except Exception as e:
        print(f"Failed to set metadata for {file_path}: {e}")


def save_metadata_to_file(metadata, save_directory, video_title):
    metadata_file_path = os.path.join(save_directory, f"{video_title}_metadata.txt")
    with open(metadata_file_path, "w") as f:
        for key, value in metadata.items():
            f.write(f"{key}: {value}\n")





# use vid_info 








