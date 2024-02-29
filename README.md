# YouTube Downloader

YouTube Downloader is a simple Python application that allows users to download single YouTube videos or entire playlists as MP4 or MP3 files.

## Features

- Download single YouTube videos by providing the video URL.
- Download entire YouTube playlists by providing the playlist URL.
- Choose between downloading videos as MP4 or extracting audio as MP3.
- Select the save directory for downloaded files.

## Dependencies

- [altgraph](https://pypi.org/project/altgraph/) (0.17.4): A Python graph (network) package that handles graph creation, manipulation, and layout.
- [black](https://pypi.org/project/black/) (24.2.0): An uncompromising Python code formatter that automatically formats your code to ensure consistency.
- [click](https://pypi.org/project/click/) (8.1.7): A Python package for creating command-line interfaces (CLIs) with ease.
- [colorama](https://pypi.org/project/colorama/) (0.4.6): A simple Python package that makes it easy to work with ANSI escape codes to colorize terminal text.
- [mypy-extensions](https://pypi.org/project/mypy-extensions/) (1.0.0): Additional extensions for the MyPy static type checker for Python.
- [packaging](https://pypi.org/project/packaging/) (23.2): A core utility for Python packaging and distribution.
- [pathspec](https://pypi.org/project/pathspec/) (0.12.1): A Python library for matching files using shell-like glob patterns.
- [pefile](https://pypi.org/project/pefile/) (2023.2.7): A Python module to read and work with Portable Executable (PE) files.
- [platformdirs](https://pypi.org/project/platformdirs/) (4.2.0): A Python library for accessing platform-specific directories for data, cache, and config files.
- [plyer](https://pypi.org/project/plyer/) (2.1.0): A platform-independent Python library for accessing features commonly found on various platforms, including notifications.
- [pyinstaller](https://pypi.org/project/pyinstaller/) (6.4.0): A Python package that converts Python scripts into standalone executables, under Windows, Linux, and macOS.
- [pyinstaller-hooks-contrib](https://pypi.org/project/pyinstaller-hooks-contrib/) (2024.1): A collection of hooks for PyInstaller to bundle additional non-Python files.
- [pytube](https://pypi.org/project/pytube/) (15.0.0): A lightweight, dependency-free Python library to fetch YouTube content.
- [pywin32-ctypes](https://pypi.org/project/pywin32-ctypes/) (0.2.2): A Python package that provides access to many of the Windows APIs from Python through ctypes.
- [setuptools](https://pypi.org/project/setuptools/) (69.1.1): A package development process library designed to facilitate packaging Python projects.



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

## Credits
 
Author - FilipP (@niwelator2)
Reporter - Veridicus (@kkwestarz002)


## License
 
MIT License

Copyright (c) [2024] [niwelator2]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
