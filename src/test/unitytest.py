from io import StringIO
import os
import sys

from click import progressbar

import pytest # type: ignore
import main
class TestAutomation:
    def test_download_single_video_automation_mp4(self):
        """Test the download of a single video in the automation MP4 format."""
        video_link = "https://music.youtube.com/watch?v=RhmHSAClG1c"
        download_type = "MP4"
        save_directory = "test/unitytest"
        current_video = 1
        downloaded_titles = set()

        main.download_single_video(
            video_link, download_type, save_directory, current_video, downloaded_titles
        )

        assert os.path.exists(os.path.join(save_directory, main.clean_video_title("Video_Title.mp4")))

    def test_download_single_video_automation_mp3(self):
        """Test the download of a single video in the automation MP3 format."""
        video_link = "https://music.youtube.com/watch?v=RhmHSAClG1c"
        download_type = "MP3"
        save_directory = "test/unitytest"
        current_video = 1
        downloaded_titles = set()

        main.download_single_video(
            video_link, download_type, save_directory, current_video, downloaded_titles
        )

        assert os.path.exists(os.path.join(save_directory, main.clean_video_title("Video_Title.mp3")))

    def test_download_playlist_video_automation_mp3(self):
        video_link = "https://music.youtube.com/playlist?list=RDCLAK5uy_nZiG9ehz_MQoWQxY5yElsLHCcG0tv9PRg"
        download_type = "MP3"
        save_directory = "test/unitytest"
        current_video = 1
        downloaded_titles = set()

        main.start_download_playlist_threaded_inner(
            video_link, download_type, save_directory, current_video, downloaded_titles
        )

        assert os.path.exists(os.path.join(save_directory, main.clean_video_title("Video_Title.mp3")))

    def test_display_message_automation(self):
        message = "Test message"
        video_title = "Test Video"

        # Redirect sys.stdout to capture print output
        captured_output = StringIO()
        sys.stdout = captured_output

        main.display_message(message, video_title)

        # Restore sys.stdout
        sys.stdout = sys.__stdout__

        assert "Test Video: Test message" in captured_output.getvalue()

    @pytest.mark.parametrize("chunk,bytes_remaining", [(b"chunk", 500), (b"", 0)])
    def test_on_progress_automation(self, chunk, bytes_remaining):
        # Test on_progress function with automation
        # Mock stream object
        class MockStream:
            filesize = 1000

        # Call the function to be tested
        main.on_progress(MockStream(), chunk, bytes_remaining, 1)

        # Assertions based on expected behavior
        # Check if the progress bar is updated correctly
        assert progressbar.get() == 50.0

    def test_clean_video_title_automation(self):
        # Test cleaning video title with automation
        title = "Test Video #1"
        cleaned_title = main.clean_video_title(title)

        # Assertions based on expected behavior
        # Check if special characters are replaced with underscores
        assert cleaned_title == "Test_Video_1"

    def test_show_error_message_automation(self):
        # Test showing an error message with automation
        error_message = "Test error message"

        # Redirect sys.stdout to capture print output
        captured_output = StringIO()
        sys.stdout = captured_output

        # Call the function to be tested
        main.show_error_message(error_message)

        # Restore sys.stdout
        sys.stdout = sys.__stdout__

        # Assertions based on expected behavior
        # Check if the error message was displayed correctly
        assert error_message in captured_output.getvalue()


if __name__ == "__main__":
    pytest.main()

