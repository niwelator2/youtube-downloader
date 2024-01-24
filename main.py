import os
import threading
from pytube import YouTube, Playlist
import tkinter as tk
from tkinter import (
    ttk,
    Label,
    Entry,
    Button,
    OptionMenu,
    StringVar,
    DoubleVar,
    filedialog,
)

current_count = 0
total_count = 0

def on_progress(stream, chunk, bytes_remaining, current_video):
    global current_count, total_count
    bytes_downloaded = stream.filesize - bytes_remaining
    percent = (bytes_downloaded / stream.filesize) * 100
    current_count = current_count + 1
    total_count = total_count + 1
    update_progress_bar(percent, current_count, total_count, current_video)

def update_progress_bar(percent, current_count, total_count, current_video):
    progress_var.set(percent)
    progress_bar["value"] = percent
    progress_label.config(text=f"Progress: {percent:.2f}% ({current_count}/{total_count} videos, Video {current_video})")
    window.update_idletasks()

def clean_video_title(title):
    return "".join(c if c.isalnum() or c in [" ", "_", "-"] else "_" for c in title)

def download_single_video(link, download_type, save_directory, current_video):
    try:
        youtube_object = YouTube(link, on_progress_callback=on_progress)
        video_title = clean_video_title(youtube_object.title)

        if download_type == "MP4":
            stream = youtube_object.streams.get_highest_resolution()
            print("Downloading video:", video_title)
            video_file = stream.download(
                output_path=save_directory, filename=video_title
            )
            new_file = os.path.join(save_directory, f"{video_title}.mp4")
            os.rename(video_file, new_file)

        elif download_type == "MP3":
            stream = youtube_object.streams.filter(only_audio=True).first()
            print("Downloading audio (MP3):", video_title)
            audio_file = stream.download(
                output_path=save_directory, filename=video_title
            )
            new_file = os.path.join(save_directory, f"{video_title}.mp3")
            os.rename(audio_file, new_file)

        else:
            print("Invalid download type. Choose 'MP4' or 'MP3'.")
            return

        print("Download completed!")

    except Exception as e:
        print(f"An error has occurred: {str(e)}")

def download_playlist():
    link = playlist_link_entry.get()
    save_directory = playlist_save_directory_entry.get() or os.getcwd()
    playlist = Playlist(link)
    total_videos = len(playlist.video_urls)

    for index, video_url in enumerate(playlist.video_urls, start=1):
        download_single_video(
            video_url, download_type_playlist_var.get(), save_directory
        )
        percent_complete = (index / total_videos) * 100
        update_progress_bar(percent_complete, index, total_videos)

    print("Playlist download completed!")

def select_save_directory(entry_widget):
    directory = filedialog.askdirectory()
    if directory:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, directory)

def download_single_video_threaded(link, download_type, save_directory):
    download_single_video(link, download_type, save_directory)

def download_playlist_threaded():
    download_playlist()

def start_download_single_video_thread():
    link = link_entry.get()
    download_type = download_type_var.get()
    save_directory = save_directory_entry.get() or os.getcwd()

    # Create a new thread for the download
    download_thread = threading.Thread(
        target=download_single_video_threaded,
        args=(link, download_type, save_directory),
    )

    # Start the thread
    download_thread.start()

def start_download_playlist_thread():
    # Create a new thread for the playlist download
    playlist_download_thread = threading.Thread(
        target=download_playlist_threaded,
    )

    # Start the thread
    playlist_download_thread.start()

# Create the main window
window = tk.Tk()
window.title("YouTube Downloader")
window.geometry("800x300")

# Create a Label to display progress
progress_var = DoubleVar()
progress_label = Label(window, text="Progress: 0.00%")
progress_label.pack(pady=10)

# Create and pack GUI elements with styling
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12))
style.configure("TEntry", font=("Helvetica", 12))
style.configure("TMenubutton", font=("Helvetica", 12))

# Left section for single video download
left_frame = ttk.Frame(window)
left_frame.pack(side="left", padx=20)

Label(left_frame, text="YouTube URL:").pack(pady=10)
link_entry = Entry(left_frame, width=50)
link_entry.pack()

Label(left_frame, text="Download Type:").pack()
download_type_var = StringVar(left_frame)
download_type_var.set("MP4")
download_type_menu = OptionMenu(left_frame, download_type_var, "MP4", "MP3")
download_type_menu.pack()

Label(left_frame, text="Save Directory:").pack()
save_directory_entry = Entry(left_frame, width=50)
save_directory_entry.pack()

select_directory_button = Button(
    left_frame,
    text="Select Directory",
    command=lambda: select_save_directory(save_directory_entry),
)
select_directory_button.pack()

download_button = Button(
    left_frame, text="Download Single Video", command=start_download_single_video_thread
)
download_button.pack()

# Right section for playlist download
right_frame = ttk.Frame(window)
right_frame.pack(side="right", padx=20)

Label(right_frame, text="YouTube Playlist URL:").pack(pady=10)
playlist_link_entry = Entry(right_frame, width=50)
playlist_link_entry.pack()

Label(right_frame, text="Download Type:").pack()
download_type_playlist_var = StringVar(right_frame)
download_type_playlist_var.set("MP4")
download_type_menu = OptionMenu(right_frame, download_type_playlist_var, "MP4", "MP3")
download_type_menu.pack()

Label(right_frame, text="Save Directory:").pack()
playlist_save_directory_entry = Entry(right_frame, width=50)
playlist_save_directory_entry.pack()

select_playlist_directory_button = Button(
    right_frame,
    text="Select Directory",
    command=lambda: select_save_directory(playlist_save_directory_entry),
)
select_playlist_directory_button.pack()

download_button2 = Button(
    right_frame, text="Download Playlist", command=start_download_playlist_thread
)
download_button2.pack()

# Progress bar
progress_bar = ttk.Progressbar(
    window, length=200, mode="determinate", variable=progress_var
)
progress_bar.pack(pady=10)

# Start the Tkinter main loop
window.mainloop()