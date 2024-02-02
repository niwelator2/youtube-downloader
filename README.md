# Youtube downloader

# Build for windows exe comand

1.Go to src directory and run the following command:

```
pyinstaller --onefile --distpath=../windows --icon=logo.ico --name=Youtube-Downloader -y -F --additional-hooks-dir=. --noconsole  main.py
```

Then it will put exe file in windows folder

# How to use

1.Install the required libraries:

```
pip install pytube tqdm
```

2.Run the script:

```
python main.py
```

3.Enter the YouTube video URL when prompted.

4.Choose the download type ('mp4', 'mp3', or 'audio').

5.Enter the directory to save the downloaded files.

# Example

Suppose you want to download a YouTube video with the following details:

URL: https://www.youtube.com/watch?v=79DijItQXMM
Download Type: mp4
Directory: videos

After running the script and providing the required information, the video will be downloaded and saved to the videos directory.

# Pushing to GitLab

```
cd existing_repo
git remote add origin https://gitlab.com/niwelator2/youtube-downloader.git
git branch -M main
git push -uf origin main
```

# License

This project is licensed under the MIT License. See the LICENSE file for details.
