import os
from pytube import YouTube
from tqdm import tqdm

def on_progress(stream, chunk, bytes_remaining):
    # Calculate the percentage of completion
    bytes_downloaded = stream.filesize - bytes_remaining
    percent = (bytes_downloaded / stream.filesize) * 100
    # Update the progress bar
    tqdm_instance.n = percent
    tqdm_instance.refresh()

def download_video(link, download_type, save_directory):
    try:
        youtube_object = YouTube(link, on_progress_callback=on_progress)
        video_title = youtube_object.title

        if download_type == 'mp4':
            stream = youtube_object.streams.get_highest_resolution()
            print("Downloading video:", video_title)
            video_file = stream.download(output_path=save_directory, filename=video_title)
            new_file = os.path.join(save_directory, f"{video_title}.mp4")
            os.rename(video_file, new_file)

        elif download_type == 'mp3':
            stream = youtube_object.streams.filter(only_audio=True).first()
            print("Downloading audio (MP3):", video_title)
            audio_file = stream.download(output_path=save_directory, filename=video_title)
            new_file = os.path.join(save_directory, f"{video_title}.mp3")
            os.rename(audio_file, new_file)

        elif download_type == 'audio':
            stream = youtube_object.streams.filter(only_audio=True).first()
            print("Downloading audio (without conversion):", video_title)
            audio_file = stream.download(output_path=save_directory, filename=video_title + ".mp4")
            new_file = os.path.join(save_directory, f"{video_title}.mp3")
            os.rename(audio_file, new_file)

        else:
            print("Invalid download type. Choose 'mp4', 'mp3', or 'audio'.")
            return

        print("Download completed!")
    except Exception as e:
        print("An error has occurred:", str(e))

if __name__ == "__main__":
    link = input("Enter the YouTube video URL: ")
    download_type = input("Choose download type ('mp4', 'mp3', or 'audio'): ").lower()
    save_directory = input("Enter the directory to save the downloaded files: ")

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Create the tqdm progress bar instance
    tqdm_instance = tqdm(total=100, unit='%', ascii=True)
    
    download_video(link, download_type, save_directory)
