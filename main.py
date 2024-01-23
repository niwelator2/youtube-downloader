import os
from pytube import YouTube, Playlist
import tkinter as tk
from tkinter import ttk, Label, Entry, Button, OptionMenu, StringVar, filedialog, Checkbutton


def on_progress(stream, chunk, bytes_remaining):
    bytes_downloaded = stream.filesize - bytes_remaining
    percent = (bytes_downloaded / stream.filesize) * 100
    update_progress_bar(percent)


def update_progress_bar(percent):
    progress_label.config(text=f"Progress: {percent:.2f}%")


def clean_video_title(title):
    return "".join(c if c.isalnum() or c in [" ", "_", "-"] else "_" for c in title)


def download_single_video(youtube_object, download_type, save_directory):
    video_title = clean_video_title(youtube_object.title)

    if download_type == "MP4":
        stream = youtube_object.streams.get_highest_resolution()
        print("Downloading video:", video_title)
        video_file = stream.download(output_path=save_directory, filename=video_title)
        new_file = os.path.join(save_directory, f"{video_title}.mp4")
        os.rename(video_file, new_file)

    elif download_type == "MP3":
        stream = youtube_object.streams.filter(only_audio=True).first()
        print("Downloading audio (MP3):", video_title)
        audio_file = stream.download(output_path=save_directory, filename=video_title)
        new_file = os.path.join(save_directory, f"{video_title}.mp3")
        os.rename(audio_file, new_file)

    else:
        print("Invalid download type. Choose 'MP4' or 'MP3'.")
        return

    print(f"Download of {video_title} completed!")


def download_playlist_videos(playlist_url, save_directory):
    playlist = Playlist(playlist_url)

    if not playlist.video_urls:
        print("Playlist is empty or invalid.")
        return

    if not save_directory:
        save_directory = playlist.title()

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    print(f"Downloading playlist: {playlist.title()}")

    for video_url in playlist.video_urls:
        try:
            video = YouTube(video_url, on_progress_callback=on_progress)
            download_single_video(video, download_type_var.get(), save_directory)
        except Exception as e:
            print(f"Error downloading video {video_url}: {str(e)}")

    print("Playlist download completed!")


def download_video():
    link = link_entry.get()
    save_directory = save_directory_entry.get()

    if "playlist?list=" in link and download_playlist_var.get():
        download_playlist_videos(link, save_directory)
    else:
        download_single_video(
            YouTube(link, on_progress_callback=on_progress),
            download_type_var.get(),
            save_directory,
        )


def select_save_directory():
    directory = filedialog.askdirectory()
    if directory:
        save_directory_entry.delete(0, tk.END)
        save_directory_entry.insert(0, directory)


# Create the main window
window = tk.Tk()
window.title("YouTube Downloader")
window.geometry("640x300")

# Create and pack GUI elements with styling
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12))
style.configure("TEntry", font=("Helvetica", 12))
style.configure("TMenubutton", font=("Helvetica", 12))

Label(window, text="YouTube URL:").pack(pady=10)
link_entry = Entry(window, width=50)
link_entry.pack()

Label(window, text="Download Type:").pack()
download_type_var = StringVar(window)
download_type_var.set("MP4")
download_type_menu = OptionMenu(window, download_type_var, "MP4", "MP3")
download_type_menu.pack()

Label(window, text="Save Directory:").pack()
save_directory_entry = Entry(window, width=50)
save_directory_entry.pack()

Label(window, text="Download Playlist:").pack()
download_playlist_var = tk.BooleanVar(window)
download_playlist_checkbox = Checkbutton(window, text="Download Entire Playlist", variable=download_playlist_var)
download_playlist_checkbox.pack()

Button(window, text="Select Directory", command=select_save_directory).pack()
download_button = Button(window, text="Download", command=download_video)
download_button.pack()

# Create a Label to display progress
progress_label = Label(window, text="Progress: 0.00%")
progress_label.pack(pady=10)

# Start the Tkinter main loop
window.mainloop()
