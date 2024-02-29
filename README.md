# YouTube Downloader

YouTube Downloader is a simple Python application that allows users to download single YouTube videos or entire playlists as MP4 or MP3 files.

## Features

- Download single YouTube videos by providing the video URL.
- Download entire YouTube playlists by providing the playlist URL.
- Choose between downloading videos as MP4 or extracting audio as MP3.
- Select the save directory for downloaded files.

## Dependencies

- [pytube](https://github.com/nficano/pytube): A lightweight, dependency-free Python library to fetch YouTube content.
- [plyer](https://github.com/kivy/plyer): A platform-independent API to access features commonly found on various platforms, including notifications.

## Installation

1. Clone the repository:


   ```bash
   git clone https://github.com/yourusername/youtube-downloader.git
   cd youtube-downloader
   cd windows/
   ./Youtube-Downloader.2.0_windows_x64_setup.exe
   ```
   
## Build 

    ```bash
    python -m venv venv
    pip install -r requirements.txt
    cd src/
    pyinstaller --onefile --distpath=../windows --icon=logo.ico --name=Youtube-Downloader -y -F --additional-hooks-dir=. --noconsole main.py
    ```


# License

This project is licensed under the MIT License. See the LICENSE file for details.
