# YouTube Downloader

YouTube Downloader is a simple Python application that allows users to download single YouTube videos or entire playlists as MP4 or MP3 files.

## Features

- Download single YouTube videos by providing the video URL.
- Download entire YouTube playlists by providing the playlist URL.
- Choose between downloading videos as MP4 or extracting audio as MP3.
- Select the save directory for downloaded files.

## Dependencies

## Dependencies

- [altgraph](https://pypi.org/project/altgraph/) (0.17.4)
- [black](https://pypi.org/project/black/) (24.2.0)
- [click](https://pypi.org/project/click/) (8.1.7)
- [colorama](https://pypi.org/project/colorama/) (0.4.6)
- [mypy-extensions](https://pypi.org/project/mypy-extensions/) (1.0.0)
- [packaging](https://pypi.org/project/packaging/) (23.2)
- [pathspec](https://pypi.org/project/pathspec/) (0.12.1)
- [pefile](https://pypi.org/project/pefile/) (2023.2.7)
- [platformdirs](https://pypi.org/project/platformdirs/) (4.2.0)
- [plyer](https://pypi.org/project/plyer/) (2.1.0)
- [pyinstaller](https://pypi.org/project/pyinstaller/) (6.4.0)
- [pyinstaller-hooks-contrib](https://pypi.org/project/pyinstaller-hooks-contrib/) (2024.1)
- [pytube](https://pypi.org/project/pytube/) (15.0.0)
- [pywin32-ctypes](https://pypi.org/project/pywin32-ctypes/) (0.2.2)
- [setuptools](https://pypi.org/project/setuptools/) (69.1.1)


## Installation

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
