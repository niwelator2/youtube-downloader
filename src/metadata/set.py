from mutagen.mp3 import MP3
from mutagen.id3 import ID3, ID3NoHeaderError, ID3FileType
from mutagen.easyid3 import EasyID3
import subprocess
# Metadata extraction and setting functions
def extract_metadata(info_dict):
    metadata = {
        "Title": info_dict.get("title", ""),
        "Length (seconds)": info_dict.get("duration", 0),
        "Views": info_dict.get("view_count", 0),
        "Age Restricted": info_dict.get("age_restricted", False),
        "Rating": info_dict.get("average_rating", None),
        "Description": info_dict.get("description", ""),
        "Publish Date": info_dict.get("upload_date", ""),
        "Author": info_dict.get("uploader", ""),
    }
    return metadata


def set_mp3_metadata(file_path, metadata):
    try:
        audio = MP3(file_path, ID3=EasyID3)
        audio["title"] = metadata["Title"]
        audio["artist"] = metadata["Author"]
        audio["album"] = metadata["Description"]
        audio["date"] = metadata["Publish Date"]
        audio["tracknumber"] = str(metadata["Length (seconds)"])
        if metadata["Rating"] is not None:
            audio["RATING"] = str(metadata["Rating"])
        audio["VIEWS"] = str(metadata["Views"])
        audio.save()
        logging.info(f"Metadata set successfully for {file_path}")
    except Exception as e:
        error_message = f"Failed to set metadata for {file_path}: {str(e)}"
        logging.error(error_message)
        show_error_message(error_message)


def set_mp4_metadata(file_path, metadata):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Input file {file_path} not found")

        ffmpeg_cmd = [
            "ffmpeg",
            "-i",
            file_path,
            "-c",
            "copy",  # Avoid re-encoding
            "-metadata",
            f'title={metadata["Title"]}',
            "-metadata",
            f'artist={metadata["Author"]}',
            "-metadata",
            f'date={metadata["Publish Date"]}',
            "-y",  # Overwrite output files without asking
            f"{file_path}_temp.mp4",
        ]

        subprocess.run(ffmpeg_cmd, check=True)

        os.remove(file_path)
        os.rename(f"{file_path}_temp.mp4", file_path)
        logging.info(f"Metadata set successfully for {file_path}")

    except FileNotFoundError as fnf_error:
        logging.error(fnf_error)
        show_error_message(str(fnf_error))
    except subprocess.CalledProcessError as cpe_error:
        logging.error(f"FFmpeg failed to set metadata: {cpe_error}")
        show_error_message(f"FFmpeg failed to set metadata: {cpe_error}")
    except Exception as e:
        logging.error(f"Failed to set metadata: {e}")
        show_error_message(f"Failed to set metadata: {e}")
