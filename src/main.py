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
    messagebox,
)

update_interval = 1


def on_progress(stream, chunk, bytes_remaining, current_video):
    bytes_downloaded = stream.filesize - bytes_remaining
    percent = (bytes_downloaded / stream.filesize) * 100
    update_progress_bar(percent, current_video)


def update_progress_bar(percent, current_video):
    progress_var.set(percent)
    progress_bar["value"] = percent
    progress_label.config(text=f"Progress: {percent:.2f}% (Video {current_video})")
    window.update_idletasks()


def clean_video_title(title):
    return "".join(c if c.isalnum() or c in [" ", "_", "-"] else "_" for c in title)


def show_error_message(message):
    messagebox.showerror("Error", message)

def download_single_video(
    link, download_type, save_directory, current_video, downloaded_titles
):
    try:
        youtube_object = YouTube(
            link,
            on_progress_callback=lambda stream, chunk, bytes_remaining: on_progress(
                stream, chunk, bytes_remaining, current_video
            ),
        )
        video_title = clean_video_title(youtube_object.title)

        if video_title in downloaded_titles:
            print(f"Skipping duplicate video: {video_title}")
            messagebox.showinfo("Duplicate Video", f"Skipping duplicate video: {video_title}")
            return

        downloaded_titles.add(video_title)

        if download_type == "MP4":
            video_file_path = os.path.join(save_directory, f"{video_title}.mp4")
            if os.path.exists(video_file_path):
                print(f"Video '{video_title}' already exists. Skipping.")
                messagebox.showinfo("Video Already Exists", f"Video '{video_title}' already exists. Skipping.")
                return
            stream = youtube_object.streams.get_highest_resolution()
            print("Downloading video:", video_title)
            video_file = stream.download(
                output_path=save_directory, filename=video_title
            )
            new_file = os.path.join(save_directory, f"{video_title}.mp4")
            os.rename(video_file, new_file)

        elif download_type == "MP3":
            audio_file_path = os.path.join(save_directory, f"{video_title}.mp3")
            if os.path.exists(audio_file_path):
                print(f"Audio '{video_title}' already exists. Skipping.")
                messagebox.showinfo("Audio Already Exists", f"Audio '{video_title}' already exists. Skipping.")
                return
            stream = youtube_object.streams.filter(only_audio=True).first()
            print("Downloading audio (MP3):", video_title)
            audio_file = stream.download(
                output_path=save_directory, filename=video_title
            )
            new_file = os.path.join(save_directory, f"{video_title}.mp3")
            os.rename(audio_file, new_file)

        else:
            error_message = "Invalid download type. Choose 'MP4' or 'MP3'."
            show_error_message(error_message)
            return

        print("Download completed!")
        update_progress_bar(100, current_video)

    except Exception as e:
        error_message = f"An error has occurred: {str(e)}"
        show_error_message(error_message)


def download_playlist(playlist_link, download_type, save_directory):
    current_video = 1
    playlist = Playlist(playlist_link)
    total_videos = len(playlist.video_urls)

    for video_url in playlist.video_urls:
        download_single_video(video_url, download_type, save_directory, current_video)
        current_video += 1
        percent_complete = (current_video / total_videos) * 100
        update_progress_bar(percent_complete, current_video)

    print("Playlist download completed!")


def select_save_directory(entry_widget, initial_dir=None):
    directory = filedialog.askdirectory(initialdir=initial_dir)
    if directory:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, directory)
        set_last_directory(directory)


def set_last_directory(directory):
    with open(".last_directory", "w") as f:
        f.write(directory)


def load_last_directory():
    try:
        with open(".last_directory", "r") as f:
            return f.read()
    except FileNotFoundError:
        return None


def download_single_video_threaded(link, download_type, save_directory, current_video):
    try:
        download_single_video(link, download_type, save_directory, current_video, set())
    except Exception as e:
        error_message = f"An error has occurred: {str(e)}"
        show_error_message(error_message)


def download_playlist_threaded(playlist_link, download_type, save_directory):
    try:
        playlist_download_thread = threading.Thread(
            target=start_download_playlist_threaded_inner,
            args=(playlist_link, download_type, save_directory),
        )
        playlist_download_thread.start()
    except Exception as e:
        error_message = f"An error has occurred: {str(e)}"
        show_error_message(error_message)


def start_download_playlist_threaded_inner(
    playlist_link, download_type, save_directory
):
    playlist = Playlist(playlist_link)
    total_videos = len(playlist.video_urls)
    current_video = 1  # Start from 1 for better user experience
    for video_url in playlist.video_urls:
        download_single_video(
            video_url, download_type, save_directory, current_video, set()
        )
        percent_complete = (current_video / total_videos) * 100
        update_progress_bar(percent_complete, current_video)
        current_video += 1  # Increment after downloading each video

    print("Playlist download completed!")


# Create the main window
window = tk.Tk()
window.title("YouTube Downloader")
window.geometry("800x300")

# Set the icon for app
# window.iconbitmap("./logo.ico")

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
    command=lambda: select_save_directory(save_directory_entry, load_last_directory()),
)
select_directory_button.pack()

download_button = Button(
    left_frame,
    text="Download Single Video",
    command=lambda: download_single_video_threaded(
        link_entry.get(), download_type_var.get(), save_directory_entry.get(), 1
    ),
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
    command=lambda: select_save_directory(
        playlist_save_directory_entry, load_last_directory()
    ),
)
select_playlist_directory_button.pack()

download_button2 = Button(
    right_frame,
    text="Download Playlist",
    command=lambda: download_playlist_threaded(
        playlist_link_entry.get(),
        download_type_playlist_var.get(),
        playlist_save_directory_entry.get(),
    ),
)
download_button2.pack()

# Progress bar
progress_bar = ttk.Progressbar(
    window, length=200, mode="determinate", variable=progress_var
)
progress_bar.pack(pady=10)

last_directory = load_last_directory()
if last_directory:
    save_directory_entry.insert(0, last_directory)
    playlist_save_directory_entry.insert(0, last_directory)

# Start the Tkinter main loop
window.mainloop()
