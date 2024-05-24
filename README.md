# YouTube Downloader

YouTube Downloader is a simple Python application that allows users to download single YouTube videos or entire playlists as MP4 or MP3 files.

## Features

- Download single YouTube videos by providing the video URL.
- Download entire YouTube playlists by providing the playlist URL.
- Choose between downloading videos as MP4 or extracting audio as MP3.
- Select the save directory for downloaded files.
- Open an directory  containing downloaded files.


## Dependencies

/*
 TODO: ADD new 
*/

## Installation

```bash
git clone https://github.com/yourusername/youtube-downloader.git
cd youtube-downloader
cd windows/
./Youtube-Downloader.2.3.setup.exe
```

## Build without console window

```bash
 python -m venv venv
 pip install -r requirements.txt
 cd src/
 pyinstaller --onefile --distpath=../windows --icon=../src/gui/icon/logo.ico --name=Youtube-Downloader -y -F --additional-hooks-dir=. --noconsole main.py --add-data "gui/:gui" --add-data "utils/:utils" --add-data "download/:download" --add-data "windows/:windows" 
```

## Build with console window

```bash
    pyinstaller --onefile --distpath=../windows --icon=../src/gui/icon/logo.ico --name=Youtube-Downloader -y -F --additional-hooks-dir=. main.py --add-data "gui/:gui" --add-data "utils/:utils" --add-data "download/:download" --add-data "windows/:windows"
```

## Credits

Author - FilipP (@niwelator2)


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
